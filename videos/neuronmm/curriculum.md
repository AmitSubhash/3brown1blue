# NeuronMM Video Curriculum (v3 -- Full Educational Build-Up)

## Audience: Curious learner who wants to deeply understand GPU/AI hardware
## Goal: Teach the full stack, then show how NeuronMM optimizes it
## Target: 15 scenes, ~20-25 minutes

### Teaching philosophy:
- Every concept introduced with WHY it matters before WHAT it is
- Data flow animations through every hardware component
- GPU education is a first-class goal, not just background
- Build mental model layer by layer: CPU -> GPU -> Memory -> Accelerators -> Optimization

---

## ACT 1: FOUNDATIONS (Scenes 1-5)

### Scene 1: Hook (~30s)
AI chatbots are slow and expensive. What if 2.5x faster?

### Scene 2: What LLMs Actually Do (~75s)
Word-by-word prediction. Each word = massive math. The math is matrix multiplication.

### Scene 3: Matrix Multiplication From Scratch (~120s)
What a matrix is. Row-times-column with real numbers. Why it's the core operation.
Animate a full 3x3 multiply step by step. Then show LLM scale (4096x4096).

### Scene 4: How a CPU Processes Data (~90s)
Fetch-decode-execute cycle. One operation at a time. Sequential processing.
Show data flowing: RAM -> Cache -> Register -> ALU -> back.
Why CPUs are slow at matrix math: one multiply at a time.

### Scene 5: Enter the GPU (~120s)
Thousands of small cores running in parallel. CUDA cores.
Show: CPU does 1 multiply per cycle, GPU does thousands simultaneously.
Data flow: CPU RAM -> PCIe -> GPU VRAM -> SM -> CUDA cores -> back.
Why GPUs revolutionized AI.

## ACT 2: THE MEMORY WALL (Scenes 6-8)

### Scene 6: The Memory Hierarchy (~120s)
Speed vs size tradeoff. Registers (fastest, tiny) -> Cache -> RAM -> Disk (slowest, huge).
Kitchen analogy: hands -> countertop -> fridge -> warehouse.
Actual numbers: latency and bandwidth at each level.
This applies to both CPUs and GPUs.

### Scene 7: GPU Memory Deep Dive (~90s)
HBM (High Bandwidth Memory): what it is, why GPUs need it.
GPU memory hierarchy: HBM -> L2 Cache -> Shared Memory -> Registers.
Data flow animation through a GPU for one matrix multiply.
The memory wall: compute is fast, but feeding data to compute is the bottleneck.

### Scene 8: The Bandwidth Bottleneck (~75s)
Arithmetic intensity: ratio of compute to memory access.
If you can't keep the cores fed, they sit idle.
Show: GPU cores waiting while data crawls from HBM.
This is THE fundamental problem in AI inference.

## ACT 3: CUSTOM AI CHIPS (Scenes 9-11)

### Scene 9: Beyond GPUs -- AI Accelerators (~75s)
Google TPU, AWS Trainium, custom silicon.
Why build custom: remove GPU generality, optimize for matrix math only.
Trainium: 95 TFLOPS at 60% GPU cost. Two NeuronCores per chip.

### Scene 10: Inside Trainium (~120s)
The systolic array: a grid of multiply-accumulate units.
Data flows through the grid like a wave.
128x128 array: 16,384 multiplications per cycle.
Three-level memory: HBM (16GB) -> SBUF (24MB) -> PSUM (2MB).
Full data flow: HBM -> DMA -> SBUF -> Systolic Array -> PSUM -> SBUF -> DMA -> HBM.

### Scene 11: Trainium's Constraints (~60s)
Stationary matrix must be transposed (systolic array requirement).
Data must fit in tiles (128x128 max).
SBUF is the critical resource: only 24MB.
These constraints drive every optimization decision.

## ACT 4: THE NEURONMM OPTIMIZATION (Scenes 12-15)

### Scene 12: SVD -- Splitting Big Matrices (~90s)
What SVD is: factoring a matrix into two smaller ones.
Visual: big rectangle splits into thin-tall x short-wide.
XW becomes X*U*V: two smaller matmuls instead of one big one.
FLOPs savings with concrete numbers.

### Scene 13: Why Naive SVD Fails + NeuronMM's Fix (~120s)
Challenge 1: intermediate result goes to HBM (65% more traffic).
Challenge 2: naive fusion recomputes 16x (11x slower).
NeuronMM's solution: cache intermediate in SBUF, reuse for each V block.
Full data flow animation through the fused kernel.

### Scene 14: Results (~75s)
Kernel speedup: 1.35x average, up to 2.22x.
End-to-end: 1.66x average, up to 2.49x.
Throughput: 50 -> 93 tokens/s.
Accuracy: less than 0.1% drop with LoRA fine-tuning.

### Scene 15: What We Learned + What's Next (~45s)
Recap the full stack: LLM -> matmul -> GPU -> memory wall -> Trainium -> SVD -> NeuronMM.
Limitations: MLP only, single chip, requires fine-tuning.
Open questions. Citation card.
