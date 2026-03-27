# NeuronMM Video Curriculum

## Audience: Graduate (systems/ML researchers)
## Domain: Machine Learning / Computer Architecture
## Target: 10 scenes, ~14 minutes

---

## Scene 1: Hook (~45s)
**Insight:** NeuronMM achieves 2.49x end-to-end LLM inference speedup on Trainium via hardware-aware SVD fusion
**Template:** FULL_CENTER
**Patterns:** Title card with key result, speedup counter animation
**Narration timestamps:** [0:00-0:45]

## Scene 2: The Matmul Bottleneck (~90s)
**Insight:** LLM inference is dominated by matmul; AI accelerators have different constraints than GPUs
**Template:** DUAL_PANEL
**Patterns:** Left: matmul dominance pie chart; Right: accelerator landscape
**Narration timestamps:** [0:45-2:15]

## Scene 3: Trainium Architecture (~120s)
**Insight:** Trainium's memory hierarchy (HBM->SBUF->PSUM) and 128x128 systolic array dictate optimization strategy
**Template:** BUILD_UP
**Patterns:** Layer-by-layer architecture reveal with memory sizes
**Narration timestamps:** [2:15-4:15]

## Scene 4: SVD Decomposition (~90s)
**Insight:** W ~ UV transforms one big matmul into two smaller ones, but naive execution is WORSE
**Template:** FULL_CENTER
**Patterns:** Equation decomposition (dim-highlight-color), matrix splitting animation
**Narration timestamps:** [4:15-5:45]

## Scene 5: The Three Challenges (~90s)
**Insight:** I/O bottleneck (65% more DMA), recomputation (11x slower), transpose overhead
**Template:** BUILD_UP -> GRID_CARDS
**Patterns:** Three challenge cards with profiling data
**Narration timestamps:** [5:45-7:15]

## Scene 6: TrainiumFusion - Caching (~120s)
**Insight:** Cache entire intermediate row strip in 24MB SBUF; reuse for all V column strips
**Template:** TOP_PERSISTENT_BOTTOM_CONTENT
**Patterns:** Pipeline at top, data flow animation showing SBUF caching
**Narration timestamps:** [7:15-9:15]

## Scene 7: Implicit Transposition (~60s)
**Insight:** (XU)^T = U^T * X^T -- zero-cost transposition by swapping operand roles
**Template:** DUAL_PANEL
**Patterns:** Equation transform, before/after comparison
**Narration timestamps:** [9:15-10:15]

## Scene 8: Block Size Optimization (~90s)
**Insight:** BM=1024 is optimal -- maximizes arithmetic intensity without SBUF spilling
**Template:** CHART_FOCUS
**Patterns:** AI vs BM curve, SBUF usage bars, spill threshold
**Narration timestamps:** [10:15-11:45]

## Scene 9: Results (~90s)
**Insight:** 1.35x kernel speedup (up to 2.22x), 1.66x E2E speedup (up to 2.49x), near 2x throughput
**Template:** CHART_FOCUS -> GRID_CARDS
**Patterns:** Bar charts for speedups, model comparison grid
**Narration timestamps:** [11:45-13:15]

## Scene 10: Limitations and Open Questions (~45s)
**Insight:** MLP-only, single NeuronCore, requires offline SVD+LoRA; multi-chip and attention layers remain open
**Template:** FULL_CENTER
**Patterns:** Limitation list with paper citation card
**Narration timestamps:** [13:15-14:00]
