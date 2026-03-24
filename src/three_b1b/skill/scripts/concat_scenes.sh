#!/usr/bin/env bash
# Concatenate rendered Manim scene MP4s into a single final video.
# Finds all scene MP4s for the given quality in numeric order and joins them
# using ffmpeg's concat demuxer (stream copy - no re-encode).
#
# Usage: ./concat_scenes.sh [project_dir] [quality]
#   project_dir  - path to project containing scene_*.py and media/  (default: .)
#   quality      - one of 480p15, 720p30, 1080p60, 2160p60           (default: 1080p60)
#
# Output:
#   <project_dir>/final_<quality>.mp4

set -euo pipefail

# ── Arguments ─────────────────────────────────────────────────────────────────
PROJECT_DIR="${1:-.}"
QUALITY="${2:-1080p60}"

# ── Validate inputs ───────────────────────────────────────────────────────────
if [ ! -d "$PROJECT_DIR" ]; then
    echo "ERROR: project_dir '$PROJECT_DIR' does not exist." >&2
    exit 1
fi

# Resolve to absolute path so ffmpeg concat list paths are always absolute
PROJECT_DIR="$(cd "$PROJECT_DIR" && pwd)"

MEDIA_DIR="$PROJECT_DIR/media/videos"
if [ ! -d "$MEDIA_DIR" ]; then
    echo "ERROR: media/videos not found under '$PROJECT_DIR'." >&2
    echo "       Have you rendered any scenes yet?" >&2
    exit 1
fi

# Validate quality value
case "$QUALITY" in
    480p15|720p30|1080p60|2160p60) ;;
    *)
        echo "ERROR: quality must be one of: 480p15, 720p30, 1080p60, 2160p60" >&2
        echo "       Got: '$QUALITY'" >&2
        exit 1
        ;;
esac

# Check ffmpeg and ffprobe are available
for tool in ffmpeg ffprobe; do
    if ! command -v "$tool" >/dev/null 2>&1; then
        echo "ERROR: '$tool' not found. Install ffmpeg to use this script." >&2
        exit 1
    fi
done

# ── Collect scene MP4s in sorted order ───────────────────────────────────────
# Collect into a temp file (avoids subshell scope issues with set -e)
TMPLIST=$(mktemp /tmp/concat_list.XXXXXX.txt)
trap 'rm -f "$TMPLIST"' EXIT

# Find MP4s at the requested quality level, excluding partial_movie_files,
# then sort so scene_01 < scene_02 < ... regardless of class name
find "$MEDIA_DIR" \
    -path "*/partial_movie_files" -prune \
    -o -path "*/${QUALITY}/*.mp4" -print \
    | sort > "$TMPLIST"

SCENE_COUNT=$(wc -l < "$TMPLIST" | tr -d ' ')

if [ "$SCENE_COUNT" -eq 0 ]; then
    echo "ERROR: No MP4s found for quality '$QUALITY' under '$MEDIA_DIR'." >&2
    echo "       Render your scenes first, or try a different quality level." >&2
    exit 1
fi

# ── Build ffmpeg concat list ──────────────────────────────────────────────────
# ffmpeg concat demuxer requires absolute paths (resolves relative to the
# list file's directory, not the working directory).
CONCAT_LIST=$(mktemp /tmp/ffmpeg_concat.XXXXXX.txt)
trap 'rm -f "$TMPLIST" "$CONCAT_LIST"' EXIT

echo "=================================================================="
echo "  3brown1blue Scene Concatenation"
echo "  Project : $PROJECT_DIR"
echo "  Quality : $QUALITY"
echo "  Scenes  : $SCENE_COUNT"
echo "=================================================================="
echo ""
echo "Scene order:"

SCENE_IDX=0
while IFS= read -r MP4_PATH; do
    SCENE_IDX=$(( SCENE_IDX + 1 ))

    # Derive a readable label: scene_01_hook/HookScene
    QUALITY_DIR=$(dirname "$MP4_PATH")
    SCENE_STEM=$(basename "$(dirname "$QUALITY_DIR")")
    CLASS_NAME=$(basename "$MP4_PATH" .mp4)

    printf "  %02d. %s/%s  -> %s\n" \
        "$SCENE_IDX" "$SCENE_STEM" "$CLASS_NAME" "$MP4_PATH"

    # Write absolute path to concat list (safe 0 allows non-relative paths)
    printf "file '%s'\n" "$MP4_PATH" >> "$CONCAT_LIST"

done < "$TMPLIST"

echo ""

# ── Run ffmpeg concat ─────────────────────────────────────────────────────────
OUTPUT="$PROJECT_DIR/final_${QUALITY}.mp4"

echo "Concatenating $SCENE_COUNT scenes into:"
echo "  $OUTPUT"
echo ""

ffmpeg -y \
    -f concat \
    -safe 0 \
    -i "$CONCAT_LIST" \
    -c copy \
    "$OUTPUT"

# ── Report final stats ────────────────────────────────────────────────────────
if [ ! -f "$OUTPUT" ]; then
    echo "ERROR: ffmpeg did not produce output file." >&2
    exit 1
fi

FINAL_DURATION=$(ffprobe -v error \
    -select_streams v:0 \
    -show_entries format=duration \
    -of default=noprint_wrappers=1:nokey=1 \
    "$OUTPUT" 2>/dev/null || echo "0")

FINAL_DURATION_FMT=$(printf "%.2f" "$FINAL_DURATION")
DURATION_INT=$(printf "%.0f" "$FINAL_DURATION")
TOTAL_MIN=$(( DURATION_INT / 60 ))
TOTAL_SEC=$(( DURATION_INT % 60 ))

FINAL_SIZE=$(du -h "$OUTPUT" | cut -f1)

echo "=================================================================="
echo "  Done"
printf "  Output file    : %s\n" "$OUTPUT"
printf "  Total duration : %sm %ss  (~%ss)\n" \
    "$TOTAL_MIN" "$TOTAL_SEC" "$FINAL_DURATION_FMT"
printf "  File size      : %s\n" "$FINAL_SIZE"
echo "=================================================================="
