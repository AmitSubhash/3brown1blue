---
name: Visual Design Pattern Catalog
description: 35 concrete visualization patterns from 3Blue1Brown frame analysis -- implementable recipes for Manim scenes
tags: [manim, patterns, 3b1b, catalog, visualization, recipes]
---

# Visual Design Pattern Catalog

Patterns 1 to 26 from 422 frames across 3 videos (NN Ch2, Transformer Ch6, MLP Ch8).
Patterns 27 to 35 from Grant Sanderson's talk "Designing Math" (Config 2026).
Each pattern: name, description, one code snippet.

---

## Data Display Patterns

### 1. Probability Distribution Sidebar

Right-aligned vertical word list with proportional inline bars and percentages. The sampled token gets a yellow border highlight. Reads like a ranked leaderboard.

```python
for word, prob in [("for", 0.69), ("as", 0.22), ("or", 0.02)]:
    label = Text(word, font_size=24).align_to(anchor, RIGHT)
    bar = Rectangle(width=prob * 5, height=0.25,
                    fill_color=interpolate_color(TEAL, GREEN, prob), fill_opacity=0.8)
```

### 2. Per-Number Sign Coloring

Color every individual number inside a matrix by its sign: positive in teal, negative in red. Creates a heatmap effect that communicates polarity distribution at a glance without reading values.

```python
for entry in matrix_entries:
    val = float(entry.get_tex_string())
    entry.set_color(TEAL if val > 0 else RED)
```

### 3. Running Counters

Real-time updating accuracy or loss numbers that change as examples flow through the system. Gives viewers a sense of progress rather than a static final result.

```python
correct, total = ValueTracker(0), ValueTracker(0)
counter = always_redraw(lambda: MathTex(
    rf"{int(correct.get_value())}/{int(total.get_value())} = "
    rf"{correct.get_value()/max(total.get_value(),1):.3f}"
).to_corner(UR))
```

### 4. Attention Heatmap Table

Matrix where rows are key tokens, columns are query tokens, and cell shading intensity encodes attention weight. Triangular masking (future tokens = dark) is immediately visible as a pattern.

```python
for i, row in enumerate(tokens):
    for j, col in enumerate(tokens):
        weight = attention_weights[i][j]
        cell = Circle(radius=0.15, fill_opacity=weight, fill_color=WHITE)
        cell.move_to(table_pos(i, j))
```

### 5. Vertical Number Line Display

Place dot-product results at their numeric position on a vertical axis. Words cluster spatially by semantic similarity. Position alone communicates value -- no bars needed.

```python
number_line = NumberLine(x_range=[-4, 4], length=6, rotation=PI/2)
for word, val in [("cats", 1.8), ("student", -1.1)]:
    dot = Dot(number_line.n2p(val), color=YELLOW)
    label = Text(word, font_size=20).next_to(dot, RIGHT)
```

---

## Architecture Visualization

### 6. 3D Transparent Box as Process Container

Render a multi-step process (e.g., Linear -> ReLU -> Linear) inside a semi-transparent 3D box. Front face is fully transparent so internals are visible. Label sits above, not inside.

```python
box = Prism(dimensions=[8, 3, 2], fill_opacity=0.1, stroke_color=WHITE)
label = Text("MLP").next_to(box, UP)
# Place pipeline elements as children inside box
```

### 7. Skip Connection as Yellow Bypass Arc

Show residual connections as a bright yellow arc that goes OVER the process box, terminating at a circled-plus operator. Spatial separation (over vs through) makes the two data paths unmistakable.

```python
skip_arc = ArcBetweenPoints(
    input_vec.get_top(), plus_sign.get_top(),
    angle=-0.5, color=YELLOW, stroke_width=3)
plus_sign = MathTex(r"\oplus", color=YELLOW)
```

### 8. Exploded Parallel Instance View

Show that an operation applies to every token by "exploding" a single instance into N copies stacked in 3D depth. Yellow lines across instances indicate shared weights.

```python
instances = VGroup(*[
    mlp_box.copy().shift(i * 0.4 * OUT + i * 0.3 * DOWN)
    for i in range(n_tokens)
])
```

### 9. Concrete Pipeline (Input -> Process -> Output)

Left: concrete input with real numbers. Center: labeled process box. Right: concrete output with real numbers and proportional bars. The viewer can verify the math.

```python
input_vec = Matrix([[0.34], [0.92], [0.16]])
box = Rectangle(width=2, height=1.5).add(Text("softmax"))
output_bars = VGroup(*[Rectangle(width=p*3, height=0.25,
    fill_color=BLUE, fill_opacity=0.8) for p in [0.01, 0.61, 0.25]])
```

---

## Layout and Composition

### 10. Side-by-Side Comparison

Two COMPLETE examples (same structure, different values) visible simultaneously. Same layout on both sides so the viewer's eye naturally diffs left vs right.

```python
left_panel = build_distribution(temp=0).to_edge(LEFT)
right_panel = build_distribution(temp=5).to_edge(RIGHT)
divider = Line(UP * 3, DOWN * 3, color=GREY, stroke_opacity=0.3)
```

### 11. Progressive Grid Fill

Build a gallery of peer visualizations one cell at a time (e.g., what each neuron learns). Don't show all at once -- fill a grid element by element so the pattern emerges across instances.

```python
for i, (r, c) in enumerate([(r, c) for r in range(4) for c in range(4)]):
    cell = create_weight_heatmap(neuron_index=i)
    cell.move_to([c * 1.5 - 2.25, -r * 1.5 + 2.25, 0])
    self.play(FadeIn(cell), run_time=0.5)
```

### 12. Multi-Scale Zoom

Drill down through layers of a system: architecture -> block -> vector -> scalar. Each zoom level maintains visual echoes of the level above so context is never lost.

```python
# Zoom sequence: full pipeline visible, highlight one block
self.play(FocusOn(block_2), block_2.animate.scale(2).move_to(ORIGIN),
          *[b.animate.set_opacity(0.2) for b in other_blocks])
# Then zoom further into a single vector within that block
```

### 13. Four-Quadrant Summary Frame

2x2 grid where each quadrant contains a miniaturized key concept from the video. Each cell is a complete mini-scene with its own labels, axes, and data. Used as a visual recap near the end.

```python
quadrants = VGroup(*[build_mini_scene(topic).scale(0.42)
                     for topic in ["Embedding", "Attention", "Dot Product", "MatMul"]])
quadrants.arrange_in_grid(rows=2, cols=2, buff=0.4)
```

### 14. Title/Concept Decomposition

Split a multi-word concept across the screen. Highlight one word at a time (yellow) while others go gray. Below each highlighted word, show a concrete visual example.

```python
words = VGroup(*[Text(w, font_size=64) for w in
                 ["Generative", "Pre-trained", "Transformer"]])
words.arrange(RIGHT, buff=1.5).to_edge(UP)
# Animate: set focused word YELLOW, others GREY_D
```

---

## Pedagogical Devices

### 15. Question Frame

Pose a question on screen for 2-3 seconds before showing the answer. Creates micro-suspense where the viewer actively predicts. Place the question in yellow near the relevant visual.

```python
question = Text("Which direction decreases C(x,y)\nmost quickly?",
                font_size=28, color=YELLOW)
self.play(Write(question)); self.wait(2)
self.play(FadeOut(question), GrowArrow(gradient_arrow))
```

### 16. Truth vs Convenient Lie

Split frame horizontally. Top: "The Truth" with the accurate version. Bottom: "A Convenient Lie" with the simplified version. Both show the same content so the simplification is explicit.

```python
divider = Line(LEFT * 6, RIGHT * 6, color=WHITE)
truth_label = Text("The Truth", font_size=32).next_to(divider, UP, buff=1.5)
lie_label = Text("A Convenient Lie", font_size=28).next_to(divider, DOWN, buff=1.5)
```

### 17. Cloud of Unknown

Use an amorphous gray blob as a visual placeholder for concepts that resist visualization (e.g., 12,288-dimensional space). Gradually replace the cloud with partial views as understanding builds.

```python
cloud = SVGMobject("cloud.svg", fill_color=GREY, fill_opacity=0.4).scale(3)
label = Text("12,288-dim\nSpace", color=YELLOW, font_size=28)
label.next_to(cloud, LEFT)
```

### 18. Absurdist Counterexample

After showing a system working correctly, immediately feed it an adversarial input (random noise, out-of-distribution image). The contrast between "96% accuracy" and "thinks noise is a 5" is more instructive than either alone.

```python
noise_image = ImageMobject(np.random.rand(28, 28))
noise_image.add(SurroundingRectangle(noise_image, color=YELLOW, buff=0.05))
result_label = Text("Looks like a 5 to me!", color=YELLOW, font_size=24)
```

### 19. Strikethrough for Conceptual Revision

Show the original text with a red line through it, then place the revised text nearby. The struck-through text remains visible so the viewer sees what changed and why.

```python
old_text = MathTex(r"90^\circ", color=RED)
strike = Line(old_text.get_left(), old_text.get_right(), color=RED, stroke_width=3)
new_text = MathTex(r"89^\circ \text{ to } 91^\circ", color=TEAL).next_to(old_text, UP)
```

### 20. Interactive Slider with Live Output

A parameter slider with a visible handle. As the value changes, ALL output values and bars update simultaneously. Input stays fixed while only the parameter changes.

```python
temp = ValueTracker(1.0)
slider = NumberLine(x_range=[0, 10], length=4)
handle = Triangle(fill_color=RED).scale(0.15)
handle.add_updater(lambda m: m.move_to(slider.n2p(temp.get_value()) + UP * 0.1))
```

### 21. Interpretive Piecewise Labels

Place a conditional/piecewise annotation next to a formula, translating math into English meaning. Bridges abstract notation to concrete semantics using quoted natural language.

```python
interp = MathTex(
    r"\begin{cases}\approx 1 & \text{If encodes ``Michael''} \\"
    r"\leq 0 & \text{If not}\end{cases}", font_size=24)
interp.next_to(dot_product_eq, RIGHT, buff=0.3)
```

### 22. Section Title Card

Clean transition: single centered title on pure black background, white serif text. Zero visual complexity signals "new topic." Hold for 2 seconds, then fade out.

```python
title = Text("Superposition", font="serif", font_size=56)
title.move_to(ORIGIN)
self.play(Write(title)); self.wait(2); self.play(FadeOut(title))
```

---

## Dynamic Data Patterns

### 23. Live Pipeline Data Flow

Show concrete values entering a pipeline and transforming at each stage. The viewer watches numbers change as data moves through boxes. Far more informative than a dot sliding across arrows.

```python
t = ValueTracker(0)  # progress: 0=start, 3=end

# Input values appear, then fade as they enter stage 1
input_display = always_redraw(lambda: VGroup(*[
    DecimalNumber(v, num_decimal_places=2, font_size=20,
                  color=interpolate_color(WHITE, WHITE, 0.5))
    for v in [0.34, 0.92, 0.16]
]).arrange(DOWN, buff=0.05).next_to(boxes[0], DOWN, buff=0.3).set_opacity(
    max(0, 1 - t.get_value())  # fade as data moves past
))

# Output bars grow as data reaches the end
output_bars = always_redraw(lambda: VGroup(*[
    Rectangle(width=p * 3 * min(1, max(0, t.get_value() - 2)),
              height=0.2, fill_color=BLUE, fill_opacity=0.8)
    for p in [0.87, 0.11, 0.02]
]).arrange(DOWN, buff=0.05).next_to(boxes[-1], DOWN, buff=0.3))

self.add(input_display, output_bars)
self.play(t.animate.set_value(3), run_time=6, rate_func=linear)
```

### 24. Linked Dual Panel with ValueTracker

Two views of the same data, synchronized via a shared ValueTracker. Moving one updates the other. The viewer viscerally grasps "these are the same signal in different representations."

```python
t = ValueTracker(0)

# Left: raw signal with a moving cursor
cursor = always_redraw(lambda: DashedLine(
    left_axes.c2p(t.get_value(), -3),
    left_axes.c2p(t.get_value(), 3),
    color=YELLOW, stroke_width=1.5,
))

# Right: feature values update as cursor moves
feature_bars = always_redraw(lambda: VGroup(*[
    Rectangle(width=abs(compute_feature(t.get_value(), ch)) * 2,
              height=0.25, fill_color=interpolate_color(RED, BLUE,
              compute_feature(t.get_value(), ch)),
              fill_opacity=0.8)
    for ch in range(8)
]).arrange(DOWN, buff=0.03).move_to(right_axes))

self.play(t.animate.set_value(4), run_time=6, rate_func=linear)
```

### 25. Heatmap Grid with interpolate_color

Grid of squares where fill color encodes a continuous value. More visually rich than labeled boxes. Use for sensor arrays, weight matrices, confusion matrices, or any 2D data.

```python
values = np.random.rand(8, 8)  # e.g., electrode modulation depths
grid = VGroup()
for r in range(8):
    for c in range(8):
        sq = Square(side_length=0.35, stroke_width=0.5)
        sq.set_fill(
            interpolate_color(ManimColor("#1a1a2e"), YELLOW, values[r, c]),
            opacity=0.9,
        )
        grid.add(sq)
grid.arrange_in_grid(8, 8, buff=0.02)

# Reveal with sweep effect
self.play(LaggedStart(
    *[FadeIn(sq, scale=0.8) for sq in grid],
    lag_ratio=0.01,
), run_time=2)
```

### 26. Camera Zoom Detail (MovingCameraScene)

Zoom into a specific region of a diagram while keeping the full context visible (dimmed). Essential for pipeline zoom-ins where you want to show internal structure without losing the big picture.

```python
class ZoomDetail(MovingCameraScene):
    def construct(self):
        # Build full diagram...
        full_diagram = build_pipeline()
        target_box = full_diagram[2]  # zoom into stage 3

        # Zoom in: enlarge target, dim everything else
        self.play(
            self.camera.frame.animate.set(
                width=target_box.width * 3.5
            ).move_to(target_box),
            *[m.animate.set_opacity(0.1)
              for m in full_diagram if m != target_box],
            run_time=1.5,
        )
        # Show internal detail at zoomed scale...

        # Zoom out: restore everything
        self.play(
            self.camera.frame.animate.set(width=14).move_to(ORIGIN),
            *[m.animate.set_opacity(1) for m in full_diagram],
            run_time=1.5,
        )
```

## Transformation and Explanation Patterns

From frame analysis of Grant Sanderson's "Designing Math" (Config 2026). These render the
ideas in explanation-design.md: showing a symbol's job, a series as motion, and a function as
a warping of the whole plane.

### 27. Role-Labeled Equation Boxes

Box every part of an equation at once, each in its semantic color, and label what each part
DOES in plain language. This is the visual form of "give your characters motivation": the
viewer reads the equation as a cast of actors with jobs, not as inert symbols. In the talk,
d/dt e^{it} = i * e^{it} is annotated as Velocity = (Rotate 90 degrees) * (Position).

```python
eq = MathTex(r"\frac{d}{dt} e^{it}", r"=", r"i", r"\cdot", r"e^{it}")
roles = [(0, "Velocity", YELLOW, DOWN), (2, "Rotate 90", YELLOW, UP), (4, "Position", TEAL, DOWN)]
for idx, text, color, side in roles:
    box = SurroundingRectangle(eq[idx], color=color, buff=0.08)
    label = Text(text, font_size=24, color=color).next_to(box, side, buff=0.15)
    eq[idx].set_color(color)
    self.play(Create(box), FadeIn(label, shift=side * 0.2))
```

### 28. Tip-to-Tail Vector Walk (series as a spiral)

Show a sum or series geometrically: lay each term as an arrow, tip to tail, so the running
total traces a path. For e^{i*pi} the terms spiral inward (factorial denominators shrink them)
and converge on -1, making "what does this sum look like?" literally visible. Color the path
green and label the active term in yellow.

```python
import math
plane = ComplexPlane(x_range=[-2, 2], y_range=[-1, 4]).add_coordinates()
partials = []
total = 0
for n in range(12):
    total += (1j * math.pi) ** n / math.factorial(n)
    partials.append(total)
arrows = VGroup(*[
    Arrow(plane.n2p(partials[k - 1]), plane.n2p(partials[k]),
          buff=0, color=GREEN, stroke_width=4, max_tip_length_to_length_ratio=0.2)
    for k in range(1, len(partials))
])
self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.4, run_time=6))
self.play(FadeIn(Dot(plane.n2p(-1), color=YELLOW, radius=0.08)))
```

### 29. Vector Field Reveals the Rule

When an object is defined by "velocity is some transform of position," draw the field: at
sampled points show the position vector (teal) and the velocity vector (green) as that
transform of it. The resulting motion becomes inevitable from the picture alone. Here velocity
is a 90-degree rotation of position, so every velocity is tangent to a circle.

```python
plane = NumberPlane(x_range=[-3, 3], y_range=[-2, 2])
field = VGroup()
for ang in np.linspace(0, TAU, 12, endpoint=False):
    pos = np.array([np.cos(ang), np.sin(ang), 0])
    vel = np.array([-pos[1], pos[0], 0])  # multiply by i = rotate 90 degrees
    field.add(Arrow(plane.c2p(0, 0), plane.c2p(*pos[:2]), buff=0, color=TEAL, stroke_width=3))
    field.add(Arrow(plane.c2p(*pos[:2]), plane.c2p(*(pos + vel)[:2]), buff=0,
                    color=GREEN, stroke_width=3))
self.play(LaggedStart(*[GrowArrow(a) for a in field], lag_ratio=0.05))
```

### 30. Tracer Lines Through a Transformation

To show "what does this function do to the whole plane," do not warp a bare grid: warp a
TEXTURED plane (checkerboard or colored grid) and highlight a few tracer lines in distinct
colors so the eye can follow where they go. In the talk, e^z turns yellow vertical lines into
concentric orange circles.

```python
grid = NumberPlane(x_range=[-3, 3], y_range=[-3, 3], background_line_style={"stroke_opacity": 0.3})
tracers = VGroup(*[
    Line(grid.c2p(x, -3), grid.c2p(x, 3), color=c, stroke_width=4)
    for x, c in [(-1, YELLOW), (0, ORANGE), (1, RED)]
])
self.add(grid, tracers)
self.play(grid.animate.apply_complex_function(lambda z: np.exp(z)),
          tracers.animate.apply_complex_function(lambda z: np.exp(z)), run_time=4)
```

### 31. Image on the Complex Plane

Ground an abstract transformation in a real artifact: place a full-bleed reference image, then
overlay coordinate axes (low-opacity cyan) to reframe it as living on the complex plane. The
viewer accepts "this picture is a function on C," which licenses transforming it (log, rotate,
exponentiate). Pi-creature or any recurring mascot can sit inside the world as an anchor.

```python
art = ImageMobject("escher_print_gallery.png").scale_to_fit_height(6)
axes = ComplexPlane(
    x_range=[-3, 3], y_range=[-3, 3],
    background_line_style={"stroke_color": TEAL, "stroke_opacity": 0.25},
).scale_to_fit_height(6).move_to(art)
self.play(FadeIn(art))
self.play(Create(axes))  # now the image "is" a region of C
```

### 32. Inverse-Function Two-Panel

Teach a function and its inverse as one figure: two panels with bidirectional labeled arrows,
one going forward and one coming back, variables color-coded (z to e^z forward, ln(w) back
from w). Makes "these undo each other" structural rather than asserted.

```python
left = make_panel("log space").to_edge(LEFT)
right = make_panel("exp space").to_edge(RIGHT)
fwd = Arrow(left.get_right(), right.get_left(), buff=0.4).shift(UP * 0.6)
bwd = Arrow(right.get_left(), left.get_right(), buff=0.4).shift(DOWN * 0.6)
fwd_lbl = MathTex(r"z \to e^{z}").next_to(fwd, UP, buff=0.1)
bwd_lbl = MathTex(r"\ln(", "w", r") \leftarrow", "w").next_to(bwd, DOWN, buff=0.1)
bwd_lbl.set_color_by_tex("w", PINK)
self.play(GrowArrow(fwd), Write(fwd_lbl)); self.play(GrowArrow(bwd), Write(bwd_lbl))
```

### 33. Commutative-Diagram Transform Grid

For a multi-step recipe, lay the stages on a grid and connect them with labeled arrows so the
whole pipeline reads at a glance. The talk shows the Escher construction as a 2x2: straighten,
take the log, rotate, exponentiate, with each edge labeled. Different from the Four-Quadrant
Summary (13): this is a process with directed edges, not a static recap.

```python
cells = {
    "tl": panel("log").to_corner(UL), "tr": panel("straight").to_corner(UR),
    "bl": panel("rotated").to_corner(DL), "br": panel("escher").to_corner(DR),
}
edges = [
    (cells["tr"], cells["tl"], MathTex(r"\ln(w) \leftarrow w"), UP),
    (cells["tl"], cells["bl"], Text("Rotate"), LEFT),
    (cells["bl"], cells["br"], MathTex(r"z \to e^{z}"), DOWN),
]
for a, b, lbl, side in edges:
    arr = Arrow(a.get_edge_center(side), b.get_edge_center(-side), buff=0.2)
    self.play(GrowArrow(arr), FadeIn(lbl.next_to(arr, side, buff=0.1)))
```

### 34. North-Star Goal Box with Live Value Readout

Keep the destination claim boxed in a corner for the WHOLE derivation (e^{iπ} = -1 sits
top-right while the circular motion plays out), and show the actual computed value next to the
moving point as the parameter advances (e^{i·3.14} = -1.00 + 0.00i). The viewer always sees
both where they are headed and where they are right now, which makes the moment of arrival land.

```python
goal = MathTex(r"e^{i\pi} = -1").to_corner(UR)
self.add(goal, SurroundingRectangle(goal, color=WHITE, buff=0.15))

t = ValueTracker(0.0)
def fmt(z):
    return f"{z.real:.2f} {'+' if z.imag >= 0 else '-'} {abs(z.imag):.2f}i"
readout = always_redraw(lambda: MathTex(
    rf"e^{{i\cdot {t.get_value():.2f}}} = " + fmt(np.exp(1j * t.get_value())),
    color=TEAL, font_size=32,
).next_to(plane.n2p(np.exp(1j * t.get_value())), UR, buff=0.15))
self.add(readout)
self.play(t.animate.set_value(PI), run_time=4)
```

### 35. Self-Driving System (velocity locked to position)

For an object defined by "velocity is a function of position," draw position and velocity as
adjacent tip-to-tail arrows on the SAME axis so "velocity equals position" reads as a visible
length match, then sweep a tracker so the system drives itself. Runaway growth and decay become
felt, not asserted. (Pair with pattern 29 for the 2D rotational case; color field arrows by
phase for a richer look.)

```python
line = NumberLine(x_range=[0, 9], length=11)
s = ValueTracker(1.0)  # position = e^t
pos_arrow = always_redraw(lambda: Arrow(
    line.n2p(0), line.n2p(s.get_value()), buff=0, color=TEAL, stroke_width=5))
vel_arrow = always_redraw(lambda: Arrow(  # drawn from position's tip; its length = position
    line.n2p(s.get_value()), line.n2p(2 * s.get_value()), buff=0, color=GREEN, stroke_width=5))
self.add(line, pos_arrow, vel_arrow)
self.play(s.animate.set_value(8), run_time=4, rate_func=rate_functions.ease_in_cubic)
```

---

## Quick Reference

| #  | Pattern                        | Category      |
|----|--------------------------------|---------------|
| 1  | Probability Distribution       | Data Display  |
| 2  | Per-Number Sign Coloring       | Data Display  |
| 3  | Running Counters               | Data Display  |
| 4  | Attention Heatmap Table        | Data Display  |
| 5  | Vertical Number Line           | Data Display  |
| 6  | 3D Transparent Box             | Architecture  |
| 7  | Skip Connection Arc            | Architecture  |
| 8  | Exploded Parallel View         | Architecture  |
| 9  | Concrete Pipeline              | Architecture  |
| 10 | Side-by-Side Comparison        | Layout        |
| 11 | Progressive Grid Fill          | Layout        |
| 12 | Multi-Scale Zoom               | Layout        |
| 13 | Four-Quadrant Summary          | Layout        |
| 14 | Title/Concept Decomposition    | Layout        |
| 15 | Question Frame                 | Pedagogical   |
| 16 | Truth vs Convenient Lie        | Pedagogical   |
| 17 | Cloud of Unknown               | Pedagogical   |
| 18 | Absurdist Counterexample       | Pedagogical   |
| 19 | Strikethrough Revision         | Pedagogical   |
| 20 | Interactive Slider             | Pedagogical   |
| 21 | Interpretive Piecewise Labels  | Pedagogical   |
| 22 | Section Title Card             | Pedagogical   |
| 23 | Live Pipeline Data Flow        | Dynamic Data  |
| 24 | Linked Dual Panel              | Dynamic Data  |
| 25 | Heatmap Grid                   | Dynamic Data  |
| 26 | Camera Zoom Detail             | Dynamic Data  |
| 27 | Role-Labeled Equation Boxes    | Transformation |
| 28 | Tip-to-Tail Vector Walk        | Transformation |
| 29 | Vector Field Reveals the Rule  | Transformation |
| 30 | Tracer Lines Through Transform | Transformation |
| 31 | Image on the Complex Plane     | Transformation |
| 32 | Inverse-Function Two-Panel     | Transformation |
| 33 | Commutative-Diagram Grid       | Transformation |
| 34 | North-Star Goal Box + Readout  | Transformation |
| 35 | Self-Driving System            | Transformation |
