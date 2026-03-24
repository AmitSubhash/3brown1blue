#!/usr/bin/env bash
# Visual audit script for 3brown1blue Manim projects.
# Extracts frames from rendered scene MP4s and prints a quality summary.
#
# Usage: ./audit_video.sh [project_dir] [quality]
#   project_dir  - path to project containing scene_*.py and media/  (default: .)
#   quality      - one of 480p15, 720p30, 1080p60, 2160p60           (default: 1080p60)
#
# Output:
#   audit_frames/<scene_name>_<pct>.jpg  (5 frames per scene)
#   Summary table printed to stdout

set -euo pipefail

# ── Arguments ────────────────────────────────────────────────────────────────
PROJECT_DIR="${1:-.}"
QUALITY="${2:-1080p60}"

# ── Validate inputs ───────────────────────────────────────────────────────────
if [ ! -d "$PROJECT_DIR" ]; then
    echo "ERROR: project_dir '$PROJECT_DIR' does not exist." >&2
    exit 1
fi

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

# ── Setup output dir ──────────────────────────────────────────────────────────
AUDIT_DIR="$PROJECT_DIR/audit_frames"
mkdir -p "$AUDIT_DIR"

# ── Collect scene MP4s in order ───────────────────────────────────────────────
# Find all MP4s for the requested quality, excluding partial_movie_files
# Collect into a temp file to avoid subshell scope issues (no pipefail risk)
TMPFILE=$(mktemp /tmp/audit_scenes.XXXXXX)
trap 'rm -f "$TMPFILE"' EXIT

find "$MEDIA_DIR" \
    -path "*/partial_movie_files" -prune \
    -o -path "*/${QUALITY}/*.mp4" -print \
    | sort > "$TMPFILE"

SCENE_COUNT=$(wc -l < "$TMPFILE" | tr -d ' ')

if [ "$SCENE_COUNT" -eq 0 ]; then
    echo "ERROR: No MP4s found for quality '$QUALITY' under '$MEDIA_DIR'." >&2
    echo "       Render your scenes first, or try a different quality level." >&2
    exit 1
fi

echo "=================================================================="
echo "  3brown1blue Visual Audit"
echo "  Project : $PROJECT_DIR"
echo "  Quality : $QUALITY"
echo "  Scenes  : $SCENE_COUNT"
echo "=================================================================="
echo ""

# ── Per-scene processing ──────────────────────────────────────────────────────
# Frame percentages: 10, 25, 50, 75, 90
FRAME_PCTS="10 25 50 75 90"

TOTAL_SECONDS=0
SCENE_IDX=0

# Read line-by-line from temp file (no subshell, compatible with set -e)
while IFS= read -r MP4_PATH; do
    SCENE_IDX=$(( SCENE_IDX + 1 ))

    # Extract human-readable scene name from path:
    # .../media/videos/scene_01_hook/1080p60/HookScene.mp4
    # -> scene_01_hook/HookScene
    QUALITY_DIR=$(dirname "$MP4_PATH")
    SCENE_STEM=$(basename "$(dirname "$QUALITY_DIR")")
    CLASS_NAME=$(basename "$MP4_PATH" .mp4)
    SCENE_LABEL="${SCENE_STEM}/${CLASS_NAME}"

    # File size
    FILE_SIZE=$(du -h "$MP4_PATH" | cut -f1)
    FILE_BYTES=$(stat -f%z "$MP4_PATH" 2>/dev/null || stat -c%s "$MP4_PATH" 2>/dev/null || echo "0")

    # Duration and frame count via ffprobe
    DURATION_RAW=$(ffprobe -v error \
        -select_streams v:0 \
        -show_entries format=duration \
        -of default=noprint_wrappers=1:nokey=1 \
        "$MP4_PATH" 2>/dev/null || echo "0")

    # Round to 2 decimal places using printf (no bc needed)
    DURATION=$(printf "%.2f" "$DURATION_RAW")

    FRAME_COUNT=$(ffprobe -v error \
        -select_streams v:0 \
        -count_packets \
        -show_entries stream=nb_read_packets \
        -of default=noprint_wrappers=1:nokey=1 \
        "$MP4_PATH" 2>/dev/null || echo "0")

    # Accumulate total (integer seconds for portability)
    DURATION_INT=$(printf "%.0f" "$DURATION_RAW")
    TOTAL_SECONDS=$(( TOTAL_SECONDS + DURATION_INT ))

    printf "Scene %02d: %s\n" "$SCENE_IDX" "$SCENE_LABEL"
    printf "  Duration : %ss  |  Frames : %s  |  Size : %s\n" \
        "$DURATION" "$FRAME_COUNT" "$FILE_SIZE"

    # Extract frames at each percentage
    FRAME_TAGS=""
    for PCT in $FRAME_PCTS; do
        # Time offset = duration * pct / 100
        # Use awk for float arithmetic (no bc dependency)
        OFFSET=$(awk "BEGIN { printf \"%.3f\", $DURATION_RAW * $PCT / 100 }")
        FRAME_FILE="${AUDIT_DIR}/${SCENE_STEM}_${CLASS_NAME}_pct${PCT}.jpg"

        ffmpeg -y -ss "$OFFSET" -i "$MP4_PATH" \
            -frames:v 1 -q:v 2 \
            "$FRAME_FILE" \
            -loglevel error 2>/dev/null || true

        if [ -f "$FRAME_FILE" ]; then
            FRAME_TAGS="${FRAME_TAGS} pct${PCT}=OK"
        else
            FRAME_TAGS="${FRAME_TAGS} pct${PCT}=FAIL"
        fi
    done

    printf "  Frames   :%s\n\n" "$FRAME_TAGS"

done < "$TMPFILE"

# ── Summary ───────────────────────────────────────────────────────────────────
TOTAL_MIN=$(( TOTAL_SECONDS / 60 ))
TOTAL_SEC=$(( TOTAL_SECONDS % 60 ))
TOTAL_FRAMES_DIR=$(find "$AUDIT_DIR" -name "*.jpg" | wc -l | tr -d ' ')

echo "=================================================================="
echo "  Summary"
echo "  Total scenes    : $SCENE_COUNT"
echo "  Total duration  : ${TOTAL_MIN}m ${TOTAL_SEC}s  (~${TOTAL_SECONDS}s)"
echo "  Frames saved    : $TOTAL_FRAMES_DIR  -> $AUDIT_DIR"
echo "=================================================================="
echo ""

# ── Visual inspection checklist ───────────────────────────────────────────────
cat <<'CHECKLIST'
Visual Inspection Checklist
---------------------------
Open audit_frames/ and review each set of 5 frames.

Layout & Overflow
  [ ] No text or graphics extending past the frame edges
  [ ] No elements with |x| > 5.5 or |y| > 3.2 (safe zone violation)
  [ ] Bottom notes have sufficient margin (buff >= 0.5)
  [ ] All text fits horizontally - no truncation or right-edge overflow

Text Quality
  [ ] No overlapping text (title + body + caption in same region)
  [ ] Bottom text replaced cleanly - old note gone before new note appears
  [ ] Multi-line text is manually broken with \n, not auto-wrapped
  [ ] Labels are next_to their target object, not floating at arbitrary coords

Container & Alignment
  [ ] Child elements fit within parent container bounds
  [ ] Groups are arranged with arrange() - no manual grid positioning
  [ ] No flipped or mirrored shapes

Timing & Density
  [ ] Mid-scene frame (50%) looks substantive - not an empty transition
  [ ] Early scenes (01-02): 3-5 elements visible (sparse)
  [ ] Middle scenes (03-08): 6-10 elements visible (building)
  [ ] Late scenes (09-11): 10-15 elements at peak density
  [ ] Final scene: returns to 3-5 elements (resolution)

Data Visualization
  [ ] Bar widths >= 0.3 and heights >= 0.2 (visible at 720p)
  [ ] Fill opacity >= 0.6 for data elements
  [ ] Stroke opacity >= 0.8 for lines and borders
  [ ] Dot radius >= 0.06
  [ ] Axes width >= 5.0 (at least 40% of frame)

Background & Opacity
  [ ] Dimmed elements are at 0.1 opacity (not 0.3 - too visible on dark bg)
  [ ] FadeOut used (not dim) when new content occupies the same region
  [ ] Content fills >= 50% of frame - no large dead zones

Lifecycle
  [ ] Titles FadeOut before new content enters their region
  [ ] No persistent ghost elements from previous animation phases
  [ ] Scenes end cleanly (fade_all called)

Visual Variety (across all scenes)
  [ ] No two consecutive scenes use the same visual technique
  [ ] At least one ValueTracker/always_redraw scene visible
  [ ] At least one MovingCamera (zoom) scene visible
  [ ] At least 5 distinct visual techniques total
  [ ] At least 2 question-frame scenes included

CHECKLIST
