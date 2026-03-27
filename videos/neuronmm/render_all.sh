#!/bin/bash
# Render all NeuronMM scenes and concatenate into final video.
# Usage: ./render_all.sh [quality]
#   quality: l (480p), m (720p), h (1080p), k (4K)
#   default: h (1080p)

set -euo pipefail

QUALITY="${1:-h}"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

SCENES=(
    "scene_01_hook.py HookScene"
    "scene_02_bottleneck.py MatmulBottleneckScene"
    "scene_03_architecture.py TrainiumArchScene"
    "scene_04_svd.py SVDDecompositionScene"
    "scene_05_challenges.py ThreeChallengesScene"
    "scene_06_fusion.py TrainiumFusionScene"
    "scene_07_transpose.py ImplicitTransposeScene"
    "scene_08_blocksize.py BlockSizeOptScene"
    "scene_09_results.py ResultsScene"
    "scene_10_limitations.py LimitationsScene"
)

# Map quality to resolution folder name
case "$QUALITY" in
    l) RES_DIR="480p15" ;;
    m) RES_DIR="720p30" ;;
    h) RES_DIR="1080p60" ;;
    k) RES_DIR="2160p60" ;;
    *) echo "Unknown quality: $QUALITY (use l, m, h, or k)"; exit 1 ;;
esac

echo "=== Rendering ${#SCENES[@]} scenes at quality -q${QUALITY} ==="

FAILED=0
for entry in "${SCENES[@]}"; do
    FILE=$(echo "$entry" | awk '{print $1}')
    CLASS=$(echo "$entry" | awk '{print $2}')
    echo ""
    echo "--- Rendering $FILE :: $CLASS ---"
    if ! manim -q"$QUALITY" "$FILE" "$CLASS"; then
        echo "FAILED: $FILE :: $CLASS"
        FAILED=$((FAILED + 1))
    fi
done

if [ "$FAILED" -gt 0 ]; then
    echo ""
    echo "=== $FAILED scene(s) failed to render ==="
    exit 1
fi

echo ""
echo "=== All scenes rendered. Concatenating... ==="

# Build ffmpeg concat list
CONCAT_FILE="$SCRIPT_DIR/concat_list.txt"
> "$CONCAT_FILE"

for entry in "${SCENES[@]}"; do
    FILE=$(echo "$entry" | awk '{print $1}')
    CLASS=$(echo "$entry" | awk '{print $2}')
    BASENAME="${FILE%.py}"
    VIDEO_PATH="$SCRIPT_DIR/media/videos/${BASENAME}/${RES_DIR}/${CLASS}.mp4"
    if [ -f "$VIDEO_PATH" ]; then
        echo "file '$VIDEO_PATH'" >> "$CONCAT_FILE"
    else
        echo "WARNING: Missing $VIDEO_PATH"
    fi
done

OUTPUT="$SCRIPT_DIR/NeuronMM_full_${QUALITY}.mp4"
ffmpeg -y -f concat -safe 0 -i "$CONCAT_FILE" -c copy "$OUTPUT" 2>/dev/null

echo ""
echo "=== Done! Final video: $OUTPUT ==="
echo "=== Scenes: ${#SCENES[@]}, Quality: ${QUALITY} ==="
