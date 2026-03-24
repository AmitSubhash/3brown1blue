---
name: Biology Domain Rules
description: Visual vocabulary, preferred templates, notation, and patterns for biology paper explainers
tags: [manim, domain, biology]
---

# Biology Explainer Rules

## Visual Vocabulary

Viewers of biology explainers expect these diagram types. They ground abstract molecular events in visible, spatial reality:

- **Scale transition diagrams**: organism -> organ -> tissue -> cell -> molecule, with zoom indicators
- **Pathway charts**: metabolic or signaling pathways as directed graphs with node states
- **Structure-function diagrams**: protein or organelle shape annotated with what each region does
- **Population dynamics plots**: time series showing growth, competition, or predator-prey cycles
- **Phylogenetic trees**: branching diagrams with labeled nodes and branch lengths
- **Experimental flowcharts**: cell culture, treatment, assay as a BUILD_UP pipeline
- **Before/after state**: healthy vs diseased tissue, treated vs untreated condition

## Preferred Layout Templates

| Concept | Template | Reason |
|---|---|---|
| Single molecular structure | FULL_CENTER | 3D structure needs all available space |
| Healthy vs diseased state | DUAL_PANEL | Side-by-side state comparison |
| Pathway with expanding detail | TOP_PERSISTENT_BOTTOM_CONTENT | Full pathway at top; zoom into one step |
| Signaling cascade | BUILD_UP | Events happen sequentially in time |
| Population dynamics or dose-response | CHART_FOCUS | Time-series data is the main content |
| Multiple phenotypes or conditions | GRID_CARDS | Each condition in its own panel |

## Domain-Specific Visual Patterns

### BIO-1: Scale Transition Zoom
Use MovingCameraScene to zoom from organism scale down to molecular scale. At each scale level, pause and label what the viewer is seeing. Draw connecting indicators (dashed box) showing which region is being magnified. The zoom path should follow a biological hierarchy: organism -> organ -> tissue -> cell -> organelle -> molecule. Never skip more than two levels in one zoom.

Template: FULL_CENTER with camera movement. Use at the opening of any paper that works at the molecular or cellular level.

### BIO-2: Pathway State Animation
Draw pathway nodes as circles with text labels. Arrows indicate reactions or activation. Use color to encode state: active=GREEN, inactive=GRAY, inhibited=RED. Animate activation by changing a node's fill color from GRAY to GREEN (Transform or animate.set_fill). When a cascade activates, use LaggedStart so each downstream node lights up after the upstream one, with a 0.3s lag per step. Show concentration levels as a small bar inside each node.

Template: BUILD_UP. Use for MAPK cascades, apoptosis pathways, immune activation, or any signaling sequence.

### BIO-3: Structure-Function Annotation
FadeIn the structure (protein domain layout, membrane cross-section, cell diagram) as a complete shape. Then highlight each functional region one at a time with a SurroundingRectangle in YELLOW, add a Brace with a label, explain it, then color that region its semantic color before moving on. This is MATH-2 applied to structure instead of equation. Keep the structure visible throughout -- only the highlighting moves.

Template: FULL_CENTER with persistent skeleton (principle #15). Use for protein domain papers, membrane biology, or organelle function.

### BIO-4: Population Dynamics with Threshold
Axes with time on x and population/concentration on y. Plot multiple curves (e.g., predator + prey) simultaneously, color-coded. Use a horizontal DashedLine to show carrying capacity or viability threshold. When a curve crosses the threshold, flash it in RED (Indicate animation). Animate curves drawing with Create(rate_func=linear) and a shared ValueTracker for time so both curves advance together.

Template: CHART_FOCUS. Use for ecology papers, tumor growth models, drug pharmacokinetics, or evolutionary dynamics.

### BIO-5: Experimental Pipeline with Sample State
Show the experimental procedure as a pipeline (BUILD_UP): sample collection -> treatment -> assay -> readout. At each stage, include a small inset showing what the sample looks like (e.g., a circle with colored dots for cells, a heatmap for gene expression). This grounds the abstract procedure in physical reality. Each stage's inset updates to show the transformation the treatment caused.

Template: TOP_PERSISTENT_BOTTOM_CONTENT (pipeline at top) or BUILD_UP. Use whenever presenting an experimental method section.

## Color Semantics

```python
BIO_COLORS = {
    "active":       GREEN_C,    # active, healthy, growing, expressed
    "inactive":     GRAY_B,     # inactive, dormant, unexpressed
    "inhibited":    RED_D,      # inhibited, diseased, suppressed
    "signal":       YELLOW_C,   # signaling molecule, ligand, activator
    "inhibitor":    RED_C,      # inhibitor, blocker, antagonist
    "structure":    BLUE_C,     # protein/organelle structure (neutral)
    "membrane":     TEAL_C,     # lipid bilayers, membranes, barriers
    "nucleus":      PURPLE_C,   # nuclear material, DNA, chromatin
    "fluid":        BLUE_A,     # water, cytoplasm, interstitial fluid
    "annotation":   GRAY_B,     # scale bars, labels, reference lines
}
```

The green=healthy / red=disease semantic is so strong in biology that violating it will confuse viewers who have domain knowledge. Never use red for "active" or green for "inhibited."

## Notation Conventions

- Gene names: italicized, all caps for human genes, e.g. `\textit{BRCA1}` -- make this explicit on screen
- Protein names: Roman (not italic), e.g. `\text{BRCA1 protein}`
- Concentrations: `[\text{Ca}^{2+}]` with square brackets and units `\mu\text{M}` or `\text{nM}` shown
- Arrows in pathways: `\rightarrow` for activation, `\dashv` (or a flat-headed arrow) for inhibition
- P-values: always show `p < 0.05` or exact value; never just "significant"
- Scale bars: always include a scale bar annotation on any spatial diagram (BIO-1 zoom diagrams especially)

## Equation Presentation Order

1. Show the biological phenomenon (what does the cell/organism do?)
2. Show the structure involved (BIO-1 scale transition or BIO-3 structure annotation)
3. Introduce the molecular players (label each component)
4. Animate the sequence of events (BIO-2 pathway animation)
5. Show the quantitative readout (BIO-4 dynamics or bar chart of experimental results)
6. Write any mathematical model last, grounded in the pathway already shown

Biology viewers are often more comfortable with diagrams than equations. Reserve equations for quantitative biology papers; in cell/molecular biology, pathway diagrams carry more explanatory weight than formulas.

## Common Explanation Mistakes

- **Molecule soup**: showing all pathway components at once without activation sequence. Fix: use BIO-2 with LaggedStart -- each component appears only when it is activated.
- **Scale confusion**: jumping from organism to molecule without a transition. Fix: always use BIO-1 zoom with intermediate scale stops.
- **Static experimental flowchart**: a pipeline with no indication of what the sample looks like at each step. Fix: add small insets showing sample state (BIO-5).
- **Color overload**: using 6+ colors in a pathway diagram. Fix: reserve semantic colors (green=active, red=inhibited, gray=inactive) and color everything else BLUE_C.
- **No healthy baseline**: only showing the disease state. Fix: always start with the healthy/normal state using DUAL_PANEL before introducing pathology.

## Scene Skeleton Recommendations

```
Scene 1 (Hook): The biological effect -- what changes, grows, or fails (macro scale)
Scene 2 (Scale): Zoom from organism to the relevant scale (BIO-1)
Scene 3 (Players): Introduce the molecular/cellular actors and label them (BIO-3)
Scene 4 (Mechanism): Animate the sequence of events (BIO-2 pathway)
Scene 5 (Experiment): Show how the authors measured this (BIO-5 pipeline)
Scene 6 (Results): Quantitative outcome -- bar chart, curves, or microscopy images
Scene 7 (Implication): What does this change about our understanding or treatment?
Scene 8 (Takeaway): One-sentence mechanism summary
```
