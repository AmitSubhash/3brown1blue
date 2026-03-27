"""Scene 08: Block Size Optimization -- chart of arithmetic intensity vs BM.

Duration: ~90s
Template: CHART_FOCUS
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from utils.style import *


# -- Data constants --
BM_LABELS: list[str] = ["128", "256", "512", "1024", "2048", "4096"]
BM_X: list[float] = [0, 1, 2, 3, 4, 5]
AI_VALUES: list[float] = [124, 239, 455, 819, 1280, 2048]
COMPUTE_THRESHOLD: float = 222  # BF16 compute-bound line


class BlockSizeOptScene(Scene):
    """Arithmetic intensity vs block size with SBUF spill annotations."""

    def construct(self) -> None:
        self.camera.background_color = BLACK

        # -- Title --
        title = safe_text(
            "Block Size Optimization",
            font_size=TITLE_SIZE, color=CHIP_BLUE,
        ).move_to(UP * TITLE_Y)

        self.play(FadeIn(title, shift=DOWN * 0.3), run_time=1.0)
        self.wait(HOLD_SHORT)

        # -- Axes --
        axes = Axes(
            x_range=[0, 5.5, 1],
            y_range=[0, 2200, 200],
            x_length=9.0,
            y_length=4.5,
            axis_config={
                "color": GRAY_B,
                "stroke_width": 2,
                "include_ticks": True,
                "font_size": 18,
            },
            tips=False,
        ).move_to(DOWN * 0.2)

        # Axis labels
        x_label = safe_text(
            "Block Size (BM)", font_size=LABEL_SIZE, color=GRAY_B,
        ).next_to(axes.x_axis, DOWN, buff=0.55)

        y_label = safe_text(
            "Arithmetic Intensity (Flops/Byte)",
            font_size=LABEL_SIZE, color=GRAY_B,
        ).rotate(PI / 2).next_to(axes.y_axis, LEFT, buff=0.55)

        # Custom x-axis tick labels
        x_tick_labels = VGroup()
        for i, label_str in enumerate(BM_LABELS):
            tick = safe_text(label_str, font_size=16, color=GRAY_B)
            tick.move_to(axes.c2p(i, 0) + DOWN * 0.3)
            x_tick_labels.add(tick)

        self.play(Create(axes), run_time=1.2)
        self.play(
            Write(x_label), Write(y_label),
            FadeIn(x_tick_labels),
            run_time=1.0,
        )
        self.wait(HOLD_SHORT)

        # -- Plot curve --
        points = [axes.c2p(x, y) for x, y in zip(BM_X, AI_VALUES)]
        dots = VGroup(*[
            Dot(p, radius=0.08, color=SPEEDUP_YELLOW) for p in points
        ])
        line_graph = VMobject(color=SPEEDUP_YELLOW, stroke_width=3)
        line_graph.set_points_smoothly(points)

        self.play(Create(line_graph), run_time=2.0)
        self.play(FadeIn(dots, lag_ratio=0.15), run_time=1.0)
        self.wait(HOLD_SHORT)

        # -- Compute-bound threshold (dashed horizontal) --
        threshold_y = COMPUTE_THRESHOLD
        left_pt = axes.c2p(0, threshold_y)
        right_pt = axes.c2p(5.5, threshold_y)
        threshold_line = DashedLine(
            left_pt, right_pt,
            color=SUCCESS_GREEN, dash_length=0.1, stroke_width=2,
        )
        threshold_label = safe_text(
            "Compute-bound threshold",
            font_size=18, color=SUCCESS_GREEN,
        ).next_to(threshold_line, RIGHT, buff=0.15)
        # Keep label within bounds
        if threshold_label.get_right()[0] > 5.5:
            threshold_label.move_to(
                axes.c2p(4.2, threshold_y) + UP * 0.3
            )

        self.play(
            Create(threshold_line), Write(threshold_label), run_time=1.0,
        )
        self.wait(HOLD_SHORT)

        # -- Shaded compute-bound zone (above threshold) --
        shade_corners = [
            axes.c2p(0, threshold_y),
            axes.c2p(5.5, threshold_y),
            axes.c2p(5.5, 2200),
            axes.c2p(0, 2200),
        ]
        shade = Polygon(
            *shade_corners,
            color=SUCCESS_GREEN, fill_opacity=0.08,
            stroke_width=0,
        )
        self.play(FadeIn(shade), run_time=0.8)
        self.wait(HOLD_SHORT)

        # -- SBUF usage annotations --
        sbuf_data: list[tuple[int, str, str]] = [
            (3, "90% SBUF, No spill", SUCCESS_GREEN),
            (4, "96% SBUF, 29MB spill", DANGER_RED),
            (5, "99% SBUF, 931MB spill", DANGER_RED),
        ]
        sbuf_labels = VGroup()
        for idx, text_str, color in sbuf_data:
            lbl = safe_text(text_str, font_size=14, color=color)
            lbl.next_to(dots[idx], UP, buff=0.2)
            # Shift left if it overflows right boundary
            if lbl.get_right()[0] > 5.3:
                lbl.shift(LEFT * (lbl.get_right()[0] - 5.0))
            sbuf_labels.add(lbl)

        self.play(
            *[FadeIn(lbl, shift=DOWN * 0.1) for lbl in sbuf_labels],
            run_time=1.2,
        )
        self.wait(HOLD_MEDIUM)

        # -- Highlight optimal BM=1024 --
        optimal_dot = dots[3]  # index 3 = BM=1024
        highlight_rect = SurroundingRectangle(
            optimal_dot, color=SPEEDUP_YELLOW, buff=0.2,
            corner_radius=0.08, stroke_width=3,
        )
        optimal_label = safe_text(
            "Optimal", font_size=20, color=SPEEDUP_YELLOW,
        ).next_to(highlight_rect, DOWN, buff=0.15)

        self.play(
            Create(highlight_rect),
            FadeIn(optimal_label, shift=UP * 0.1),
            run_time=1.0,
        )
        self.wait(HOLD_MEDIUM)

        # -- Equation in top-right corner --
        eq = MathTex(
            r"AI = \frac{2r}{\left(1 + \frac{r}{BM}\right) \cdot s}",
            font_size=SMALL_EQ, color=WHITE,
        ).move_to(UP * 2.2 + RIGHT * 4.0)

        eq_box = SurroundingRectangle(
            eq, color=CHIP_BLUE, buff=0.15,
            corner_radius=0.08, stroke_width=1.5, fill_opacity=0.05,
        )

        self.play(Write(eq), Create(eq_box), run_time=1.5)
        self.wait(HOLD_MEDIUM)

        # -- Bottom note --
        note = bottom_note(
            "BM=1024: maximum arithmetic intensity without SBUF spilling"
        )
        self.play(FadeIn(note, shift=UP * 0.2), run_time=0.8)
        self.wait(HOLD_LONG)

        # -- Cleanup --
        fade_all(
            self, title, axes, x_label, y_label, x_tick_labels,
            line_graph, dots, threshold_line, threshold_label, shade,
            sbuf_labels, highlight_rect, optimal_label,
            eq, eq_box, note,
        )
        self.wait(0.5)
