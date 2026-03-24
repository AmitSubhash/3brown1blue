---
name: Physics Domain Rules
description: Visual vocabulary, preferred templates, notation, and patterns for physics paper explainers
tags: [manim, domain, physics]
---

# Physics Explainer Rules

## Visual Vocabulary

Viewers of physics explainers expect these diagram types. Without them the video feels like a textbook, not an explanation:

- **Free body diagrams**: object with labeled force arrows radiating outward, Newton's 3rd law pairs
- **Vector fields**: ArrowVectorField or StreamLines showing how a quantity varies in space
- **Wave propagation**: ParametricFunction with ValueTracker for time, showing moving wavefronts
- **Phase space trajectories**: axes labeled by position and momentum/velocity, orbits traced out
- **Energy level diagrams**: horizontal lines at different heights, arrows showing transitions
- **Conservation law visualizations**: two quantities summing to a constant, shown as a partition
- **Experimental setup**: labeled schematic of the apparatus, showing what is measured where

## Preferred Layout Templates

| Concept | Template | Reason |
|---|---|---|
| Single phenomenon demonstration | FULL_CENTER | The animation IS the content |
| Before-vs-after or two models | DUAL_PANEL | Direct visual comparison |
| Experimental setup + equations | TOP_PERSISTENT_BOTTOM_CONTENT | Setup stays visible while math builds |
| Building a model step by step | BUILD_UP | Conservation law + boundary condition + solution |
| Parameter sweep (frequency, amplitude) | CHART_FOCUS | Axes show the effect of changing conditions |
| Multiple conservation laws | GRID_CARDS | Each law in its own panel |

## Domain-Specific Visual Patterns

### PHYS-1: Phenomenon-First Introduction
Before any equation appears, animate what actually happens: show the wave moving, the ball falling, the field lines bending. Use a ValueTracker for time and always_redraw for the physical system. Only AFTER the viewer has watched the phenomenon for at least 3 seconds do you introduce the variable names and equations. This is the physics analog of Principle #1 (Geometry Before Algebra).

Template: FULL_CENTER. Always use as the first scene for any new physical effect.

### PHYS-2: Free Body Diagram Build
Start with just the object (a circle or rectangle). Add each force arrow one at a time with GrowArrow, labeling it immediately with the force name and formula. The net force vector appears last in YELLOW, as the vector sum of all individual forces. Then write Newton's second law below the diagram, coloring each term to match its corresponding arrow.

Template: FULL_CENTER. Use when introducing equations of motion or equilibrium conditions.

### PHYS-3: Field Line Animation
Use ArrowVectorField with a lambda function for the field. Show static arrows first (FadeIn with LaggedStart). Then switch to StreamLines with start_animation(warm_up=True) to show flow direction. When a parameter changes (e.g., charge magnitude via ValueTracker), update the field lambda so the arrows deform continuously. Always show a legend for field direction and magnitude.

Template: FULL_CENTER. Use for electromagnetic fields, fluid flow, gravitational fields, or any vector quantity varying in space.

### PHYS-4: Conservation Law Partition
Draw a horizontal bar or rectangle. Split it into two colored regions. Use a ValueTracker to animate the boundary between regions as the system evolves (e.g., KE growing as PE shrinks). Label each region with the quantity name and its current value (DecimalNumber with always_redraw). The total bar width stays constant -- the viewer watches energy "move" between forms.

Template: CHART_FOCUS or FULL_CENTER. Use for energy conservation, momentum conservation, or any conserved partition.

### PHYS-5: Phase Space Orbit
Create axes with position on x and momentum/velocity on y. Animate a Dot moving along the trajectory (TracedPath so the orbit accumulates). For periodic systems, the viewer watches the closed orbit form. For chaotic systems, the trace never closes. Always show the real-space trajectory (object moving) simultaneously in a DUAL_PANEL alongside the phase space, linked by a single ValueTracker.

Template: DUAL_PANEL (real space left, phase space right). Use for oscillators, pendulums, or any Hamiltonian system.

## Color Semantics

```python
PHYS_COLORS = {
    "field":        BLUE_C,     # fields, potentials, forces from environment
    "object":       WHITE,      # the physical object under study
    "force":        YELLOW_C,   # force vectors, applied quantities
    "net_force":    PURE_YELLOW,# net/resultant vector (always distinct)
    "wave":         TEAL_C,     # wavefronts, oscillations, signal propagation
    "energy_ke":    RED_C,      # kinetic energy (motion, heat)
    "energy_pe":    BLUE_C,     # potential energy (stored, elevated)
    "source":       RED_D,      # sources, charges, emitters
    "detector":     GREEN_C,    # detectors, receivers, measurement points
    "boundary":     GRAY_B,     # boundaries, interfaces, surfaces
}
```

Force arrows: use tip-to-tail vector addition with arrows drawn thick (stroke_width=4). The resultant always in PURE_YELLOW.

## Notation Conventions

- Vectors: always with arrows `\vec{F}` or bold `\mathbf{F}` -- never plain `F` for a vector quantity
- Units: always shown in brackets after a quantity when first introduced, e.g. `v \; [\text{m/s}]`
- Partial derivatives: `\partial` notation, never `d` for partial
- Magnitude vs vector: `|\vec{F}|` or `F` (italic, no arrow) -- make the distinction explicit on screen
- Subscripts: define every subscript the first time (e.g. `\vec{F}_{net}`, label "net = sum of all forces")
- Constants: `c`, `g`, `G`, `\hbar` should be introduced with a Brace + value the first time they appear

## Equation Presentation Order

1. Show the phenomenon animating in real time (PHYS-1: at least 3 seconds)
2. Identify and name the physical quantities involved (label the diagram)
3. Write the conservation law or symmetry principle that governs the system
4. Draw the free body diagram or field diagram (PHYS-2 or PHYS-3)
5. Write the equation of motion or field equation
6. Solve for the special case shown in step 1 (verify numbers match the animation)
7. Sweep a parameter to show generalization (PHYS-4 or PHYS-5)

Never start with the equation. Equations in physics ARE the model, and a model without a phenomenon to describe is meaningless to the viewer.

## Common Explanation Mistakes

- **Starting with the equation**: writing F = ma before showing anything moving. Fix: always show the phenomenon first for 3+ seconds (PHYS-1).
- **Force arrows without vector addition**: showing individual forces but never the resultant. Fix: always add GrowArrow for the net force vector as the final step in any free body diagram.
- **Wave animation without the oscillation visible**: a static snapshot of a wave. Fix: always use a ValueTracker for time and always_redraw so the wave moves.
- **Field lines without a source**: showing field arrows without indicating where they come from. Fix: always show the source object (charge, mass, antenna) at the origin or boundary.
- **Ignoring units**: writing v = 30 with no units. Fix: annotate units as a GRAY_B subscript the first time each numerical value appears.

## Scene Skeleton Recommendations

```
Scene 1 (Hook): The phenomenon animating -- no equations, no labels, just the effect
Scene 2 (Variables): Label what is being measured (FadeIn labels onto the animation)
Scene 3 (Physical Intuition): Conservation law or symmetry that constrains the system
Scene 4 (Model): Free body diagram / field diagram with all forces/sources labeled
Scene 5 (Equation): Write and decompose the governing equation (MATH-2 style)
Scene 6 (Solve): Animate the solution process for the case shown in Scene 1
Scene 7 (Generalization): Parameter sweep showing how behavior changes with conditions
Scene 8 (Takeaway): What the law predicts and where it breaks down
```
