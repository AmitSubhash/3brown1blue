"""Scene 09: Performance Results -- kernel speedups, E2E speedups, accuracy.

Duration: ~90s
Template: CHART_FOCUS
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from utils.style import *


# -- Data --
MODELS: list[str] = ["Llama-3.2-1B", "Llama-3.2-3B", "Qwen3-1.7B", "Qwen3-4B"]
KERNEL_SPEEDUPS: list[float] = [1.35, 1.42, 1.28, 1.35]
E2E_SPEEDUPS: list[float] = [1.63, 2.49, 1.74, 1.67]
ACCURACY_DROPS: list[str] = ["-0.07", "-0.10", "-0.03", "-0.05"]

BAR_WIDTH: float = 0.5
GROUP_SPACING: float = 2.4


def _build_bar_chart(
    axes: Axes,
    values: list[float],
    baseline: float,
    bar_color: str,
    base_color: str,
    x_positions: list[float],
) -> tuple[VGroup, VGroup]:
    """Build paired baseline + value bars. Returns (baseline_bars, value_bars)."""
    base_bars = VGroup()
    val_bars = VGroup()

    for i, (xp, val) in enumerate(zip(x_positions, values)):
        # Baseline bar
        b_height = axes.c2p(0, baseline)[1] - axes.c2p(0, 0)[1]
        b_rect = Rectangle(
            width=BAR_WIDTH, height=max(b_height, 0.01),
            color=base_color, fill_opacity=0.5, stroke_width=1,
        )
        b_rect.move_to(axes.c2p(xp - 0.3, baseline / 2))
        base_bars.add(b_rect)

        # Value bar
        v_height = axes.c2p(0, val)[1] - axes.c2p(0, 0)[1]
        v_rect = Rectangle(
            width=BAR_WIDTH, height=max(v_height, 0.01),
            color=bar_color, fill_opacity=0.7, stroke_width=1,
        )
        v_rect.move_to(axes.c2p(xp + 0.3, val / 2))
        val_bars.add(v_rect)

    return base_bars, val_bars


class ResultsScene(Scene):
    """Three-phase results: kernel speedup, E2E speedup, accuracy impact."""

    def construct(self) -> None:
        self.camera.background_color = BLACK

        # -- Title --
        title = safe_text(
            "Performance Results",
            font_size=TITLE_SIZE, color=CHIP_BLUE,
        ).move_to(UP * TITLE_Y)
        self.play(FadeIn(title, shift=DOWN * 0.3), run_time=1.0)
        self.wait(HOLD_SHORT)

        # ============================================================
        # Phase 1: Kernel Speedup Bar Chart
        # ============================================================
        x_positions = [1, 2.5, 4, 5.5]

        axes1 = Axes(
            x_range=[0, 6.5, 1],
            y_range=[0, 1.8, 0.2],
            x_length=9.5,
            y_length=3.8,
            axis_config={
                "color": GRAY_B, "stroke_width": 2,
                "include_ticks": True, "font_size": 16,
            },
            tips=False,
        ).move_to(DOWN * 0.3)

        y1_label = safe_text(
            "Kernel Speedup (x)",
            font_size=LABEL_SIZE, color=GRAY_B,
        ).rotate(PI / 2).next_to(axes1.y_axis, LEFT, buff=0.5)

        # Model name labels
        model_labels1 = VGroup()
        for i, (name, xp) in enumerate(zip(MODELS, x_positions)):
            ml = safe_text(name, font_size=14, color=GRAY_B)
            ml.move_to(axes1.c2p(xp, 0) + DOWN * 0.35)
            model_labels1.add(ml)

        self.play(Create(axes1), Write(y1_label), run_time=1.0)
        self.play(FadeIn(model_labels1), run_time=0.6)

        # Build bars
        base_bars1, val_bars1 = _build_bar_chart(
            axes1, KERNEL_SPEEDUPS, 1.0,
            SPEEDUP_YELLOW, BASELINE_GRAY, x_positions,
        )

        # Animate baseline bars appearing
        self.play(
            *[GrowFromEdge(b, DOWN) for b in base_bars1],
            run_time=0.8,
        )
        # Animate value bars growing
        self.play(
            *[GrowFromEdge(b, DOWN) for b in val_bars1],
            run_time=1.2,
        )
        self.wait(HOLD_SHORT)

        # Bar value labels
        val_labels1 = VGroup()
        for i, (xp, val) in enumerate(zip(x_positions, KERNEL_SPEEDUPS)):
            vl = safe_text(
                f"{val:.2f}x", font_size=16, color=SPEEDUP_YELLOW,
            )
            vl.next_to(val_bars1[i], UP, buff=0.1)
            val_labels1.add(vl)
        self.play(FadeIn(val_labels1, lag_ratio=0.1), run_time=0.8)

        # "up to 2.22x" callout pointing at highest bar (index 1)
        max_callout = safe_text(
            "up to 2.22x", font_size=20, color=SPEEDUP_YELLOW,
        )
        max_callout.next_to(val_bars1[1], UP, buff=0.5)
        max_arrow = Arrow(
            max_callout.get_bottom(),
            val_labels1[1].get_top() + UP * 0.05,
            buff=0.08, color=SPEEDUP_YELLOW, stroke_width=2,
            max_tip_length_to_length_ratio=0.2,
        )
        self.play(
            FadeIn(max_callout, shift=DOWN * 0.1),
            Create(max_arrow),
            run_time=0.8,
        )
        self.wait(HOLD_MEDIUM)

        # Legend
        legend = VGroup(
            VGroup(
                Rectangle(width=0.3, height=0.2, color=BASELINE_GRAY, fill_opacity=0.5),
                safe_text("Baseline", font_size=14, color=BASELINE_GRAY),
            ).arrange(RIGHT, buff=0.1),
            VGroup(
                Rectangle(width=0.3, height=0.2, color=SPEEDUP_YELLOW, fill_opacity=0.7),
                safe_text("NeuronMM", font_size=14, color=SPEEDUP_YELLOW),
            ).arrange(RIGHT, buff=0.1),
        ).arrange(RIGHT, buff=0.5).move_to(UP * 2.2 + RIGHT * 3.0)
        self.play(FadeIn(legend), run_time=0.5)
        self.wait(HOLD_MEDIUM)

        # -- Fade Phase 1 --
        phase1 = VGroup(
            axes1, y1_label, model_labels1,
            base_bars1, val_bars1, val_labels1,
            max_callout, max_arrow, legend,
        )
        self.play(FadeOut(phase1), run_time=0.8)

        # ============================================================
        # Phase 2: End-to-End Speedup
        # ============================================================
        phase2_header = safe_text(
            "End-to-End Speedup",
            font_size=HEADING_SIZE, color=WHITE,
        ).move_to(UP * 2.2)
        self.play(Write(phase2_header), run_time=0.8)

        axes2 = Axes(
            x_range=[0, 6.5, 1],
            y_range=[0, 3.0, 0.5],
            x_length=9.5,
            y_length=3.5,
            axis_config={
                "color": GRAY_B, "stroke_width": 2,
                "include_ticks": True, "font_size": 16,
            },
            tips=False,
        ).move_to(DOWN * 0.3)

        y2_label = safe_text(
            "E2E Speedup (x)",
            font_size=LABEL_SIZE, color=GRAY_B,
        ).rotate(PI / 2).next_to(axes2.y_axis, LEFT, buff=0.5)

        model_labels2 = VGroup()
        for name, xp in zip(MODELS, x_positions):
            ml = safe_text(name, font_size=14, color=GRAY_B)
            ml.move_to(axes2.c2p(xp, 0) + DOWN * 0.35)
            model_labels2.add(ml)

        self.play(Create(axes2), Write(y2_label), run_time=0.8)
        self.play(FadeIn(model_labels2), run_time=0.5)

        base_bars2, val_bars2 = _build_bar_chart(
            axes2, E2E_SPEEDUPS, 1.0,
            SPEEDUP_YELLOW, BASELINE_GRAY, x_positions,
        )

        self.play(
            *[GrowFromEdge(b, DOWN) for b in base_bars2],
            run_time=0.6,
        )
        self.play(
            *[GrowFromEdge(b, DOWN) for b in val_bars2],
            run_time=1.2,
        )

        # Value labels
        val_labels2 = VGroup()
        for i, (xp, val) in enumerate(zip(x_positions, E2E_SPEEDUPS)):
            vl = safe_text(
                f"{val:.2f}x", font_size=18, color=SPEEDUP_YELLOW,
            )
            vl.next_to(val_bars2[i], UP, buff=0.1)
            val_labels2.add(vl)
        self.play(FadeIn(val_labels2, lag_ratio=0.1), run_time=0.8)
        self.wait(HOLD_SHORT)

        # Highlight Llama-3.2-3B at 2.49x
        highlight_rect = SurroundingRectangle(
            VGroup(val_bars2[1], val_labels2[1]),
            color=SPEEDUP_YELLOW, buff=0.15,
            corner_radius=0.08, stroke_width=3,
        )
        self.play(Create(highlight_rect), run_time=0.8)

        throughput_note = safe_text(
            "49.69 -> 92.52 tokens/s",
            font_size=18, color=SPEEDUP_YELLOW,
        ).next_to(highlight_rect, UP, buff=0.15)
        self.play(FadeIn(throughput_note, shift=DOWN * 0.1), run_time=0.8)
        self.wait(HOLD_LONG)

        # -- Fade Phase 2 --
        phase2 = VGroup(
            phase2_header, axes2, y2_label, model_labels2,
            base_bars2, val_bars2, val_labels2,
            highlight_rect, throughput_note,
        )
        self.play(FadeOut(phase2), run_time=0.8)

        # ============================================================
        # Phase 3: Accuracy Impact Grid
        # ============================================================
        phase3_header = safe_text(
            "Accuracy Impact (mAcc change)",
            font_size=HEADING_SIZE, color=WHITE,
        ).move_to(UP * 2.0)
        self.play(Write(phase3_header), run_time=0.8)

        cards = VGroup()
        for i, (model, drop) in enumerate(zip(MODELS, ACCURACY_DROPS)):
            card_name = safe_text(
                model, font_size=20, color=WHITE,
            )
            card_val = safe_text(
                drop, font_size=HEADING_SIZE, color=SUCCESS_GREEN,
            )
            card_content = VGroup(card_name, card_val).arrange(DOWN, buff=0.2)
            card_box = RoundedRectangle(
                width=2.6, height=1.5, corner_radius=0.12,
                color=SUCCESS_GREEN, fill_opacity=0.08, stroke_width=2,
            )
            card_content.move_to(card_box)
            cards.add(VGroup(card_box, card_content))

        cards.arrange(RIGHT, buff=0.35).move_to(DOWN * 0.2)
        # Scale if too wide
        if cards.width > 11.0:
            cards.scale_to_fit_width(11.0)

        self.play(
            *[FadeIn(c, shift=UP * 0.2, lag_ratio=0.05) for c in cards],
            run_time=1.5,
        )
        self.wait(HOLD_MEDIUM)

        # -- Bottom note --
        note = bottom_note(
            "Negligible accuracy loss with LoRA fine-tuning"
        )
        self.play(FadeIn(note, shift=UP * 0.2), run_time=0.8)
        self.wait(HOLD_LONG)

        # -- Cleanup --
        fade_all(self, title, phase3_header, cards, note)
        self.wait(0.5)
