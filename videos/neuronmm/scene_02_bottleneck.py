"""Scene 02: The Matmul Bottleneck -- compute breakdown and accelerator comparison.

Duration: ~90s
Template: DUAL_PANEL
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from utils.style import *


class MatmulBottleneckScene(Scene):
    """Matmul dominance in LLM inference + Trainium cost advantage."""

    def construct(self) -> None:
        self.camera.background_color = BLACK

        # -- Title --
        title = safe_text(
            "The Matmul Bottleneck",
            font_size=TITLE_SIZE,
            color=WHITE,
        ).move_to(UP * TITLE_Y)

        self.play(Write(title), run_time=1.2)
        self.wait(HOLD_SHORT)

        # ========================================
        # LEFT PANEL: Equation + Stacked Bar
        # ========================================
        left_center_x = -3.2

        # Y = XW equation
        eq = MathTex(
            "Y", "=", "X", "W",
            font_size=EQ_SIZE,
        ).move_to(RIGHT * left_center_x + UP * 1.5)
        eq[0].set_color(MATRIX_Y)
        eq[2].set_color(MATRIX_X)
        eq[3].set_color(MATRIX_W)

        self.play(Write(eq), run_time=1.2)
        self.wait(HOLD_SHORT)

        # Stacked bar chart: Matmul 70%, Attention 15%, Other 15%
        bar_width = 3.5
        bar_height = 0.7
        bar_anchor = RIGHT * left_center_x + DOWN * 0.2

        # Matmul bar (70%)
        matmul_w = bar_width * 0.70
        matmul_bar = Rectangle(
            width=matmul_w, height=bar_height,
            color=DANGER_RED, fill_opacity=0.6, stroke_width=1.5,
        )
        matmul_bar.move_to(bar_anchor)
        matmul_bar.align_to(bar_anchor + LEFT * bar_width / 2, LEFT)
        matmul_label = safe_text("Matmul 70%", font_size=18, color=WHITE)
        matmul_label.move_to(matmul_bar)

        # Attention bar (15%)
        attn_w = bar_width * 0.15
        attn_bar = Rectangle(
            width=attn_w, height=bar_height,
            color=CHIP_BLUE, fill_opacity=0.5, stroke_width=1.5,
        )
        attn_bar.next_to(matmul_bar, RIGHT, buff=0)
        attn_label = safe_text("Attn 15%", font_size=16, color=WHITE)
        attn_label.move_to(attn_bar)
        if attn_label.width > attn_w - 0.1:
            attn_label.scale_to_fit_width(attn_w - 0.1)

        # Other bar (15%)
        other_w = bar_width * 0.15
        other_bar = Rectangle(
            width=other_w, height=bar_height,
            color=BASELINE_GRAY, fill_opacity=0.4, stroke_width=1.5,
        )
        other_bar.next_to(attn_bar, RIGHT, buff=0)
        other_label = safe_text("Other 15%", font_size=16, color=WHITE)
        other_label.move_to(other_bar)
        if other_label.width > other_w - 0.1:
            other_label.scale_to_fit_width(other_w - 0.1)

        bar_group = VGroup(
            matmul_bar, matmul_label,
            attn_bar, attn_label,
            other_bar, other_label,
        )

        compute_title = safe_text(
            "LLM Inference Compute",
            font_size=LABEL_SIZE,
            color=BASELINE_GRAY,
        ).next_to(bar_group, DOWN, buff=0.3)

        self.play(
            Create(matmul_bar), Write(matmul_label),
            run_time=1.0,
        )
        self.play(
            Create(attn_bar), Write(attn_label),
            Create(other_bar), Write(other_label),
            run_time=0.8,
        )
        self.play(FadeIn(compute_title, shift=UP * 0.1), run_time=0.6)
        self.wait(HOLD_MEDIUM)

        # ========================================
        # RIGHT PANEL: GPU vs Trainium
        # ========================================
        right_center_x = 3.0

        gpu_box = labeled_box(
            "GPU: CUDA Cores",
            width=3.2, height=0.9,
            color=BASELINE_GRAY,
            fill_opacity=0.15,
        ).move_to(RIGHT * right_center_x + UP * 1.4)

        trainium_box = labeled_box(
            "Trainium: Systolic Array",
            width=3.2, height=0.9,
            color=CHIP_BLUE,
            fill_opacity=0.2,
        ).move_to(RIGHT * right_center_x + UP * 0.2)

        self.play(FadeIn(gpu_box, shift=LEFT * 0.3), run_time=0.8)
        self.play(FadeIn(trainium_box, shift=LEFT * 0.3), run_time=0.8)
        self.wait(HOLD_SHORT)

        # Trainium advantage callout
        advantage = safe_multiline(
            "95 TFLOPS",
            "at 60% GPU cost",
            font_size=BODY_SIZE,
            color=SUCCESS_GREEN,
            line_buff=0.25,
        ).move_to(RIGHT * right_center_x + DOWN * 1.2)

        self.play(FadeIn(advantage, shift=UP * 0.2), run_time=1.0)
        self.wait(HOLD_MEDIUM)

        # Arrow connecting left result to right -- "can we optimize?"
        bridge_arrow = Arrow(
            start=LEFT * 0.8 + DOWN * 0.2,
            end=RIGHT * 1.0 + DOWN * 0.2,
            color=SPEEDUP_YELLOW,
            stroke_width=3,
            buff=0.1,
            max_tip_length_to_length_ratio=0.2,
        )
        question = safe_text(
            "Can we optimize?",
            font_size=LABEL_SIZE,
            color=SPEEDUP_YELLOW,
        ).next_to(bridge_arrow, DOWN, buff=0.2)

        self.play(Create(bridge_arrow), Write(question), run_time=1.2)
        self.wait(HOLD_LONG)

        # -- Bottom note --
        note = bottom_note(
            "Matmul dominates LLM inference -- custom accelerators offer cost advantages"
        )
        self.play(FadeIn(note, shift=UP * 0.2), run_time=0.8)
        self.wait(HOLD_LONG)

        # -- Cleanup --
        fade_all(
            self,
            title, eq,
            bar_group, compute_title,
            gpu_box, trainium_box, advantage,
            bridge_arrow, question, note,
        )
        self.wait(0.5)
