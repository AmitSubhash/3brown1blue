# NeuronMM: High-Performance Matrix Multiplication for LLM Inference on AWS Trainium

## Paper Metadata
- **arXiv:** 2510.25977
- **Authors:** Dinghong Song (UC Merced), Jierui Xu (UW Madison), Weichu Yang (UW Madison), Pengfei Su (UC Merced), Dong Li (UC Merced)
- **Submitted:** Oct 2025 (v3: Nov 2025)
- **Code:** https://github.com/dinghongsong/NeuronMM

## Core Problem
LLM inference on AI accelerators like AWS Trainium is challenging due to:
1. Systolic array architecture requiring repeated load-compute-store cycles with small SRAM
2. Tensor logical shape must align with physical memory layout; misalignment requires costly transposes

## Key Insight
Apply SVD to weight matrices (W ~ UV), transforming XW into XUV (two smaller matmuls), then fuse the two matmuls with SRAM-aware caching to eliminate HBM round-trips.

## Technical Contributions

### 1. Block-Aligned SVD
- Standard SVD: W = U Sigma V^T, keep top-k singular values
- Innovation: rank r = floor((k*n*(1-ratio)) / ((k+n)*block_size) + alpha) * block_size
- Aligns rank with hardware tile boundaries (128x128 systolic array)
- LoRA fine-tuning recovers accuracy post-compression

### 2. TrainiumFusion (Kernel Fusion)
Three techniques:
- **Caching:** Compute entire intermediate row strip (XU)_{m*} and cache in SBUF (24MB). Reuse for all V column strips.
- **Implicit Transposition:** (XU)^T = U^T * X^T -- produces transposed result with zero overhead
- **Blocking:** Two-phase inner loops per row strip: (1) compute+cache (XU)^T, (2) multiply cached result with V blocks

### 3. Trainium Architecture Details
- Per NeuronCore: Tensor Engine (128x128 systolic array), Scalar/Vector/GPSIMD engines
- Memory: 16GB HBM (off-chip), 24MB SBUF (on-chip, 128 partitions), 2MB PSUM (accumulator)
- Three-level data layout: Tile (max 128x128), Block (tiles grouped), Strip (blocks spanning one dim)

### 4. Challenges Overcome
- **I/O Bottleneck:** Sequential XUV causes 65% more DMA time, 2x HBM traffic
- **Recomputation:** Naive fusion recomputes intermediates 16x (11x slower)
- **Transpose:** Systolic array needs stationary matrix transposed; intermediate transpose between fused matmuls

### 5. Key Equations
- Arithmetic Intensity: AI = 2r / ((1 + r/BM) * s)
- Peak SBUF Usage: (BM*r + (BM+Br)*max(BK,BN)) * s
- Optimal BM: saturate tensor engine (AI >= 222 Flops/Byte for BF16) while fitting in 24MB SBUF

## Results
- **Kernel:** Average 1.35x speedup (up to 2.22x) over AWS baseline
- **End-to-end:** Average 1.66x speedup (up to 2.49x)
- **Throughput:** 49.69 -> 92.52 tokens/s (Llama-3.2-1B)
- **Models:** Llama-3.2-1B, Llama-3.2-3B, Qwen3-1.7B, Qwen3-4B
- Optimal block size BM=1024 (90% SBUF, no spill)
- BM=2048+ causes SBUF spilling, degraded performance

## Limitations
- Only applied to MLP layers (70% of params), not attention
- Applying to both causes accuracy degradation even with fine-tuning
- Requires offline SVD + LoRA fine-tuning (not zero-shot)
- Tested only on single NeuronCore, not multi-chip scaling
