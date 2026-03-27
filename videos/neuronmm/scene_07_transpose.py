"""Scene 07: Implicit Transposition -- dual panel comparing naive vs NeuronMM.

Duration: ~60s
Template: DUAL_PANEL
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from utils.style import *


class ImplicitTransposeScene(Scene):
    """Show how NeuronMM avoids explicit transpose by swapping operand roles."""

    def construct(self) -> None:
        self.camera.background_color = BLACK

        # -- Title --
        title = safe_text(
            "Implicit Transposition",
            font_size=TITLE_SIZE,
            color=CHIP_BLUE,
        ).move_to(UP * TITLE_Y)

        self.play(FadeIn(title, shift=DOWN * 0.3), run_time=1.0)
        self.wait(HOLD_SHORT)

        # -- Vertical divider --
        divider = DashedLine(
            start=UP * 2.3, end=DOWN * 2.5,
            color=GRAY_B, dash_length=0.12, stroke_width=2,
        )
        self.play(Create(divider), run_time=0.6)

        # -- Panel headers --
        left_header = safe_text(
            "Naive Approach", font_size=HEADING_SIZE, color=DANGER_RED,
        ).move_to(UP * 2.2 + LEFT * 3.3)

        right_header = safe_text(
            "NeuronMM", font_size=HEADING_SIZE, color=SUCCESS_GREEN,
        ).move_to(UP * 2.2 + RIGHT * 3.3)

        self.play(
            Write(left_header), Write(right_header), run_time=1.0,
        )
        self.wait(HOLD_SHORT)

        # ============================================================
        # LEFT PANEL: Naive approach (x in [-5.5, -0.8])
        # ============================================================
        left_cx = -3.3

        # Step 1: Compute Y = X * U
        step1_label = safe_text(
            "Step 1: Y = X * U",
            font_size=LABEL_SIZE, color=WHITE,
        ).move_to(UP * 1.3 + LEFT * 3.3)

        mat_x = matrix_rect("X", 1, "d", MATRIX_X, width=1.0, height=0.7)
        mat_u = matrix_rect("U", "d", "r", MATRIX_U, width=1.0, height=0.7)
        mat_y = matrix_rect("Y", 1, "r", MATRIX_Y, width=1.0, height=0.7)
        times1 = MathTex(r"\times", font_size=LABEL_SIZE, color=WHITE)
        eq1 = MathTex(r"=", font_size=LABEL_SIZE, color=WHITE)

        step1_row = VGroup(mat_x, times1, mat_u, eq1, mat_y).arrange(
            RIGHT, buff=0.15,
        ).move_to(UP * 0.5 + LEFT * 3.3)
        step1_row.scale_to_fit_width(4.2)

        self.play(Write(step1_label), run_time=0.6)
        self.play(FadeIn(step1_row), run_time=0.8)
        self.wait(HOLD_SHORT)

        # Step 2: Transpose Y -> Y^T (expensive)
        step2_label = safe_text(
            "Step 2: Transpose Y",
            font_size=LABEL_SIZE, color=WHITE,
        ).move_to(DOWN * 0.4 + LEFT * 3.3)

        mat_y2 = matrix_rect("Y", 1, "r", MATRIX_Y, width=1.0, height=0.7)
        mat_yt = matrix_rect("Y^T", "r", 1, MATRIX_Y, width=0.7, height=1.0)

        transpose_group = VGroup(mat_y2, mat_yt).arrange(
            RIGHT, buff=0.8,
        ).move_to(DOWN * 1.2 + LEFT * 3.3)
        transpose_group.scale_to_fit_width(3.5)

        rotate_arrow = CurvedArrow(
            mat_y2.get_right() + RIGHT * 0.1,
            mat_yt.get_left() + LEFT * 0.1,
            angle=-TAU / 6, color=DANGER_RED, stroke_width=3,
        )

        expensive_label = safe_text(
            "expensive!", font_size=20, color=DANGER_RED,
        ).next_to(rotate_arrow, UP, buff=0.1)

        self.play(Write(step2_label), run_time=0.6)
        self.play(
            FadeIn(mat_y2),
            Create(rotate_arrow),
            FadeIn(mat_yt),
            run_time=1.2,
        )
        self.play(FadeIn(expensive_label, scale=1.2), run_time=0.5)
        self.wait(HOLD_SHORT)

        # Step 3 label
        step3_label = safe_text(
            "Step 3: Use Y^T in next matmul",
            font_size=LABEL_SIZE, color=WHITE,
        ).move_to(DOWN * 2.2 + LEFT * 3.3)
        self.play(Write(step3_label), run_time=0.6)
        self.wait(HOLD_SHORT)

        # Cross out the entire left pipeline
        left_all = VGroup(
            step1_label, step1_row, step2_label,
            mat_y2, rotate_arrow, mat_yt, expensive_label, step3_label,
        )
        cross_line1 = Line(
            left_all.get_corner(UL) + LEFT * 0.2 + UP * 0.1,
            left_all.get_corner(DR) + RIGHT * 0.2 + DOWN * 0.1,
            color=DANGER_RED, stroke_width=5,
        )
        cross_line2 = Line(
            left_all.get_corner(UR) + RIGHT * 0.2 + UP * 0.1,
            left_all.get_corner(DL) + LEFT * 0.2 + DOWN * 0.1,
            color=DANGER_RED, stroke_width=5,
        )
        self.play(
            Create(cross_line1), Create(cross_line2), run_time=0.8,
        )
        self.wait(HOLD_SHORT)

        # ============================================================
        # RIGHT PANEL: NeuronMM (x in [0.8, 5.5])
        # ============================================================
        right_cx = 3.3

        # Key equation: (XU)^T = U^T X^T
        eq_tex = MathTex(
            r"(XU)^T", r"=", r"U^T", r"\cdot", r"X^T",
            font_size=EQ_SIZE,
        ).move_to(UP * 1.0 + RIGHT * right_cx)
        eq_tex[0].set_color(MATRIX_Y)
        eq_tex[2].set_color(MATRIX_U)
        eq_tex[4].set_color(MATRIX_X)

        self.play(Write(eq_tex), run_time=1.5)
        self.wait(HOLD_MEDIUM)

        # Insight box
        insight_lines = safe_multiline(
            "Swap operand roles in",
            "the NKI kernel call:",
            "stationary = U^T",
            "moving = X^T",
            font_size=20, color=WHITE, line_buff=0.22, max_width=4.5,
        ).move_to(DOWN * 0.3 + RIGHT * right_cx)

        insight_box = SurroundingRectangle(
            insight_lines, color=CHIP_BLUE, buff=0.2,
            corner_radius=0.1, stroke_width=2, fill_opacity=0.05,
        )

        self.play(
            FadeIn(insight_lines, shift=UP * 0.2),
            Create(insight_box),
            run_time=1.2,
        )
        self.wait(HOLD_MEDIUM)

        # "Free!" label + checkmark
        free_label = safe_text(
            "Free!", font_size=HEADING_SIZE, color=SUCCESS_GREEN,
        ).move_to(DOWN * 1.7 + RIGHT * 2.3)

        checkmark = MathTex(
            r"\checkmark", font_size=48, color=SUCCESS_GREEN,
        ).next_to(free_label, RIGHT, buff=0.2)

        result_text = safe_text(
            "Result is already transposed",
            font_size=20, color=GRAY_B,
        ).next_to(free_label, DOWN, buff=0.2)

        self.play(
            FadeIn(free_label, scale=0.8),
            FadeIn(checkmark, scale=0.5),
            run_time=0.8,
        )
        self.play(Write(result_text), run_time=0.8)
        self.wait(HOLD_MEDIUM)

        # -- Bottom note --
        note = bottom_note(
            "Zero-cost transposition by swapping operand roles"
        )
        self.play(FadeIn(note, shift=UP * 0.2), run_time=0.8)
        self.wait(HOLD_LONG)

        # -- Cleanup --
        fade_all(
            self, title, divider, left_header, right_header,
            left_all, cross_line1, cross_line2,
            eq_tex, insight_lines, insight_box,
            free_label, checkmark, result_text, note,
        )
        self.wait(0.5)
