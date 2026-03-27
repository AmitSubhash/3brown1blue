"""Scene 10: Inside Trainium -- Systolic array, memory hierarchy, data flow.

Duration: ~120s
Template: FULL_CENTER
Audience: Curious learner
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from utils.style import *


class InsideTrainiumScene(Scene):
    """Deep dive into Trainium architecture with full data flow animation."""

    def construct(self) -> None:
        self.camera.background_color = BLACK

        # -- Title --
        title = section_title("Inside Trainium")
        self.play(Write(title), run_time=1.2)
        self.wait(2)

        # ===== Phase 1: The Systolic Array =====
        intro = safe_text(
            "The heart of Trainium: the systolic array",
            font_size=BODY_SIZE, color=CHIP_BLUE,
        ).next_to(title, DOWN, buff=0.4)
        self.play(Write(intro), run_time=1.3)
        self.wait(2)

        # Build a 4x4 grid of circles (MACs)
        GRID_N = 4
        CELL_RAD = 0.22
        CELL_BUFF = 0.65
        grid_cells: list[list[Circle]] = []
        grid_group = VGroup()

        for r in range(GRID_N):
            row: list[Circle] = []
            for c in range(GRID_N):
                cell = Circle(
                    radius=CELL_RAD, color=CHIP_BLUE,
                    fill_opacity=0.15, stroke_width=2,
                )
                cell.move_to(
                    LEFT * ((GRID_N - 1) / 2 - c) * CELL_BUFF
                    + UP * ((GRID_N - 1) / 2 - r) * CELL_BUFF
                )
                row.append(cell)
                grid_group.add(cell)
            grid_cells.append(row)

        grid_group.move_to(DOWN * 0.5)
        self.play(FadeIn(grid_group, shift=UP * 0.2), run_time=1.2)

        cell_label = safe_text(
            "Each cell: multiply and pass to neighbor",
            font_size=LABEL_SIZE, color=GRAY_B,
        ).next_to(grid_group, DOWN, buff=0.35)
        self.play(Write(cell_label), run_time=1.2)
        self.wait(2)

        # Animate data flowing through the grid like a wave
        # Row data from left, column data from top
        for wave in range(GRID_N):
            pulse_anims = []
            for r in range(GRID_N):
                c = wave - r
                if 0 <= c < GRID_N:
                    pulse_anims.append(
                        grid_cells[r][c].animate.set_fill(ACCENT, opacity=0.6)
                    )
            if pulse_anims:
                self.play(*pulse_anims, run_time=0.4)

        # Second pass to show diagonal wave continuing
        for wave in range(GRID_N, 2 * GRID_N - 1):
            pulse_anims = []
            for r in range(GRID_N):
                c = wave - r
                if 0 <= c < GRID_N:
                    pulse_anims.append(
                        grid_cells[r][c].animate.set_fill(ACCENT, opacity=0.6)
                    )
            # Fade previous wave
            fade_anims = []
            for r in range(GRID_N):
                c = wave - r - GRID_N
                if 0 <= c < GRID_N:
                    fade_anims.append(
                        grid_cells[r][c].animate.set_fill(CHIP_BLUE, opacity=0.15)
                    )
            if pulse_anims or fade_anims:
                self.play(*(pulse_anims + fade_anims), run_time=0.4)

        # Reset all cells
        self.play(
            *[
                grid_cells[r][c].animate.set_fill(CHIP_BLUE, opacity=0.15)
                for r in range(GRID_N) for c in range(GRID_N)
            ],
            run_time=0.5,
        )

        wave_label = safe_text(
            "Like a wave of computation flowing through",
            font_size=BODY_SIZE, color=WHITE,
        ).next_to(cell_label, DOWN, buff=0.3)
        self.play(Write(wave_label), run_time=1.2)
        self.wait(2)

        # Scale reveal
        scale_text = safe_text(
            "Real array: 128 x 128 = 16,384 units!",
            font_size=BODY_SIZE, color=ACCENT,
        ).move_to(wave_label.get_center())
        self.play(
            FadeOut(wave_label),
            FadeIn(scale_text, shift=UP * 0.2),
            run_time=1.2,
        )

        # Zoom out effect: shrink grid, add surrounding grid hint
        big_grid_rect = RoundedRectangle(
            width=5.0, height=3.5, corner_radius=0.15,
            color=CHIP_BLUE, fill_opacity=0.08, stroke_width=2,
        ).move_to(grid_group.get_center())
        big_label = safe_text(
            "128 x 128", font_size=HEADING_SIZE, color=CHIP_BLUE,
        ).move_to(big_grid_rect)

        self.play(
            grid_group.animate.scale(0.15).set_opacity(0.3),
            FadeIn(big_grid_rect),
            FadeIn(big_label),
            run_time=1.5,
        )
        self.wait(3)

        # Fade Phase 1
        fade_all(
            self, title, intro, cell_label, scale_text,
            grid_group, big_grid_rect, big_label,
        )

        # ===== Phase 2: The Memory Hierarchy =====
        mem_title = section_title("Trainium Memory Hierarchy")
        self.play(Write(mem_title), run_time=1.2)
        self.wait(2)

        analogy_text = safe_text(
            "Like a kitchen: from warehouse to chef's plate",
            font_size=BODY_SIZE, color=ACCENT,
        ).next_to(mem_title, DOWN, buff=0.3)
        self.play(Write(analogy_text), run_time=1.3)
        self.wait(2)
        self.play(FadeOut(analogy_text))

        # Build 5 components from left (slow) to right (fast)
        # Reversed: HBM -> DMA -> SBUF -> Systolic -> PSUM
        hbm = mem_block("HBM", "16 GB", width=2.0, height=1.0, color=HBM_PURPLE)
        dma = labeled_box("DMA Engine", width=1.8, height=0.9, color=DMA_ORANGE)
        sbuf = mem_block("SBUF", "24 MB", width=2.0, height=1.0, color=SBUF_GREEN)
        systolic = labeled_box("Systolic Array", width=2.0, height=0.9, color=CHIP_BLUE)
        psum = mem_block("PSUM", "2 MB", width=1.6, height=0.9, color=PSUM_TEAL)

        mem_chain = VGroup(hbm, dma, sbuf, systolic, psum).arrange(RIGHT, buff=0.4)
        mem_chain.move_to(DOWN * 0.2)
        if mem_chain.width > SAFE_WIDTH - 0.5:
            mem_chain.scale_to_fit_width(SAFE_WIDTH - 0.5)

        # Analogy labels
        hbm_analogy = safe_text(
            "Warehouse", font_size=16, color=HBM_PURPLE,
        ).next_to(hbm, DOWN, buff=0.25)
        dma_analogy = safe_text(
            "Truck", font_size=16, color=DMA_ORANGE,
        ).next_to(dma, DOWN, buff=0.25)
        sbuf_analogy = safe_text(
            "Countertop", font_size=16, color=SBUF_GREEN,
        ).next_to(sbuf, DOWN, buff=0.25)
        sys_analogy = safe_text(
            "Chef", font_size=16, color=CHIP_BLUE,
        ).next_to(systolic, DOWN, buff=0.25)
        psum_analogy = safe_text(
            "Plate", font_size=16, color=PSUM_TEAL,
        ).next_to(psum, DOWN, buff=0.25)

        analogies = VGroup(
            hbm_analogy, dma_analogy, sbuf_analogy, sys_analogy, psum_analogy,
        )

        # Arrows between components
        arr1 = pipeline_arrow(hbm, dma, color=HBM_PURPLE)
        arr2 = pipeline_arrow(dma, sbuf, color=DMA_ORANGE)
        arr3 = pipeline_arrow(sbuf, systolic, color=SBUF_GREEN)
        arr4 = pipeline_arrow(systolic, psum, color=PSUM_TEAL)
        arrows = VGroup(arr1, arr2, arr3, arr4)

        # Animate each component appearing left to right
        components = [hbm, dma, sbuf, systolic, psum]
        arrow_list = [arr1, arr2, arr3, arr4]
        analogy_list = [hbm_analogy, dma_analogy, sbuf_analogy, sys_analogy, psum_analogy]

        for i, comp in enumerate(components):
            anims = [FadeIn(comp, shift=UP * 0.2), FadeIn(analogy_list[i], shift=UP * 0.15)]
            if i > 0:
                anims.append(Create(arrow_list[i - 1]))
            self.play(*anims, run_time=0.8)

        # Speed labels
        slow_label = safe_text(
            "SLOW", font_size=18, color=DANGER_RED,
        ).next_to(arr1, UP, buff=0.1)
        fast_label = safe_text(
            "FAST", font_size=18, color=SUCCESS_GREEN,
        ).next_to(arr3, UP, buff=0.1)
        instant_label = safe_text(
            "INSTANT", font_size=18, color=SUCCESS_GREEN,
        ).next_to(arr4, UP, buff=0.1)

        self.play(
            FadeIn(slow_label), FadeIn(fast_label), FadeIn(instant_label),
            run_time=0.8,
        )
        self.wait(3)

        # Fade Phase 2
        fade_all(
            self, mem_title, mem_chain, arrows, analogies,
            slow_label, fast_label, instant_label,
        )

        # ===== Phase 3: Complete Data Flow Animation =====
        flow_title = section_title("Matrix Multiply: Full Data Flow")
        self.play(Write(flow_title), run_time=1.2)
        self.wait(2)

        # Simplified pipeline: 5 boxes in a row
        hbm2 = labeled_box("HBM", width=1.6, height=0.8, color=HBM_PURPLE)
        dma2 = labeled_box("DMA", width=1.2, height=0.7, color=DMA_ORANGE)
        sbuf2 = labeled_box("SBUF", width=1.6, height=0.8, color=SBUF_GREEN)
        sys2 = labeled_box("Systolic", width=1.6, height=0.8, color=CHIP_BLUE)
        psum2 = labeled_box("PSUM", width=1.4, height=0.7, color=PSUM_TEAL)

        pipe = VGroup(hbm2, dma2, sbuf2, sys2, psum2).arrange(RIGHT, buff=0.5)
        pipe.move_to(UP * 0.8)
        if pipe.width > SAFE_WIDTH - 0.5:
            pipe.scale_to_fit_width(SAFE_WIDTH - 0.5)

        p_arr1 = pipeline_arrow(hbm2, dma2, color=GRAY_B)
        p_arr2 = pipeline_arrow(dma2, sbuf2, color=GRAY_B)
        p_arr3 = pipeline_arrow(sbuf2, sys2, color=GRAY_B)
        p_arr4 = pipeline_arrow(sys2, psum2, color=GRAY_B)
        p_arrows = VGroup(p_arr1, p_arr2, p_arr3, p_arr4)

        self.play(FadeIn(pipe), Create(p_arrows), run_time=1.2)
        self.wait(2)

        # Step labels shown below the pipeline
        steps = [
            ("Step 1: Weights HBM -> SBUF", DANGER_RED, "slow"),
            ("Step 2: Inputs HBM -> SBUF", DANGER_RED, "slow"),
            ("Step 3: SBUF -> Systolic Array", SUCCESS_GREEN, "fast"),
            ("Step 4: Results accumulate in PSUM", SUCCESS_GREEN, "instant"),
            ("Step 5: PSUM -> SBUF -> HBM", DANGER_RED, "slow"),
        ]

        step_y = DOWN * 0.5
        prev_step_text = None

        for i, (desc, color, speed) in enumerate(steps):
            step_text = safe_text(desc, font_size=BODY_SIZE, color=color)
            step_text.move_to(step_y)

            speed_tag = safe_text(
                speed.upper(), font_size=LABEL_SIZE, color=color,
            ).next_to(step_text, RIGHT, buff=0.3)

            if prev_step_text is not None:
                self.play(FadeOut(prev_step_text), FadeOut(prev_speed))

            # Animate a dot moving through relevant pipeline segment
            dot = Dot(radius=0.12, color=color)
            if i == 0:
                # HBM -> DMA -> SBUF (weights)
                dot.move_to(hbm2.get_right())
                self.play(
                    FadeIn(step_text), FadeIn(speed_tag), FadeIn(dot),
                    run_time=0.6,
                )
                self.play(
                    dot.animate.move_to(sbuf2.get_left()),
                    run_time=1.5,
                    rate_func=linear,
                )
            elif i == 1:
                # HBM -> DMA -> SBUF (inputs)
                dot.move_to(hbm2.get_right())
                self.play(
                    FadeIn(step_text), FadeIn(speed_tag), FadeIn(dot),
                    run_time=0.6,
                )
                self.play(
                    dot.animate.move_to(sbuf2.get_left()),
                    run_time=1.5,
                    rate_func=linear,
                )
            elif i == 2:
                # SBUF -> Systolic (fast)
                dot.move_to(sbuf2.get_right())
                self.play(
                    FadeIn(step_text), FadeIn(speed_tag), FadeIn(dot),
                    run_time=0.6,
                )
                self.play(
                    dot.animate.move_to(sys2.get_left()),
                    run_time=0.6,
                    rate_func=linear,
                )
            elif i == 3:
                # Systolic -> PSUM (instant)
                dot.move_to(sys2.get_right())
                self.play(
                    FadeIn(step_text), FadeIn(speed_tag), FadeIn(dot),
                    run_time=0.6,
                )
                self.play(
                    dot.animate.move_to(psum2.get_left()),
                    run_time=0.3,
                    rate_func=linear,
                )
            else:
                # PSUM -> SBUF -> HBM (slow, reverse)
                dot.move_to(psum2.get_left())
                self.play(
                    FadeIn(step_text), FadeIn(speed_tag), FadeIn(dot),
                    run_time=0.6,
                )
                self.play(
                    dot.animate.move_to(hbm2.get_right()),
                    run_time=1.5,
                    rate_func=linear,
                )

            self.play(FadeOut(dot), run_time=0.3)
            prev_step_text = step_text
            prev_speed = speed_tag
            self.wait(1.5)

        self.play(FadeOut(prev_step_text), FadeOut(prev_speed))

        # Summary
        summary = safe_multiline(
            "Slow parts: steps 1, 2, 5 (trips to HBM)",
            "Fast parts: steps 3, 4 (everything on-chip)",
            font_size=BODY_SIZE, color=WHITE, line_buff=0.35,
        ).move_to(DOWN * 1.0)

        self.play(
            Write(summary[0]), run_time=1.2,
        )
        self.play(
            Write(summary[1]), run_time=1.2,
        )
        self.wait(3)

        # Bottom note
        note = bottom_note(
            "Trainium: systolic array for compute, 3-level memory for data"
        )
        self.play(FadeIn(note, shift=UP * 0.2), run_time=1.2)
        self.wait(3)

        # Cleanup
        fade_all(self, flow_title, pipe, p_arrows, summary, note)
