"""Reference scenes for the Designing Math patterns (catalog 27, 28, 29).

These reproduce three visuals from Grant Sanderson's "Designing Math"
(Config 2026) using the helpers in templates/style.py, and double as a
render check that those helpers work.

Render the stills:
    manim -s -qm designing_math_demo.py P27RoleBoxes
    manim -s -qm designing_math_demo.py P28VectorWalk
    manim -s -qm designing_math_demo.py P29VectorField

See ../../rules/explanation-design.md and ../../rules/visual-design-catalog.md.
"""

# Manim's API is used via `from manim import *`, the framework's standard idiom.
# ruff: noqa: F403, F405

import math
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "templates"))
from manim import *  # noqa: E402,F403
from style import ENTITY, glow_dot, role_annotation, vector_walk  # noqa: E402


class P27RoleBoxes(Scene):
    """Pattern 27: box each part of an equation and label what it DOES."""

    def construct(self) -> None:
        eq = MathTex(
            r"\frac{d}{dt} e^{it}",
            r"=",
            r"i",
            r"\cdot",
            r"e^{it}",
            font_size=72,
        )
        self.add(eq)
        self.add(role_annotation(eq[0], "Velocity", ENTITY["path"], DOWN))
        self.add(role_annotation(eq[2], "Rotate 90°", ENTITY["active"], UP))
        self.add(role_annotation(eq[4], "Position", ENTITY["position"], DOWN))


class P28VectorWalk(Scene):
    """Pattern 28: e^{i*pi} as a tip-to-tail spiral landing on -1."""

    def construct(self) -> None:
        # Range covers the partial sums, which overshoot to real ~ -4 and
        # imag ~ -2 before spiraling back in to -1.
        plane = ComplexPlane(
            x_range=[-4.5, 1.5],
            y_range=[-2.5, 3.5],
            background_line_style={
                "stroke_color": ENTITY["grid"],
                "stroke_opacity": 0.5,
            },
        )
        partials: list[complex] = [0j]
        total = 0j
        for n in range(14):
            total += (1j * math.pi) ** n / math.factorial(n)
            partials.append(total)

        walk = vector_walk(partials, plane.n2p, ENTITY["path"])
        dot = glow_dot(plane.n2p(-1), ENTITY["active"])
        label = MathTex("-1", color=ENTITY["active"], font_size=40)
        label.next_to(plane.n2p(-1), DR, buff=0.1)

        VGroup(plane, walk, dot, label).scale_to_fit_height(7).move_to(ORIGIN)
        self.add(plane, walk, dot, label)


class P29VectorField(Scene):
    """Pattern 29: position (teal) + velocity (green) field => circular motion."""

    def construct(self) -> None:
        plane = NumberPlane(
            x_range=[-2.5, 2.5],
            y_range=[-2, 2],
            background_line_style={
                "stroke_color": ENTITY["grid"],
                "stroke_opacity": 0.4,
            },
        )
        self.add(plane)
        field = VGroup()
        for ang in np.linspace(0, TAU, 12, endpoint=False):
            pos = np.array([np.cos(ang), np.sin(ang), 0])
            vel = np.array([-pos[1], pos[0], 0])  # multiply by i = rotate 90 degrees
            field.add(
                Arrow(
                    plane.c2p(0, 0),
                    plane.c2p(pos[0], pos[1]),
                    buff=0,
                    color=ENTITY["position"],
                    stroke_width=3,
                    max_tip_length_to_length_ratio=0.2,
                )
            )
            field.add(
                Arrow(
                    plane.c2p(pos[0], pos[1]),
                    plane.c2p(*(pos + vel)[:2]),
                    buff=0,
                    color=ENTITY["path"],
                    stroke_width=3,
                    max_tip_length_to_length_ratio=0.2,
                )
            )
        self.add(field)
        unit = float(np.linalg.norm(plane.c2p(1, 0) - plane.c2p(0, 0)))
        self.add(
            Circle(radius=unit, color=WHITE, stroke_opacity=0.3).move_to(
                plane.c2p(0, 0)
            )
        )
