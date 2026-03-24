---
name: Machine Learning Domain Rules
description: Visual vocabulary, preferred templates, notation, and patterns for machine learning paper explainers
tags: [manim, domain, machine-learning]
---

# Machine Learning Explainer Rules

## Visual Vocabulary

Viewers of ML explainers expect to see these diagram types. If your video lacks them, it feels generic:

- **Architecture diagrams**: boxes for layers, left-to-right data flow, color-coded by layer type
- **Attention heatmaps**: token x token matrix with shaded cells encoding weight magnitude
- **Loss curves**: training vs validation, epoch counter, the classic "divergence" shape for overfitting
- **Gradient flow**: forward pass in one color, backward pass arrows overlaid in a contrasting color
- **Weight matrices**: grids with per-cell sign coloring (pattern #2: positive=teal, negative=red)
- **Embedding space**: 2D projection (PCA/t-SNE) where similar items cluster together
- **Data tensors**: concrete arrays with real numeric values, not placeholder variables

## Preferred Layout Templates

| Concept | Template | Reason |
|---|---|---|
| Single architecture overview | FULL_CENTER | One diagram, needs full width |
| Forward vs backward pass | DUAL_PANEL | Two simultaneous flows |
| Pipeline + layer detail | TOP_PERSISTENT_BOTTOM_CONTENT | Full pipeline stays; zoom into one stage |
| Building a loss function term by term | BUILD_UP | Terms accumulate with each step |
| Loss curve / accuracy chart | CHART_FOCUS | Axes are the main element |
| Attention head gallery | GRID_CARDS | Multiple heads shown simultaneously |

## Domain-Specific Visual Patterns

### ML-1: Layer-by-Layer Architecture Build
Reveal the architecture one layer at a time using FadeIn(shift=UP*0.5). After each layer appears, show a concrete tensor flowing through it (pattern #23). Color scheme: input=GREEN_C, hidden layers=BLUE_C, attention=YELLOW_C, output=TEAL_C. The viewer builds a mental model of the data path before seeing the full picture.

Template: BUILD_UP. Use when introducing any new architecture for the first time.

### ML-2: Forward/Backward Pass Overlay
Show the forward pass with WHITE arrows. After the loss is computed, overlay RED dashed arrows flowing backward through the same path. Both remain on screen simultaneously so the viewer sees that backprop reuses the same topology. Use DIM_OPACITY=0.1 on forward arrows while explaining backward.

Template: FULL_CENTER or TOP_PERSISTENT_BOTTOM_CONTENT. Use when explaining backpropagation or gradient checkpointing.

### ML-3: Loss Landscape Surface
ThreeDScene with a Surface colored by height using set_fill_by_value with colorscale [(BLUE, low), (YELLOW, mid), (RED, high)]. Animate a Dot3D rolling down a gradient descent path via ValueTracker. Show the saddle points and local minima explicitly as labeled Dot3D objects.

Template: FULL_CENTER. Use when explaining optimization, learning rate schedules, or second-order methods.

### ML-4: Attention Weight Animation
Render a token sequence as a row of labeled boxes. For each query token, animate connection lines to all key tokens where line opacity encodes attention weight. The softmax normalization step is shown as a color sweep across the key tokens. Triangular masking is shown by graying out future-token cells before the sweep.

Template: DUAL_PANEL (tokens left, attention matrix right). Use for transformer attention, cross-attention, or any attention variant.

### ML-5: Training Dynamics with Live Counters
Axes for loss + a second y-axis for accuracy. Animate both curves drawing simultaneously with Create(rate_func=linear). Add a ValueTracker for epoch number; display it as an Integer mobject in the corner. When overfitting occurs, highlight the divergence region with a yellow Rectangle fill behind the curves.

Template: CHART_FOCUS. Use for any results section showing training stability or convergence.

## Color Semantics

```python
ML_COLORS = {
    "input":      GREEN_C,    # input data, embeddings, raw tensors
    "encoder":    BLUE_C,     # encoding / feature extraction layers
    "decoder":    PURPLE_C,   # decoding / generation layers
    "attention":  YELLOW_C,   # attention weights, focus
    "loss":       RED_C,      # loss values, errors, gradients flowing back
    "output":     TEAL_C,     # predictions, logits, output distributions
    "correct":    GREEN_D,    # ground truth, target labels
    "wrong":      RED_D,      # incorrect predictions
    "highlight":  PURE_YELLOW,# current focus point (one thing at a time)
    "dim":        GRAY,       # inactive / explained-already elements
}
```

Gradient direction: BLUE for positive weights, RED for negative. Never swap these within a video.

## Notation Conventions

- Weight matrices: uppercase bold LaTeX, e.g. `\mathbf{W}_Q`, `\mathbf{W}_K`
- Activation vectors: lowercase bold, e.g. `\mathbf{x}`, `\mathbf{h}`
- Scalars: lowercase italic, e.g. `d_k`, `n`, `T`
- Loss: always `\mathcal{L}` (calligraphic), never plain `L`
- Softmax argument: `z_i` for logit, `\hat{y}_i` for probability
- Dimensions: always annotate tensor shapes next to the array, e.g. `[B, T, d]` as a GRAY_B subscript label below each matrix

## Equation Presentation Order

1. Show the architecture diagram (what the model looks like)
2. Show data flowing forward through it (concrete tensor values)
3. Introduce the loss function (what we are minimizing)
4. Show the gradient (how the loss signals back)
5. Show the weight update rule (the final parameter change)

Never introduce the loss before the viewer has seen data flow forward. The loss is meaningless without the forward pass context.

## Common Explanation Mistakes

- **Static architecture**: showing the diagram but no data flowing through it. Fix: always animate a concrete input vector through at least one layer before explaining any component in depth.
- **Backprop without chain rule**: explaining "gradients flow backward" without showing the product of local Jacobians. Fix: use pattern ML-2 and show the actual d(loss)/d(layer_output) at each stage.
- **Attention without the query/key geometry**: saying "it computes similarity" without showing the dot product between two vectors. Fix: always show two concrete vectors before the heatmap.
- **Loss curve with no epoch labels**: viewers cannot tell if convergence took 10 or 10,000 steps. Fix: always show epoch numbers on the x-axis with at least 3 tick labels.
- **Too many layers at once**: revealing a 12-layer transformer all at once. Fix: show 2-3 layers, add "..." indicators, then focus on one representative layer.

## Scene Skeleton Recommendations

```
Scene 1 (Hook): Show the final result -- accuracy number, generated output, or key figure from paper
Scene 2 (Problem): Animated failure case of baseline method (pattern #18 Absurdist Counterexample)
Scene 3 (Background): Architecture diagram built layer by layer (pattern ML-1)
Scene 4 (Forward Pass): Concrete tensor flowing through the architecture (pattern #23 Live Pipeline)
Scene 5 (Key Contribution): The novel component introduced in isolation, then integrated into full pipeline
Scene 6 (Loss + Training): Loss landscape or training curves (pattern ML-5)
Scene 7 (Results): Side-by-side comparison with baseline (pattern #10), bar chart of metrics
Scene 8 (Takeaway): One-sentence summary card (pattern #22)
```
