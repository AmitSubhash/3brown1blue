---
name: Neuroscience Domain Rules
description: Visual vocabulary, preferred templates, notation, and patterns for neuroscience paper explainers
tags: [manim, domain, neuroscience]
---

# Neuroscience Explainer Rules

## Visual Vocabulary

Viewers of neuroscience explainers expect these diagram types. They anchor abstract computations in physical anatomy:

- **Brain anatomy overlays**: lateral or coronal view with regions highlighted by color
- **Neural signal traces**: time-series voltage or fluorescence traces, multiple channels overlaid
- **Imaging modality diagrams**: fNIRS optodes on scalp, EEG electrode caps, fMRI BOLD sequences
- **Connectivity matrices**: N x N heatmap where cell intensity encodes connection strength
- **Receptive field maps**: 2D spatial maps showing which inputs drive a neuron
- **Population tuning curves**: response amplitude vs stimulus feature (orientation, frequency)
- **Spike rasters**: dots on a time axis per trial/neuron, revealing firing patterns

## Preferred Layout Templates

| Concept | Template | Reason |
|---|---|---|
| Brain anatomy + highlighted region | FULL_CENTER | Brain image needs most of the frame |
| Signal recording + analysis result | DUAL_PANEL | Raw trace left, processed result right |
| Imaging setup + signal traces | TOP_PERSISTENT_BOTTOM_CONTENT | Setup stays; traces appear below |
| Signal processing pipeline | BUILD_UP | Filter -> feature -> decode builds step by step |
| Population-level tuning curves | CHART_FOCUS | The curve shape IS the finding |
| Multiple brain regions or conditions | GRID_CARDS | One region/condition per card |

## Domain-Specific Visual Patterns

### NEURO-1: Anatomy-First Grounding
Open every scene involving a brain region by showing the full brain outline first (a simplified SVG or custom Polygon path). Then use a SurroundingRectangle or colored Region to highlight the area of interest. FadeIn a label with an arrow pointing to it. Zoom in (MovingCameraScene) to that region before showing any signals or recordings. This establishes spatial context before signals appear. Never show a trace without first showing WHERE in the brain it came from.

Template: FULL_CENTER with camera zoom. Required as the opening of any scene introducing a new brain region.

### NEURO-2: Multi-Channel Signal Trace
Create multiple Axes vertically stacked (y-offset by 1.5 per channel), all sharing the same x-axis (time). Plot each channel's trace as a ParametricFunction drawn with Create(rate_func=linear). Color traces by channel type (LFP=BLUE_C, spike=YELLOW_C, EMG=GREEN_C, artifact=GRAY_B). Use a shared ValueTracker for a time cursor -- a vertical DashedLine that sweeps across all channels simultaneously. When an event occurs, flash all channels in YELLOW at that time.

Template: CHART_FOCUS. Use for any paper showing electrophysiology, calcium imaging, or optical recording data.

### NEURO-3: Imaging Modality Setup
Draw the experimental setup as a spatial diagram: scalp/skull cross-section for fNIRS/EEG, or a head inside an MRI bore for fMRI. For fNIRS, show optodes as RED (source) and BLUE (detector) dots on the scalp surface with curved banana-shaped sensitivity paths between them. For EEG, show electrode positions on a circular head outline. For fMRI, show the BOLD signal as a heat-map overlay on a brain slice. Always label the modality name prominently.

Template: FULL_CENTER or DUAL_PANEL (setup left, signal right). Use when introducing any recording modality for the first time.

### NEURO-4: Connectivity Matrix Animation
Draw an N x N grid using pattern #25 (Heatmap Grid). Rows and columns are labeled with region names. Reveal with LaggedStart(FadeIn, lag_ratio=0.01) for a sweep effect. Then animate a specific finding: highlight a cell or row with SurroundingRectangle in YELLOW and zoom in. For directed connectivity, use triangular asymmetry -- show upper vs lower triangle separately with arrows indicating direction.

Template: FULL_CENTER or GRID_CARDS. Use for functional connectivity, structural connectome, or any correlation matrix.

### NEURO-5: Population Code Visualization
Show N neuron responses as N small bar charts or tuning curves arranged in a GRID_CARDS layout. When a stimulus changes (driven by a ValueTracker), all N curves update simultaneously via always_redraw. Highlight the "most tuned" neuron in YELLOW. Then show the population vector (weighted sum) as a single arrow whose direction updates as the stimulus changes. This demonstrates that the population encodes information the single neuron does not.

Template: GRID_CARDS (individual tuning) with a FULL_CENTER inset for the population vector. Use for population coding, neural decoding, or dimensionality reduction results.

## Color Semantics

```python
NEURO_COLORS = {
    "excitatory":   BLUE_C,     # excitatory neurons, positive BOLD, activation
    "inhibitory":   RED_C,      # inhibitory neurons, suppression, deactivation
    "signal_lfp":   BLUE_C,     # local field potential
    "signal_spike": YELLOW_C,   # single-unit spikes, action potentials
    "signal_bold":  RED_D,      # fMRI BOLD signal (oxygenated hemoglobin)
    "source_fnirs": RED_C,      # fNIRS light source (emitter)
    "detector_fnirs": BLUE_C,   # fNIRS detector (receiver)
    "highlight":    PURE_YELLOW,# the neuron/region currently being discussed
    "resting":      GRAY_B,     # baseline, resting state, unexplained variance
    "connectivity": TEAL_C,     # connectivity strength, coherence
}
```

Excitatory=blue / inhibitory=red follows the dominant convention in neuroscience figures and matches viewer expectations from textbooks. Never swap these.

## Notation Conventions

- Brain regions: standard anatomical abbreviations on screen, defined in a legend on first use (e.g., `\text{V1}`: primary visual cortex)
- Signals: `\Delta[\text{HbO}]` for fNIRS oxygenated, `\Delta[\text{HbR}]` for deoxygenated
- Spiking: `r_i(t)` for firing rate of neuron i, `s_i(t)` for spike train
- Connectivity: `W_{ij}` for weight from neuron j to neuron i (note convention direction)
- Time axes: always label in milliseconds (ms) for electrophysiology, seconds (s) for BOLD/fNIRS
- Trial-averaged vs single-trial: always indicate which is shown; never imply single-trial looks like the average

## Equation Presentation Order

1. Show the anatomy (NEURO-1: which brain region, what it does)
2. Show the recording setup (NEURO-3: how signals are measured)
3. Show raw signal traces (NEURO-2: what the data looks like before analysis)
4. Introduce the analysis step (equation or model that extracts the finding)
5. Animate the result (NEURO-4 connectivity, NEURO-5 population code, or decoded variable)
6. Relate back to anatomy (which regions showed the effect)

Neuroscience viewers trust anatomy. Ground every computational claim in a spatial claim about the brain first. A connectivity matrix without a brain diagram above it is harder to interpret than one anchored to named regions.

## Common Explanation Mistakes

- **Signals without anatomy**: showing traces or matrices without first establishing where in the brain they come from. Fix: always use NEURO-1 as the scene opener.
- **Single-channel traces for multi-channel findings**: the paper's key finding is a correlation between regions, but only one trace is shown. Fix: use NEURO-2 multi-channel stacked view.
- **Imaging modality not explained**: assuming viewers know what fNIRS is. Fix: always include NEURO-3 when introducing any imaging modality.
- **Connectivity matrix without region labels**: an unlabeled heatmap. Fix: always label rows and columns; use abbreviated but readable region names.
- **Population code shown as a single neuron**: the paper is about population decoding but only one tuning curve is shown. Fix: use NEURO-5 with at least 9 neurons in a 3x3 grid.

## Scene Skeleton Recommendations

```
Scene 1 (Hook): The behavioral result or clinical implication -- what the brain does/fails to do
Scene 2 (Anatomy): Brain diagram with the relevant region highlighted (NEURO-1)
Scene 3 (Recording): How the signals are measured (NEURO-3 imaging setup)
Scene 4 (Raw Data): What the signals look like (NEURO-2 multi-channel trace)
Scene 5 (Analysis): The computational method applied to the signals
Scene 6 (Finding): Connectivity matrix, population code, or decoded variable (NEURO-4/5)
Scene 7 (Interpretation): What the finding means for understanding brain function
Scene 8 (Takeaway): The neural computation principle demonstrated by the paper
```
