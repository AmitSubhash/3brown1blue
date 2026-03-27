"""Scene 04: SVD Weight Compression.

Shows how a large weight matrix W is decomposed via SVD into smaller
factors U and V, reducing FLOPs when the rank r is small.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from utils.style import *


class SVDDecompositionScene(Scene):
    """Animate SVD decomposition W -> U*V and the matmul transformation."""

    def construct(self) -> None:
        # ── Title ──
        title = safe_text(
            "SVD Weight Compression", font_size=TITLE_SIZE, color=WHITE
        ).move_to(UP * TITLE_Y)
        self.play(Write(title))
        self.wait(HOLD_SHORT)

        # ── Phase 1: Show large weight matrix W ──
        w_rect = Rectangle(
            width=2.8, height=2.2,
            color=MATRIX_W, fill_opacity=0.35, stroke_width=2,
        ).move_to(ORIGIN)
        w_label = safe_text("W", font_size=HEADING_SIZE, color=MATRIX_W)
        w_label.move_to(w_rect)
        w_dim = safe_text("[k x n]", font_size=16, color=GRAY_B)
        w_dim.next_to(w_rect, DOWN, buff=0.15)
        w_group = VGroup(w_rect, w_label, w_dim)

        self.play(FadeIn(w_group, shift=UP * 0.3))
        self.wait(HOLD_SHORT)

        # ── Phase 2: SVD equation ──
        svd_eq = MathTex(
            "W", "=", "U", r"\Sigma", "V^T",
            font_size=EQ_SIZE,
        ).move_to(UP * 1.0)
        svd_eq[0].set_color(MATRIX_W)
        svd_eq[2].set_color(MATRIX_U)
        svd_eq[3].set_color(ACCENT)
        svd_eq[4].set_color(MATRIX_V)

        # Move W matrix down to make room for equation
        self.play(
            w_group.animate.move_to(DOWN * 0.8),
            FadeIn(svd_eq, shift=DOWN * 0.2),
        )
        self.wait(HOLD_MEDIUM)

        # ── Phase 3: Approximate -- absorb Sigma, keep top r ──
        approx_eq = MathTex(
            "W", r"\approx", "U_r", "V_r",
            font_size=EQ_SIZE,
        ).move_to(svd_eq.get_center())
        approx_eq[0].set_color(MATRIX_W)
        approx_eq[2].set_color(MATRIX_U)
        approx_eq[3].set_color(MATRIX_V)

        self.play(TransformMatchingTex(svd_eq, approx_eq))
        self.wait(HOLD_SHORT)

        # ── Phase 4: Split W into U and V rectangles ──
        u_rect = Rectangle(
            width=1.2, height=2.2,
            color=MATRIX_U, fill_opacity=0.35, stroke_width=2,
        )
        u_label = safe_text("U", font_size=HEADING_SIZE, color=MATRIX_U)
        u_dim = safe_text("[k x r]", font_size=16, color=GRAY_B)

        v_rect = Rectangle(
            width=2.8, height=1.0,
            color=MATRIX_V, fill_opacity=0.35, stroke_width=2,
        )
        v_label = safe_text("V", font_size=HEADING_SIZE, color=MATRIX_V)
        v_dim = safe_text("[r x n]", font_size=16, color=GRAY_B)

        # Position U and V with a multiply dot between them
        u_group = VGroup(u_rect, u_label, u_dim)
        u_label.move_to(u_rect)
        u_dim.next_to(u_rect, DOWN, buff=0.15)

        v_group = VGroup(v_rect, v_label, v_dim)
        v_label.move_to(v_rect)
        v_dim.next_to(v_rect, DOWN, buff=0.15)

        mult_dot = MathTex(r"\times", font_size=BODY_SIZE, color=WHITE)
        factors = VGroup(u_group, mult_dot, v_group).arrange(RIGHT, buff=0.4)
        factors.move_to(DOWN * 0.8)

        # Rank annotation
        rank_note = safe_text(
            "r << min(k, n)", font_size=LABEL_SIZE, color=ACCENT,
        ).next_to(factors, DOWN, buff=0.35)

        self.play(
            ReplacementTransform(w_rect, u_rect),
            ReplacementTransform(w_label, u_label),
            ReplacementTransform(w_dim, u_dim),
            FadeIn(v_group, shift=RIGHT * 0.3),
            FadeIn(mult_dot),
        )
        self.play(FadeIn(rank_note, shift=UP * 0.2))
        self.wait(HOLD_MEDIUM)

        # ── Phase 5: FadeOut equation and rank note, clear top area ──
        self.play(
            FadeOut(approx_eq),
            FadeOut(title),
            FadeOut(rank_note),
        )

        # ── Phase 6: Matmul transformation XW -> X*U*V ──
        subtitle = safe_text(
            "Matmul Transformation", font_size=HEADING_SIZE, color=WHITE,
        ).move_to(UP * TITLE_Y)
        self.play(Write(subtitle))

        # Move factors up a bit
        self.play(
            VGroup(u_group, mult_dot, v_group).animate.move_to(UP * 1.8),
        )

        # Build XW diagram
        x_rect_big = Rectangle(
            width=1.8, height=1.6,
            color=MATRIX_X, fill_opacity=0.3, stroke_width=2,
        )
        x_label_big = safe_text("X", font_size=HEADING_SIZE, color=MATRIX_X)
        x_label_big.move_to(x_rect_big)
        x_dim_big = safe_text("[m x k]", font_size=16, color=GRAY_B)
        x_dim_big.next_to(x_rect_big, DOWN, buff=0.15)
        x_group_big = VGroup(x_rect_big, x_label_big, x_dim_big)

        w2_rect = Rectangle(
            width=2.8, height=1.6,
            color=MATRIX_W, fill_opacity=0.3, stroke_width=2,
        )
        w2_label = safe_text("W", font_size=HEADING_SIZE, color=MATRIX_W)
        w2_label.move_to(w2_rect)
        w2_dim = safe_text("[k x n]", font_size=16, color=GRAY_B)
        w2_dim.next_to(w2_rect, DOWN, buff=0.15)
        w2_group = VGroup(w2_rect, w2_label, w2_dim)

        dot1 = MathTex(r"\times", font_size=BODY_SIZE, color=WHITE)
        eq_sign = MathTex("=", font_size=BODY_SIZE, color=WHITE)

        o_rect = Rectangle(
            width=2.8, height=1.6,
            color=SPEEDUP_YELLOW, fill_opacity=0.2, stroke_width=2,
        )
        o_label = safe_text("O", font_size=HEADING_SIZE, color=SPEEDUP_YELLOW)
        o_label.move_to(o_rect)
        o_dim = safe_text("[m x n]", font_size=16, color=GRAY_B)
        o_dim.next_to(o_rect, DOWN, buff=0.15)
        o_group = VGroup(o_rect, o_label, o_dim)

        old_matmul = VGroup(
            x_group_big, dot1, w2_group, eq_sign, o_group
        ).arrange(RIGHT, buff=0.3)
        old_matmul.move_to(DOWN * 0.5)

        self.play(FadeIn(old_matmul, shift=UP * 0.3))
        self.wait(HOLD_MEDIUM)

        # Show "1 big matmul" label
        big_label = safe_text(
            "One big matmul: mkn FLOPs",
            font_size=LABEL_SIZE, color=DANGER_RED,
        ).next_to(old_matmul, DOWN, buff=0.3)
        self.play(FadeIn(big_label, shift=UP * 0.1))
        self.wait(HOLD_SHORT)

        # ── Phase 7: Transform to two smaller matmuls ──
        # Build X * U * V layout
        x2_rect = Rectangle(
            width=1.4, height=1.4,
            color=MATRIX_X, fill_opacity=0.3, stroke_width=2,
        )
        x2_label = safe_text("X", font_size=HEADING_SIZE, color=MATRIX_X)
        x2_label.move_to(x2_rect)
        x2_dim = safe_text("[m x k]", font_size=16, color=GRAY_B)
        x2_dim.next_to(x2_rect, DOWN, buff=0.12)
        x2_group = VGroup(x2_rect, x2_label, x2_dim)

        u2_rect = Rectangle(
            width=0.8, height=1.4,
            color=MATRIX_U, fill_opacity=0.35, stroke_width=2,
        )
        u2_label = safe_text("U", font_size=HEADING_SIZE, color=MATRIX_U)
        u2_label.move_to(u2_rect)
        u2_dim = safe_text("[k x r]", font_size=16, color=GRAY_B)
        u2_dim.next_to(u2_rect, DOWN, buff=0.12)
        u2_group = VGroup(u2_rect, u2_label, u2_dim)

        v2_rect = Rectangle(
            width=2.0, height=0.8,
            color=MATRIX_V, fill_opacity=0.35, stroke_width=2,
        )
        v2_label = safe_text("V", font_size=HEADING_SIZE, color=MATRIX_V)
        v2_label.move_to(v2_rect)
        v2_dim = safe_text("[r x n]", font_size=16, color=GRAY_B)
        v2_dim.next_to(v2_rect, DOWN, buff=0.12)
        v2_group = VGroup(v2_rect, v2_label, v2_dim)

        dot2 = MathTex(r"\times", font_size=BODY_SIZE, color=WHITE)
        dot3 = MathTex(r"\times", font_size=BODY_SIZE, color=WHITE)
        eq2 = MathTex("=", font_size=BODY_SIZE, color=WHITE)

        o2_rect = Rectangle(
            width=2.0, height=1.4,
            color=SPEEDUP_YELLOW, fill_opacity=0.2, stroke_width=2,
        )
        o2_label = safe_text("O", font_size=HEADING_SIZE, color=SPEEDUP_YELLOW)
        o2_label.move_to(o2_rect)
        o2_dim = safe_text("[m x n]", font_size=16, color=GRAY_B)
        o2_dim.next_to(o2_rect, DOWN, buff=0.12)
        o2_group = VGroup(o2_rect, o2_label, o2_dim)

        new_matmul = VGroup(
            x2_group, dot2, u2_group, dot3, v2_group, eq2, o2_group
        ).arrange(RIGHT, buff=0.25)
        new_matmul.move_to(DOWN * 0.5)

        # Labels for two-step
        two_label = safe_text(
            "Two small matmuls: mkr + mrn FLOPs",
            font_size=LABEL_SIZE, color=SUCCESS_GREEN,
        ).next_to(new_matmul, DOWN, buff=0.3)

        self.play(
            FadeOut(old_matmul),
            FadeOut(big_label),
        )
        self.play(FadeIn(new_matmul, shift=UP * 0.3))
        self.play(FadeIn(two_label, shift=UP * 0.1))
        self.wait(HOLD_MEDIUM)

        # ── Phase 8: FLOPs comparison ──
        flops_text = safe_text(
            "mkn  -->  mkr + mrn  (savings when r << n)",
            font_size=BODY_SIZE, color=WHITE,
        ).move_to(UP * 0.4)

        self.play(
            VGroup(u_group, mult_dot, v_group).animate.set_opacity(DIM_OPACITY),
            new_matmul.animate.shift(DOWN * 0.4),
            two_label.animate.shift(DOWN * 0.4),
            FadeIn(flops_text, shift=DOWN * 0.2),
        )
        self.wait(HOLD_LONG)

        # ── Phase 9: Bottom note -- the catch ──
        note = bottom_note("But naive execution makes things WORSE...")
        self.play(FadeIn(note, shift=UP * 0.2))
        self.wait(HOLD_LONG)

        # ── Cleanup ──
        all_objs = [
            subtitle, u_group, mult_dot, v_group,
            new_matmul, two_label, flops_text, note,
        ]
        self.play(*[FadeOut(m) for m in all_objs])
        self.wait(0.3)
