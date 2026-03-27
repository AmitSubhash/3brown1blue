"""Scene 11: Trainium Constraints -- Tile sizes, transpose, SBUF limits.

Duration: ~60s
Template: FULL_CENTER
Audience: Curious learner
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from utils.style import *


class TrainiumConstraintsScene(Scene):
    """Explain Trainium's specific constraints that make optimization hard."""

    def construct(self) -> None:
        self.camera.background_color = BLACK

        # -- Title --
        title = section_title("Trainium's Rules")
        self.play(Write(title), run_time=1.2)
        self.wait(2)

        # ===== Phase 1: Tile size constraint =====
        phase1_label = safe_text(
            "Rule 1: Data must be tiled",
            font_size=HEADING_SIZE, color=CHIP_BLUE,
        ).next_to(title, DOWN, buff=0.4)
        self.play(Write(phase1_label), run_time=1.2)
        self.wait(2)

        # Show 128x128 systolic array
        array_rect = RoundedRectangle(
            width=2.0, height=2.0, corner_radius=0.1,
            color=CHIP_BLUE, fill_opacity=0.15, stroke_width=2,
        ).move_to(LEFT * 3.5 + DOWN * 0.5)
        array_label = safe_text(
            "128 x 128", font_size=LABEL_SIZE, color=CHIP_BLUE,
        ).move_to(array_rect)
        array_sub = safe_text(
            "Systolic Array", font_size=16, color=GRAY_B,
        ).next_to(array_rect, DOWN, buff=0.15)

        self.play(
            FadeIn(array_rect, shift=UP * 0.2),
            FadeIn(array_label),
            FadeIn(array_sub),
            run_time=1.2,
        )

        # Big matrix on the right
        big_matrix = Rectangle(
            width=4.0, height=3.0,
            color=MATRIX_W, fill_opacity=0.2, stroke_width=2,
        ).move_to(RIGHT * 1.5 + DOWN * 0.5)
        big_label = safe_text(
            "Big Matrix", font_size=BODY_SIZE, color=MATRIX_W,
        ).move_to(big_matrix.get_center() + UP * 0.3)
        big_dim = safe_text(
            "[4096 x 4096]", font_size=LABEL_SIZE, color=GRAY_B,
        ).next_to(big_label, DOWN, buff=0.15)

        self.play(
            FadeIn(big_matrix, shift=UP * 0.2),
            Write(big_label),
            Write(big_dim),
            run_time=1.2,
        )
        self.wait(2)

        # Cut into tiles with grid lines
        tile_desc = safe_text(
            "Cut into 128 x 128 tiles, like cutting a sheet into squares",
            font_size=LABEL_SIZE, color=ACCENT,
        ).move_to(DOWN * 2.8)
        self.play(Write(tile_desc), run_time=1.3)

        # Draw grid lines on the big matrix (4 divisions = 3 lines each way)
        grid_lines = VGroup()
        for i in range(1, 4):
            frac = i / 4
            # Vertical lines
            x = big_matrix.get_left()[0] + frac * big_matrix.width
            vline = Line(
                [x, big_matrix.get_top()[1], 0],
                [x, big_matrix.get_bottom()[1], 0],
                color=ACCENT, stroke_width=1.5,
            )
            grid_lines.add(vline)
            # Horizontal lines
            y = big_matrix.get_bottom()[1] + frac * big_matrix.height
            hline = Line(
                [big_matrix.get_left()[0], y, 0],
                [big_matrix.get_right()[0], y, 0],
                color=ACCENT, stroke_width=1.5,
            )
            grid_lines.add(hline)

        self.play(Create(grid_lines), run_time=1.5)
        self.wait(3)

        # Fade Phase 1
        fade_all(
            self, phase1_label, array_rect, array_label, array_sub,
            big_matrix, big_label, big_dim, tile_desc, grid_lines,
        )

        # ===== Phase 2: Transpose requirement =====
        phase2_label = safe_text(
            "Rule 2: Stationary matrix must be transposed",
            font_size=HEADING_SIZE, color=DMA_ORANGE,
        ).next_to(title, DOWN, buff=0.4)
        self.play(Write(phase2_label), run_time=1.3)
        self.wait(2)

        # Show a small 3x2 matrix with visible entries
        # Original matrix
        orig_entries = [
            ["a", "b"],
            ["c", "d"],
            ["e", "f"],
        ]
        orig_group = VGroup()
        cell_size = 0.6
        for r, row in enumerate(orig_entries):
            for c, val in enumerate(row):
                cell = Square(
                    side_length=cell_size,
                    color=MATRIX_W, fill_opacity=0.15, stroke_width=1.5,
                ).move_to(
                    LEFT * 2.5 + RIGHT * c * cell_size + DOWN * r * cell_size
                )
                label = safe_text(val, font_size=20, color=MATRIX_W)
                label.move_to(cell)
                orig_group.add(VGroup(cell, label))

        orig_group.move_to(LEFT * 2.0 + DOWN * 0.3)
        orig_title = safe_text(
            "Original (3x2)", font_size=LABEL_SIZE, color=MATRIX_W,
        ).next_to(orig_group, UP, buff=0.2)

        self.play(FadeIn(orig_group, shift=UP * 0.2), Write(orig_title), run_time=1.2)
        self.wait(2)

        # Arrow
        transpose_arrow = Arrow(
            orig_group.get_right() + RIGHT * 0.3,
            orig_group.get_right() + RIGHT * 2.0,
            color=ACCENT, stroke_width=3,
        )
        rotate_label = safe_text(
            "Transpose", font_size=LABEL_SIZE, color=ACCENT,
        ).next_to(transpose_arrow, UP, buff=0.1)
        self.play(Create(transpose_arrow), Write(rotate_label), run_time=1.2)

        # Transposed matrix (2x3)
        trans_entries = [
            ["a", "c", "e"],
            ["b", "d", "f"],
        ]
        trans_group = VGroup()
        for r, row in enumerate(trans_entries):
            for c, val in enumerate(row):
                cell = Square(
                    side_length=cell_size,
                    color=DMA_ORANGE, fill_opacity=0.15, stroke_width=1.5,
                ).move_to(
                    RIGHT * 2.5 + RIGHT * c * cell_size + DOWN * r * cell_size
                )
                label = safe_text(val, font_size=20, color=DMA_ORANGE)
                label.move_to(cell)
                trans_group.add(VGroup(cell, label))

        trans_group.move_to(RIGHT * 2.5 + DOWN * 0.3)
        trans_title = safe_text(
            "Transposed (2x3)", font_size=LABEL_SIZE, color=DMA_ORANGE,
        ).next_to(trans_group, UP, buff=0.2)

        self.play(FadeIn(trans_group, shift=LEFT * 0.2), Write(trans_title), run_time=1.2)
        self.wait(2)

        analogy = safe_text(
            "Like flipping a page before reading it -- takes time and memory",
            font_size=BODY_SIZE, color=WHITE,
        ).move_to(DOWN * 2.5)
        self.play(Write(analogy), run_time=1.3)
        self.wait(3)

        # Fade Phase 2
        fade_all(
            self, phase2_label, orig_group, orig_title,
            transpose_arrow, rotate_label,
            trans_group, trans_title, analogy,
        )

        # ===== Phase 3: SBUF is the bottleneck =====
        phase3_label = safe_text(
            "Rule 3: Only 24 MB of fast memory",
            font_size=HEADING_SIZE, color=SBUF_GREEN,
        ).next_to(title, DOWN, buff=0.4)
        self.play(Write(phase3_label), run_time=1.3)
        self.wait(2)

        # SBUF rectangle with capacity bar
        sbuf_rect = RoundedRectangle(
            width=5.0, height=2.0, corner_radius=0.15,
            color=SBUF_GREEN, fill_opacity=0.1, stroke_width=2,
        ).move_to(UP * 0.0)
        sbuf_label = safe_text(
            "SBUF: 24 MB", font_size=HEADING_SIZE, color=SBUF_GREEN,
        ).move_to(sbuf_rect.get_center() + UP * 0.3)

        # Capacity bar inside
        bar_bg = Rectangle(
            width=4.0, height=0.4,
            color=GRAY, fill_opacity=0.1, stroke_width=1,
        ).move_to(sbuf_rect.get_center() + DOWN * 0.4)
        bar_fill = Rectangle(
            width=4.0, height=0.4,
            color=SBUF_GREEN, fill_opacity=0.3, stroke_width=0,
        ).move_to(bar_bg)

        self.play(
            FadeIn(sbuf_rect, shift=UP * 0.2),
            Write(sbuf_label),
            FadeIn(bar_bg), FadeIn(bar_fill),
            run_time=1.2,
        )
        self.wait(2)

        # "If data doesn't fit..."
        fit_text = safe_text(
            "If your data doesn't fit, it spills to HBM",
            font_size=BODY_SIZE, color=WHITE,
        ).move_to(DOWN * 1.5)
        self.play(Write(fit_text), run_time=1.3)
        self.wait(2)

        # Overflow animation: bar overfills, red spillover
        overflow_bar = Rectangle(
            width=1.5, height=0.4,
            color=DANGER_RED, fill_opacity=0.5, stroke_width=0,
        )
        overflow_bar.next_to(bar_bg, RIGHT, buff=0.0)

        spill_label = safe_text(
            "SPILL!", font_size=LABEL_SIZE, color=DANGER_RED,
        ).next_to(overflow_bar, UP, buff=0.15)

        hbm_indicator = safe_text(
            "-> HBM (slow!)", font_size=LABEL_SIZE, color=DANGER_RED,
        ).next_to(overflow_bar, RIGHT, buff=0.2)

        self.play(
            FadeIn(overflow_bar, shift=LEFT * 0.3),
            FadeIn(spill_label),
            FadeIn(hbm_indicator),
            bar_fill.animate.set_color(SPEEDUP_YELLOW),
            run_time=1.3,
        )
        self.wait(2)

        conclusion = safe_text(
            "Spilling = slow. We MUST keep data within 24 MB.",
            font_size=BODY_SIZE, color=ACCENT,
        ).move_to(DOWN * 2.3)
        self.play(Write(conclusion), run_time=1.3)
        self.wait(3)

        # Bottom note
        note = bottom_note(
            "Every optimization must respect: tile sizes, transpose rules, and 24 MB SBUF limit"
        )
        self.play(FadeIn(note, shift=UP * 0.2), run_time=1.2)
        self.wait(3)

        # Cleanup
        fade_all(
            self, title, phase3_label, sbuf_rect, sbuf_label,
            bar_bg, bar_fill, overflow_bar, spill_label,
            hbm_indicator, fit_text, conclusion, note,
        )
