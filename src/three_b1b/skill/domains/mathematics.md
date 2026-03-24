---
name: Mathematics Domain Rules
description: Visual vocabulary, preferred templates, notation, and patterns for mathematics paper explainers
tags: [manim, domain, mathematics]
---

# Mathematics Explainer Rules

## Visual Vocabulary

Viewers of mathematics explainers expect these diagram types. Their absence signals "this is just a lecture, not an explanation":

- **Coordinate planes and number lines**: axes with labeled ticks, plotted curves, moving points
- **Geometric constructions**: triangles, circles, tangent lines, areas, chords -- drawn in the animation, not pre-rendered
- **Proof structure diagrams**: hypothesis -> step -> step -> conclusion as a vertical BUILD_UP
- **Equation morphing**: one form transforming into another while maintaining identity
- **Complex plane visualizations**: unit circle, Argand plane, roots of unity as rotating vectors
- **Function transformations**: showing f(x), then g(f(x)), then h(g(f(x))) with each layer added
- **Matrices acting on space**: 2D grid deforming under a linear transformation

## Preferred Layout Templates

| Concept | Template | Reason |
|---|---|---|
| Single theorem statement | FULL_CENTER | Equation needs the full horizontal span |
| Geometric proof | DUAL_PANEL | Left: geometry, Right: algebra that matches it |
| Multi-step derivation | BUILD_UP | Each step builds on the previous |
| Parameter sweep on a function | CHART_FOCUS | Axes are the primary anchor |
| Taxonomy of cases | GRID_CARDS | Each case is a self-contained mini-diagram |
| Running proof with persistent diagram | TOP_PERSISTENT_BOTTOM_CONTENT | Diagram stays; equations build below |

## Domain-Specific Visual Patterns

### MATH-1: Geometry-First Reveal
Draw the geometric object (curve, shape, construction) completely before writing any equation. Then, after the viewer has absorbed the shape, write the equation and use Braces + labels to connect each symbol to a feature they can already see. The geometry answers "what does this formula mean?" before the formula is even introduced.

Template: FULL_CENTER or DUAL_PANEL (geometry left, algebra right). Always use for any formula whose terms have geometric interpretations.

### MATH-2: Dim-and-Reveal Equation Decomposition
Write the full equation at full opacity. Wait 2 seconds (viewer scans). Dim everything to DIM_OPACITY. Bring each term to full opacity one at a time, color it, and attach a Brace + label. When all terms are colored, un-dim everything. The result is a color-coded equation the viewer can "read" left to right.

Template: FULL_CENTER. This is the primary pattern for any equation the viewer has not seen before. See paper-explainer.md for the full implementation.

### MATH-3: Continuous Morphing Between Representations
Use ReplacementTransform to show that two algebraic forms are the same object. The transform proves identity by showing the viewer the same pixels reconfig into the new form. Pause 1 second before and 2 seconds after the transform. Use this for: factoring, completing the square, changing bases, Fourier representations.

Template: FULL_CENTER. Never use a static "therefore" arrow -- always morph.

### MATH-4: Proof Step Counter
Place a VGroup of small numbered circles on the left margin (y-positions spaced 1.2 apart). As each proof step is established, highlight the corresponding circle in YELLOW and write the step's key equation to its right. Circles below the current step remain DIM_OPACITY. This gives the viewer a persistent proof map -- they always know how far through the argument they are.

Template: BUILD_UP with the step counter as the persistent skeleton (principle #15).

### MATH-5: Parametric Animation with Traced Path
Use ParametricFunction driven by a ValueTracker. Add a TracedPath attached to the moving point so the viewer sees the full curve materialize as the parameter sweeps. Label the initial and terminal points. This is essential for polar curves, Lissajous figures, cycloids, and any curve defined parametrically.

Template: FULL_CENTER or CHART_FOCUS. Use whenever a curve is "traced out" rather than appearing all at once.

## Color Semantics

```python
MATH_COLORS = {
    "primary_curve":  BLUE_C,     # the main function being studied
    "secondary_curve": RED_C,     # comparison, inverse, or derivative
    "highlight":      YELLOW_C,   # current point of focus, dot on curve
    "geometry":       TEAL_C,     # geometric constructions (triangles, chords)
    "proof_done":     GREEN_C,    # established / already proved terms
    "unknown":        GRAY_B,     # terms not yet explained
    "emphasis":       PURE_YELLOW,# the one thing the viewer must not miss
    "axis":           GRAY,       # axes, grid lines (background)
}
```

One consistent rule: once a term is explained and colored, it keeps that color for the rest of the video. The color history IS the learning history.

## Notation Conventions

- Vectors: bold lowercase `\mathbf{v}` or with arrows `\vec{v}` -- pick one and use it throughout
- Matrices: uppercase bold `\mathbf{A}`, never plain `A` for a matrix
- Sets: calligraphic `\mathcal{F}`, `\mathcal{H}` for function spaces
- Norms: `\|\mathbf{v}\|` with double vertical bars, not single
- Big O: `\mathcal{O}(n)` not `O(n)`
- Implication arrows in proofs: `\Rightarrow` for logical implication, `\implies` for "it follows"
- Annotate every subscript the first time it appears: never assume the viewer knows what `n`, `k`, or `\lambda` means in your context

## Equation Presentation Order

1. State the phenomenon geometrically (draw it)
2. Ask the question verbally (pattern #15 Question Frame)
3. Introduce the simplest special case first (concrete numbers, pattern #10)
4. Write the general form and immediately point back to the special case
5. Prove or derive the formula (BUILD_UP, one step per beat)
6. Show consequences / applications (transform back to geometry)

The cardinal rule: the GEOMETRY comes before the ALGEBRA. A viewer who understands the shape can verify the formula. A viewer who only sees the formula cannot reconstruct the shape.

## Common Explanation Mistakes

- **Algebra without geometry**: writing a chain of equalities with no visual anchor. Fix: at each step, update the geometric diagram to reflect what the algebra just said.
- **Proofs by "clearly"**: skipping a step the presenter finds obvious. Fix: every step gets its own Beat -- if it takes less than 2 seconds to justify, add a visual that shows why it's true.
- **Morphing too fast**: ReplacementTransform at run_time=0.5 so viewers cannot follow what moved where. Fix: minimum 1.5s for any equation transform, pause 2s after.
- **Axes without labels**: plotting a curve on unlabeled axes. Fix: always show axis labels, at minimum f(x) and x, before plotting.
- **Showing the full proof before explaining any of it**: a 6-line proof appearing all at once. Fix: always use Dim-and-Reveal (MATH-2) or Proof Step Counter (MATH-4).

## Scene Skeleton Recommendations

```
Scene 1 (Hook): Show the surprising visual result (the curve, the construction, the equality)
Scene 2 (Motivation): Why does this matter? What would be hard without this theorem?
Scene 3 (Special Case): Work the simplest concrete example (n=2, unit circle, integer coefficients)
Scene 4 (Geometry): Build the geometric picture that makes the proof obvious
Scene 5 (Proof): Step-by-step derivation with persistent diagram (pattern MATH-4)
Scene 6 (Generalization): Extend to the full statement; morph the special case into general form
Scene 7 (Applications): Two or three applications animated quickly (GRID_CARDS)
Scene 8 (Takeaway): One-sentence summary of what was proved and why it matters
```
