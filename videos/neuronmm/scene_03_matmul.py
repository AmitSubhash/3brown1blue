"""Scene 03: Matrix Multiplication -- teach from scratch with real numbers.

Duration: ~120s
Template: FULL_CENTER
Audience: Curious learner (no ML/CS background)
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from utils.style import *


class MatrixMultiplyScene(Scene):
    """Teach matrix multiplication from scratch with animated dot products."""

    def _make_grid(
        self,
        values: list[list[int]],
        color: str,
        cell_size: float = 0.7,
    ) -> VGroup:
        """Create a grid of numbers with colored background cells."""
        rows = len(values)
        cols = len(values[0])
        grid = VGroup()

        w = cols * cell_size
        h = rows * cell_size
        bg = Rectangle(
            width=w + 0.2, height=h + 0.2,
            color=color, fill_opacity=0.1, stroke_width=2,
        )
        grid.add(bg)

        entries = VGroup()
        cells = VGroup()  # background cells for highlighting
        for r in range(rows):
            for c in range(cols):
                # Cell background
                cell_bg = Rectangle(
                    width=cell_size, height=cell_size,
                    color=color, fill_opacity=0.0, stroke_width=0.5,
                    stroke_opacity=0.3,
                )
                x = (c - (cols - 1) / 2) * cell_size
                y = ((rows - 1) / 2 - r) * cell_size
                cell_bg.move_to(bg.get_center() + RIGHT * x + UP * y)
                cells.add(cell_bg)

                num = safe_text(
                    str(values[r][c]),
                    font_size=22, color=WHITE,
                )
                num.move_to(cell_bg)
                entries.add(num)

        grid.add(cells)
        grid.add(entries)
        grid.entries = entries
        grid.cells = cells
        grid.bg = bg
        grid.vals = values
        grid.n_rows = rows
        grid.n_cols = cols
        grid.cell_size = cell_size
        return grid

    def construct(self) -> None:
        self.camera.background_color = BLACK

        # -- Title --
        title = safe_text(
            "Matrix Multiplication",
            font_size=TITLE_SIZE, color=WHITE,
        ).move_to(UP * TITLE_Y)
        self.play(Write(title), run_time=1.2)
        self.wait(HOLD_MEDIUM)

        # =====================================================
        # Phase 1: What is a matrix?
        # =====================================================
        whats_a = safe_text(
            "A matrix is just a grid of numbers",
            font_size=BODY_SIZE, color=WHITE,
        ).move_to(UP * 1.8)
        self.play(Write(whats_a), run_time=1.2)
        self.wait(HOLD_SHORT)

        demo_vals = [[2, 1, 0], [3, 0, 1], [1, 2, 1]]
        demo_grid = self._make_grid(demo_vals, CHIP_BLUE, cell_size=0.9)
        demo_grid.move_to(ORIGIN)

        # Row/column labels
        row_label = safe_text("rows", font_size=LABEL_SIZE, color=BASELINE_GRAY)
        row_label.next_to(demo_grid, LEFT, buff=0.4)
        col_label = safe_text("columns", font_size=LABEL_SIZE, color=BASELINE_GRAY)
        col_label.next_to(demo_grid, UP, buff=0.3)

        self.play(FadeIn(demo_grid, shift=UP * 0.2), run_time=1.2)
        self.wait(HOLD_SHORT)
        self.play(
            FadeIn(row_label, shift=RIGHT * 0.1),
            FadeIn(col_label, shift=DOWN * 0.1),
            run_time=0.8,
        )
        self.wait(HOLD_SHORT)

        analogy = safe_text(
            "Think of it as a spreadsheet",
            font_size=BODY_SIZE, color=BASELINE_GRAY,
        ).move_to(DOWN * 2.2)
        self.play(FadeIn(analogy, shift=UP * 0.1), run_time=0.8)
        self.wait(HOLD_LONG)

        # Fade phase 1
        self.play(
            FadeOut(whats_a), FadeOut(demo_grid),
            FadeOut(row_label), FadeOut(col_label), FadeOut(analogy),
            run_time=0.8,
        )

        # =====================================================
        # Phase 2: How multiply works -- the core visual
        # =====================================================
        a_vals = [[2, 1, 0], [3, 0, 1], [1, 2, 1]]
        b_vals = [[1, 0, 2], [3, 1, 0], [0, 2, 1]]

        grid_a = self._make_grid(a_vals, MATRIX_X, cell_size=0.8)
        grid_a.move_to(LEFT * 3.5 + DOWN * 0.3)
        label_a = safe_text("A (Input)", font_size=LABEL_SIZE, color=MATRIX_X)
        label_a.next_to(grid_a, UP, buff=0.25)

        grid_b = self._make_grid(b_vals, MATRIX_W, cell_size=0.8)
        grid_b.move_to(RIGHT * 0.0 + DOWN * 0.3)
        label_b = safe_text("B (Weights)", font_size=LABEL_SIZE, color=MATRIX_W)
        label_b.next_to(grid_b, UP, buff=0.25)

        times_sign = MathTex(
            r"\times", font_size=EQ_SIZE, color=WHITE,
        ).move_to(
            (grid_a.get_right() + grid_b.get_left()) / 2 + DOWN * 0.3
        )

        self.play(
            FadeIn(grid_a, shift=RIGHT * 0.3),
            Write(label_a),
            run_time=1.2,
        )
        self.play(
            FadeIn(grid_b, shift=LEFT * 0.3),
            Write(label_b),
            FadeIn(times_sign),
            run_time=1.2,
        )
        self.wait(HOLD_MEDIUM)

        # Output grid placeholder (empty)
        equals_sign = MathTex(
            "=", font_size=EQ_SIZE, color=WHITE,
        ).next_to(grid_b, RIGHT, buff=0.5).shift(DOWN * 0.0)

        out_grid_bg = Rectangle(
            width=2.6, height=2.6,
            color=SPEEDUP_YELLOW, fill_opacity=0.05, stroke_width=2,
        ).next_to(equals_sign, RIGHT, buff=0.5)

        label_out = safe_text("Output", font_size=LABEL_SIZE, color=SPEEDUP_YELLOW)
        label_out.next_to(out_grid_bg, UP, buff=0.25)

        self.play(
            FadeIn(equals_sign),
            FadeIn(out_grid_bg, shift=LEFT * 0.2),
            FadeIn(label_out),
            run_time=0.8,
        )
        self.wait(HOLD_SHORT)

        # Highlight row 0 of A (entries 0,1,2) and col 0 of B (entries 0,3,6)
        row0_entries = VGroup(*[grid_a.entries[j] for j in range(3)])
        col0_entries = VGroup(*[grid_b.entries[j * 3] for j in range(3)])

        row_hl = SurroundingRectangle(
            row0_entries, color=MATRIX_X, buff=0.08, stroke_width=3,
        )
        col_hl = SurroundingRectangle(
            col0_entries, color=MATRIX_W, buff=0.08, stroke_width=3,
        )

        self.play(Create(row_hl), Create(col_hl), run_time=0.8)
        self.wait(HOLD_SHORT)

        # Step-by-step dot product animation
        calc_y = DOWN * 2.5
        step1 = safe_text("2 x 1", font_size=BODY_SIZE, color=WHITE)
        step1.move_to(LEFT * 3.0 + calc_y)
        self.play(Write(step1), run_time=0.8)
        self.wait(0.5)

        plus1 = safe_text("+", font_size=BODY_SIZE, color=WHITE)
        plus1.next_to(step1, RIGHT, buff=0.2)
        step2 = safe_text("1 x 3", font_size=BODY_SIZE, color=WHITE)
        step2.next_to(plus1, RIGHT, buff=0.2)
        self.play(FadeIn(plus1), Write(step2), run_time=0.8)
        self.wait(0.5)

        plus2 = safe_text("+", font_size=BODY_SIZE, color=WHITE)
        plus2.next_to(step2, RIGHT, buff=0.2)
        step3 = safe_text("0 x 0", font_size=BODY_SIZE, color=WHITE)
        step3.next_to(plus2, RIGHT, buff=0.2)
        self.play(FadeIn(plus2), Write(step3), run_time=0.8)
        self.wait(0.5)

        eq_sign = safe_text("=", font_size=BODY_SIZE, color=WHITE)
        eq_sign.next_to(step3, RIGHT, buff=0.3)
        result = safe_text("5", font_size=HEADING_SIZE, color=SPEEDUP_YELLOW)
        result.next_to(eq_sign, RIGHT, buff=0.3)
        self.play(FadeIn(eq_sign), FadeIn(result, scale=0.7), run_time=0.8)
        self.wait(HOLD_SHORT)

        # Place result in output grid cell [0,0]
        out_cell_00 = safe_text(
            "5", font_size=22, color=SPEEDUP_YELLOW,
        ).move_to(
            out_grid_bg.get_center()
            + LEFT * 0.8 + UP * 0.8
        )
        self.play(FadeIn(out_cell_00, scale=0.5), run_time=0.6)

        calc_group = VGroup(step1, plus1, step2, plus2, step3, eq_sign, result)

        explain = safe_text(
            "We multiply matching pairs and add them up",
            font_size=BODY_SIZE, color=WHITE,
        ).move_to(DOWN * 2.5)

        self.play(FadeOut(calc_group), run_time=0.5)
        self.play(Write(explain), run_time=1.2)
        self.wait(HOLD_MEDIUM)

        one_num = safe_text(
            "That gives us ONE number in the output",
            font_size=BODY_SIZE, color=BASELINE_GRAY,
        ).move_to(DOWN * 3.0)
        self.play(FadeIn(one_num, shift=UP * 0.1), run_time=0.8)
        self.wait(HOLD_LONG)

        self.play(
            FadeOut(row_hl), FadeOut(col_hl),
            FadeOut(explain), FadeOut(one_num),
            run_time=0.6,
        )

        # =====================================================
        # Phase 3: Fill remaining cells quickly
        # =====================================================
        # Precompute actual results for A*B:
        # Row 0: [5, 1, 4], Row 1: [3, 2, 7], Row 2: [7, 4, 3]
        output_vals = [
            [5, 1, 4],
            [3, 2, 7],
            [7, 4, 3],
        ]
        out_cells: list[Text] = [out_cell_00]

        for r in range(3):
            for c in range(3):
                if r == 0 and c == 0:
                    continue  # already placed
                # Brief highlight of the row and column
                row_entries = VGroup(
                    *[grid_a.entries[r * 3 + j] for j in range(3)]
                )
                col_entries_b = VGroup(
                    *[grid_b.entries[j * 3 + c] for j in range(3)]
                )
                row_flash = SurroundingRectangle(
                    row_entries, color=MATRIX_X, buff=0.06, stroke_width=2,
                )
                col_flash = SurroundingRectangle(
                    col_entries_b, color=MATRIX_W, buff=0.06, stroke_width=2,
                )

                x_off = (c - 1) * 0.8
                y_off = (1 - r) * 0.8
                cell = safe_text(
                    str(output_vals[r][c]),
                    font_size=22, color=SPEEDUP_YELLOW,
                ).move_to(
                    out_grid_bg.get_center()
                    + RIGHT * x_off + UP * y_off
                )

                self.play(
                    Create(row_flash), Create(col_flash),
                    run_time=0.25,
                )
                self.play(
                    FadeIn(cell, scale=0.5),
                    FadeOut(row_flash), FadeOut(col_flash),
                    run_time=0.3,
                )
                out_cells.append(cell)

        self.wait(HOLD_SHORT)

        summary = safe_text(
            "9 output numbers, each needing 3 multiplications",
            font_size=BODY_SIZE, color=WHITE,
        ).move_to(DOWN * 2.5)
        self.play(Write(summary), run_time=1.2)
        self.wait(HOLD_LONG)

        # =====================================================
        # Phase 4: Scale up to LLM size
        # =====================================================
        all_grids = VGroup(
            grid_a, label_a, grid_b, label_b,
            times_sign, equals_sign, out_grid_bg, label_out,
            *out_cells, summary,
        )
        self.play(FadeOut(all_grids), FadeOut(title), run_time=0.8)

        scale_title = safe_text(
            "Now scale that up...",
            font_size=TITLE_SIZE, color=WHITE,
        ).move_to(UP * TITLE_Y)
        self.play(Write(scale_title), run_time=1.0)
        self.wait(HOLD_SHORT)

        # Small matrix grows into enormous one
        small_box = Rectangle(
            width=1.0, height=1.0,
            color=MATRIX_X, fill_opacity=0.15, stroke_width=2,
        ).move_to(LEFT * 0.0 + UP * 0.3)

        small_label = safe_text(
            "3 x 3", font_size=LABEL_SIZE, color=MATRIX_X,
        ).next_to(small_box, DOWN, buff=0.2)

        self.play(FadeIn(small_box), Write(small_label), run_time=0.8)
        self.wait(HOLD_SHORT)

        # Grow to big box
        big_box = Rectangle(
            width=4.5, height=4.5,
            color=MATRIX_X, fill_opacity=0.06, stroke_width=2,
        ).move_to(LEFT * 0.0 + DOWN * 0.1)

        big_label = safe_text(
            "4,096 x 4,096", font_size=HEADING_SIZE, color=MATRIX_X,
        ).next_to(big_box, DOWN, buff=0.2)

        # Add tiny grid lines inside for effect
        grid_lines = VGroup()
        for i in range(1, 12):
            frac = i / 12
            h_line = Line(
                big_box.get_left() + UP * (big_box.height / 2 - frac * big_box.height),
                big_box.get_right() + UP * (big_box.height / 2 - frac * big_box.height),
                color=MATRIX_X, stroke_width=0.3, stroke_opacity=0.3,
            )
            v_line = Line(
                big_box.get_top() + RIGHT * (-big_box.width / 2 + frac * big_box.width),
                big_box.get_bottom() + RIGHT * (-big_box.width / 2 + frac * big_box.width),
                color=MATRIX_X, stroke_width=0.3, stroke_opacity=0.3,
            )
            grid_lines.add(h_line, v_line)

        self.play(
            Transform(small_box, big_box),
            Transform(small_label, big_label),
            run_time=2.5,
            rate_func=smooth,
        )
        self.play(FadeIn(grid_lines, run_time=0.8))
        self.wait(HOLD_SHORT)

        # Big number reveal
        millions = safe_text(
            "16 MILLION multiplications",
            font_size=HEADING_SIZE, color=DANGER_RED,
        ).move_to(UP * TITLE_Y)

        self.play(FadeOut(scale_title), run_time=0.3)
        self.play(Write(millions), run_time=1.5)
        self.wait(HOLD_MEDIUM)

        dozens = safe_text(
            "And each word prediction needs DOZENS of these",
            font_size=BODY_SIZE, color=SPEEDUP_YELLOW,
        ).move_to(DOWN * 2.8)
        self.play(Write(dozens), run_time=1.5)
        self.wait(HOLD_LONG)

        # -- Bottom note --
        note = bottom_note(
            "Matrix multiplication: multiply rows by columns, add up the results"
        )
        self.play(FadeIn(note, shift=UP * 0.2), run_time=0.8)
        self.wait(HOLD_LONG)

        # -- Cleanup --
        fade_all(
            self, small_box, small_label, grid_lines,
            millions, dozens, note,
        )
        self.wait(0.5)
