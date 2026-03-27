# NeuronMM Storyboard

## Scene 1: HookScene (~45s)
Template: FULL_CENTER
Content:
- CENTER: Paper title fades in, then key result: "2.49x faster LLM inference"
- Animated counter: throughput 49.69 -> 92.52 tokens/s
- Small chip icon representing Trainium
- BOTTOM: "NeuronMM: Song et al., 2025"
Visual anchors: Speedup number in YELLOW
Cleanup: FadeOut all before Scene 2
Equations: None
Data: 2.49x speedup, 49.69->92.52 tokens/s

## Scene 2: MatmulBottleneckScene (~90s)
Template: DUAL_PANEL
Content:
- LEFT: Matmul dominance visualization -- stacked bars showing compute breakdown (matmul ~60-80%)
- RIGHT: Accelerator comparison: GPU (CUDA cores, HBM) vs Trainium (systolic array, SBUF) side by side
- BOTTOM: "Matmul accounts for majority of LLM inference compute"
Visual anchors: Matmul bar highlighted in RED
Cleanup: FadeOut all
Equations: Y = XW (the fundamental operation)
Data: A100 ~312 TFLOPS, Trainium NeuronCore ~95 TFLOPS at 60% cost

## Scene 3: TrainiumArchScene (~120s)
Template: BUILD_UP
Content:
- Build NeuronCore from outside in:
  1. Start with chip outline
  2. Add Tensor Engine (128x128 systolic array) -- the star of the show
  3. Add SBUF (24MB on-chip), PSUM (2MB accumulator)
  4. Add HBM (16GB off-chip) connected via DMA
- Show memory hierarchy: HBM (16GB, slow) -> SBUF (24MB, fast) -> PSUM (2MB, fastest)
- Animate a tile flowing through: HBM -> DMA -> SBUF -> Tensor Engine -> PSUM -> SBUF -> DMA -> HBM
- BOTTOM: "Three-level data layout: Tile (128x128), Block, Strip"
Visual anchors: Memory hierarchy boxes with capacity labels
Cleanup: Dim to 0.1 (will reuse in Scene 6)
Equations: None
Data: 16GB HBM, 24MB SBUF (128 partitions), 2MB PSUM (128 partitions, 8 banks)

## Scene 4: SVDDecompositionScene (~90s)
Template: FULL_CENTER
Content:
- Show W (large matrix) with dimensions [k x n]
- SVD animation: W splits into U * Sigma * V^T
- Keep top-r singular values: W ~ U_r * V_r (absorb Sigma into U or V)
- Show XW -> X * U * V (two smaller matmuls)
- Dimension annotations: X[m,k] * U[k,r] * V[r,n] where r << min(k,n)
- Show FLOPs comparison: mkn vs mkr + mrn (savings when r small)
- BOTTOM: "But naive execution makes things WORSE..."
Visual anchors: Matrix dimension labels
Cleanup: FadeOut, leave "XUV" text for transition
Equations:
  - W = U \Sigma V^T
  - W \approx U_r V_r
  - XW \to X U V
Data: Compression ratios 0.1, 0.2

## Scene 5: ThreeChallengesScene (~90s)
Template: BUILD_UP -> GRID_CARDS
Content:
- Three cards appear one by one:
  1. I/O Bottleneck: diagram showing X*U -> [write Y to HBM] -> [read Y from HBM] -> Y*V
     Label: "65% more DMA transfer, 2x HBM traffic"
  2. Recomputation: naive fusion recomputes Y blocks 16x
     Label: "11x slower (18.06ms vs 1.57ms)"
  3. Transpose: systolic array needs stationary matrix transposed
     Label: "Intermediate Y must be transposed between matmuls"
- BOTTOM: "All three must be solved simultaneously"
Visual anchors: Three challenge cards in RED/ORANGE
Cleanup: FadeOut all
Data: 65% more DMA, 11x slower, 4x FLOPs increase

## Scene 6: TrainiumFusionScene (~120s)
Template: TOP_PERSISTENT_BOTTOM_CONTENT
Content:
- TOP: Small pipeline: X -> [XU] -> cache -> [cached * V] -> O
- BOTTOM: Detailed animation:
  1. Show SBUF as a large rectangle (24MB)
  2. Compute XU row strip (shape BM x r) -- fits in SBUF!
  3. Cache the entire strip in SBUF (highlight in GREEN)
  4. For each column block of V: multiply cached result, accumulate in PSUM, write to HBM
  5. Show reuse: the cached strip is read ceil(n/BN) times from SBUF, NOT HBM
- Key insight: intermediate never touches HBM
- BOTTOM note: "Entire intermediate cached in 24MB SBUF"
Visual anchors: SBUF rectangle with fill level indicator
Cleanup: FadeOut detail, keep pipeline
Equations: None (visual explanation)
Data: 24MB SBUF, BM*r fits when r is small

## Scene 7: ImplicitTransposeScene (~60s)
Template: DUAL_PANEL
Content:
- LEFT: "Naive" -- compute Y=XU, then transpose Y for next matmul (expensive)
- RIGHT: "NeuronMM" -- compute (XU)^T = U^T * X^T directly via NKI
  - Swap stationary and moving operands
  - Result is already transposed, zero overhead
- Show equation transform with ReplacementTransform
- BOTTOM: "Zero-cost transposition by swapping operand roles"
Visual anchors: Transpose operation crossed out in RED on right side
Cleanup: FadeOut all
Equations:
  - Y = X \cdot U
  - Y^T = U^T \cdot X^T
Data: None

## Scene 8: BlockSizeOptScene (~90s)
Template: CHART_FOCUS
Content:
- Plot 1: Arithmetic Intensity vs BM (x-axis: 128, 256, 512, 1024, 2048, 4096)
  - Show AI = 2r / ((1 + r/BM) * s)
  - Horizontal line at AI=222 (BF16 compute-bound threshold)
  - BM=1024 crosses the threshold
- Plot 2 (or overlay): SBUF usage % vs BM
  - BM=1024: 90% SBUF, no spill
  - BM=2048: 96% SBUF, 29MB spill (RED region)
  - BM=4096: 99% SBUF, 931MB spill (RED region)
- Highlight sweet spot at BM=1024
- BOTTOM: "BM=1024: maximum AI without SBUF spilling"
Visual anchors: Sweet spot dot at BM=1024
Cleanup: FadeOut all
Equations: AI = 2r / ((1 + r/BM) \cdot s)
Data: Table 3 from paper

## Scene 9: ResultsScene (~90s)
Template: CHART_FOCUS -> GRID_CARDS
Content:
- Bar chart: Kernel speedup by model (Llama-3.2-1B, 3B, Qwen3-1.7B, 4B)
  - Baseline = 1.0, NeuronMM bars
  - Highlight max: 2.22x kernel speedup
- Second chart or transition: End-to-end speedup
  - Llama-3.2-3B: 2.49x (highlight)
- Grid: Model accuracy impact
  - Llama-3.2-1B: -0.07 mAcc drop
  - Llama-3.2-3B: -0.10
  - Qwen3-1.7B: -0.03
  - Qwen3-4B: -0.05
- BOTTOM: "Negligible accuracy loss with LoRA fine-tuning"
Visual anchors: 2.49x speedup number
Cleanup: FadeOut all
Data: Table 4 from paper

## Scene 10: LimitationsScene (~45s)
Template: FULL_CENTER
Content:
- Bullet list of limitations:
  1. MLP layers only (70% of params) -- attention layers cause accuracy degradation
  2. Single NeuronCore evaluation -- multi-chip scaling untested
  3. Requires offline SVD + LoRA fine-tuning
  4. Trainium-specific -- techniques not directly portable
- Open questions: Can attention layers be compressed differently? Multi-chip NCCL overhead?
- Paper citation card: title, authors, year, arXiv link
- BOTTOM: "Open-sourced: github.com/dinghongsong/NeuronMM"
Visual anchors: Citation card
Cleanup: FadeOut all
