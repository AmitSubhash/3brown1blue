"""Scene 12: SVD Explained -- Intuitive SVD, then applied to matrix multiply.

Duration: ~90s
Template: FULL_CENTER
Audience: Curious learner
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from utils.style import *


class SVDExplainedScene(Scene):
    """Teach SVD at an intuitive level, then connect to optimization."""

    def construct(self) -> None:
        self.camera.background_color = BLACK

        # -- Title --
        title = section_title("SVD: Splitting Big Matrices")
        self.play(Write(title), run_time=1.2)
        self.wait(2)

        # ===== Phase 1: The intuition =====
        # Big weight matrix
        big_w = Rectangle(
            width=4.0, height=3.5,
            color=MATRIX_W, fill_opacity=0.25, stroke_width=2,
        ).move_to(DOWN * 0.2)
        w_label = safe_text("W", font_size=HEADING_SIZE, color=MATRIX_W)
        w_label.move_to(big_w)
        w_dim = safe_text(
            "[4096 x 4096]", font_size=LABEL_SIZE, color=GRAY_B,
        ).next_to(big_w, DOWN, buff=0.2)
        w_count = safe_text(
            "16 million numbers", font_size=BODY_SIZE, color=WHITE,
        ).next_to(w_dim, DOWN, buff=0.15)

        self.play(
            FadeIn(big_w, shift=UP * 0.2), FadeIn(w_label),
            Write(w_dim), Write(w_count),
            run_time=1.3,
        )
        self.wait(2)

        # "What if most numbers are redundant?"
        redundant = safe_text(
            "What if most of these numbers are... redundant?",
            font_size=BODY_SIZE, color=ACCENT,
        ).move_to(DOWN * 2.8)
        self.play(Write(redundant), run_time=1.3)
        self.wait(2)

        # Dim most of the matrix, highlight a thin vertical slice
        # Create a thin highlighted strip overlaid on the matrix
        thin_strip = Rectangle(
            width=0.5, height=3.5,
            color=ACCENT, fill_opacity=0.4, stroke_width=2,
        ).move_to(big_w.get_center())

        self.play(
            big_w.animate.set_fill(opacity=DIM_OPACITY),
            FadeIn(thin_strip),
            run_time=1.3,
        )

        concentrated = safe_text(
            "The important info is concentrated",
            font_size=BODY_SIZE, color=ACCENT,
        ).move_to(redundant.get_center())
        self.play(FadeOut(redundant), FadeIn(concentrated, shift=UP * 0.15), run_time=1.0)
        self.wait(2)

        finds = safe_text(
            "SVD finds this concentrated structure",
            font_size=BODY_SIZE, color=WHITE,
        ).move_to(concentrated.get_center())
        self.play(FadeOut(concentrated), FadeIn(finds, shift=UP * 0.15), run_time=1.0)
        self.wait(2)

        # Fade Phase 1
        fade_all(self, big_w, w_label, w_dim, w_count, thin_strip, finds)

        # ===== Phase 2: The split =====
        # Animate big matrix splitting into U and V
        # Start with the big matrix again in center
        w_rect = Rectangle(
            width=3.5, height=3.0,
            color=MATRIX_W, fill_opacity=0.25, stroke_width=2,
        ).move_to(ORIGIN + UP * 0.3)
        w_txt = safe_text("W", font_size=HEADING_SIZE, color=MATRIX_W)
        w_txt.move_to(w_rect)

        self.play(FadeIn(w_rect, shift=UP * 0.2), FadeIn(w_txt), run_time=1.0)
        self.wait(1.5)

        # Target: U (tall thin) on left, V (short wide) on right
        u_rect = Rectangle(
            width=1.2, height=3.0,
            color=MATRIX_U, fill_opacity=0.3, stroke_width=2,
        )
        u_txt = safe_text("U", font_size=HEADING_SIZE, color=MATRIX_U)
        u_dim = safe_text("[4096 x 256]", font_size=18, color=GRAY_B)

        v_rect = Rectangle(
            width=3.0, height=1.0,
            color=MATRIX_V, fill_opacity=0.3, stroke_width=2,
        )
        v_txt = safe_text("V", font_size=HEADING_SIZE, color=MATRIX_V)
        v_dim = safe_text("[256 x 4096]", font_size=18, color=GRAY_B)

        # Position U and V
        u_group = VGroup(u_rect, u_txt, u_dim)
        u_rect.move_to(LEFT * 2.5 + UP * 0.3)
        u_txt.move_to(u_rect)
        u_dim.next_to(u_rect, DOWN, buff=0.15)

        v_group = VGroup(v_rect, v_txt, v_dim)
        v_rect.move_to(RIGHT * 2.5 + UP * 0.3)
        v_txt.move_to(v_rect)
        v_dim.next_to(v_rect, DOWN, buff=0.15)

        # Multiplication sign between
        times_sign = MathTex(r"\times", font_size=EQ_SIZE, color=WHITE)
        times_sign.move_to(ORIGIN + UP * 0.3)

        # Approximately equal sign above
        approx_eq = MathTex(r"W \approx U \times V", font_size=EQ_SIZE)
        approx_eq.set_color_by_tex("W", MATRIX_W)
        approx_eq.set_color_by_tex("U", MATRIX_U)
        approx_eq.set_color_by_tex("V", MATRIX_V)
        approx_eq.next_to(title, DOWN, buff=0.3)

        # Animate the split
        self.play(
            ReplacementTransform(w_rect, u_rect),
            ReplacementTransform(w_txt, u_txt),
            run_time=1.5,
        )
        self.play(
            FadeIn(v_rect, shift=LEFT * 0.3),
            FadeIn(v_txt),
            FadeIn(times_sign),
            run_time=1.2,
        )
        self.play(
            Write(u_dim), Write(v_dim),
            Write(approx_eq),
            run_time=1.3,
        )
        self.wait(2)

        # Compression stat
        compression = safe_multiline(
            "Instead of 16 million numbers, we store ~2 million",
            "That's an 8x compression!",
            font_size=BODY_SIZE, color=SUCCESS_GREEN, line_buff=0.3,
        ).move_to(DOWN * 2.0)
        self.play(Write(compression[0]), run_time=1.3)
        self.play(Write(compression[1]), run_time=1.2)
        self.wait(3)

        # Fade Phase 2
        fade_all(
            self, u_rect, u_txt, u_dim, v_rect, v_txt, v_dim,
            times_sign, approx_eq, compression,
        )

        # ===== Phase 3: Applied to matrix multiply =====
        self.play(FadeOut(title))
        phase3_title = section_title("SVD Applied to Matrix Multiply")
        self.play(Write(phase3_title), run_time=1.2)
        self.wait(2)

        # X * W (one big multiply)
        remind = safe_text(
            "The LLM computes X * W for every word",
            font_size=BODY_SIZE, color=WHITE,
        ).next_to(phase3_title, DOWN, buff=0.4)
        self.play(Write(remind), run_time=1.3)
        self.wait(2)

        # Show X * W as big operation
        x_box = matrix_rect("X", 128, 4096, MATRIX_X, width=1.2, height=1.5)
        times1 = MathTex(r"\times", font_size=EQ_SIZE, color=WHITE)
        w_box = matrix_rect("W", 4096, 4096, MATRIX_W, width=2.0, height=1.5)

        big_op = VGroup(x_box, times1, w_box).arrange(RIGHT, buff=0.4)
        big_op.move_to(UP * 0.0)

        expensive_label = safe_text(
            "Expensive!", font_size=BODY_SIZE, color=DANGER_RED,
        ).next_to(big_op, DOWN, buff=0.3)

        self.play(
            FadeIn(x_box, shift=UP * 0.2),
            FadeIn(times1),
            FadeIn(w_box, shift=UP * 0.2),
            run_time=1.2,
        )
        self.play(Write(expensive_label), run_time=1.0)
        self.wait(2)

        # Transform to X * U * V (two smaller multiplies)
        x_box2 = matrix_rect("X", 128, 4096, MATRIX_X, width=1.0, height=1.3)
        times2a = MathTex(r"\times", font_size=EQ_SIZE, color=WHITE)
        u_box = matrix_rect("U", 4096, 256, MATRIX_U, width=0.8, height=1.3)
        times2b = MathTex(r"\times", font_size=EQ_SIZE, color=WHITE)
        v_box = matrix_rect("V", 256, 4096, MATRIX_V, width=1.5, height=0.7)

        small_op = VGroup(x_box2, times2a, u_box, times2b, v_box).arrange(RIGHT, buff=0.3)
        small_op.move_to(UP * 0.0)

        cheaper_label = safe_text(
            "Cheaper!", font_size=BODY_SIZE, color=SUCCESS_GREEN,
        ).next_to(small_op, DOWN, buff=0.3)

        self.play(
            FadeOut(big_op), FadeOut(expensive_label),
            run_time=0.8,
        )
        self.play(
            FadeIn(small_op, shift=UP * 0.2),
            Write(cheaper_label),
            run_time=1.3,
        )
        self.wait(2)

        # FLOPs comparison
        flops = safe_multiline(
            "16 billion -> 4 billion operations",
            "Two small multiplies beat one huge one",
            font_size=BODY_SIZE, color=WHITE, line_buff=0.3,
        ).move_to(DOWN * 2.0)
        self.play(Write(flops[0]), run_time=1.2)
        self.play(Write(flops[1]), run_time=1.2)
        self.wait(3)

        # Fade Phase 3
        fade_all(self, phase3_title, remind, small_op, cheaper_label, flops)

        # ===== Phase 4: The catch =====
        catch_title = safe_text(
            "Sounds great... but there's a problem",
            font_size=HEADING_SIZE, color=ACCENT,
        ).move_to(UP * 1.0)
        self.play(Write(catch_title), run_time=1.3)
        self.wait(2)

        catch_detail = safe_text(
            "The intermediate result (X * U) creates extra data movement",
            font_size=BODY_SIZE, color=WHITE,
        ).next_to(catch_title, DOWN, buff=0.5)
        self.play(Write(catch_detail), run_time=1.5)
        self.wait(2)

        # Show intermediate: X*U produces Y, then Y must be stored
        x_small = matrix_rect("X", 128, 4096, MATRIX_X, width=0.8, height=1.0)
        t_sign = MathTex(r"\times", font_size=SMALL_EQ, color=WHITE)
        u_small = matrix_rect("U", 4096, 256, MATRIX_U, width=0.6, height=1.0)
        eq_sign = MathTex(r"=", font_size=SMALL_EQ, color=WHITE)
        y_result = matrix_rect("Y", 128, 256, MATRIX_Y, width=0.7, height=0.8)

        intermediate_chain = VGroup(
            x_small, t_sign, u_small, eq_sign, y_result,
        ).arrange(RIGHT, buff=0.25)
        intermediate_chain.move_to(DOWN * 1.0)

        # "Y must be stored" arrow to HBM
        store_label = safe_text(
            "Must store Y in memory!", font_size=LABEL_SIZE, color=DANGER_RED,
        ).next_to(y_result, DOWN, buff=0.3)

        self.play(FadeIn(intermediate_chain, shift=UP * 0.2), run_time=1.2)
        self.play(Write(store_label), run_time=1.0)
        self.wait(3)

        # Bottom note
        note = bottom_note(
            "SVD: factoring a matrix into two smaller, more manageable pieces"
        )
        self.play(FadeIn(note, shift=UP * 0.2), run_time=1.2)
        self.wait(3)

        # Cleanup
        fade_all(
            self, catch_title, catch_detail,
            intermediate_chain, store_label, note,
        )
