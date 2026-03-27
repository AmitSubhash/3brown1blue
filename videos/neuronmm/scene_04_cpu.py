"""Scene 04: How a CPU processes data -- sequential, one thing at a time.

Duration: ~90s
Template: FULL_CENTER
Audience: Curious learner (no ML/CS background)
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from utils.style import *


class HowCPUWorksScene(Scene):
    """Teach CPU basics: fetch-decode-execute, memory hierarchy, sequential bottleneck."""

    def construct(self) -> None:
        self.camera.background_color = BLACK

        # -- Title --
        title = safe_text(
            "How Your Computer Processes Data",
            font_size=TITLE_SIZE, color=WHITE,
        ).move_to(UP * TITLE_Y)
        self.play(Write(title), run_time=1.2)
        self.wait(HOLD_MEDIUM)

        # =====================================================
        # Phase 1: The CPU
        # =====================================================
        cpu_box = labeled_box(
            "CPU", width=3.0, height=1.5,
            color=CHIP_BLUE, font_size=HEADING_SIZE,
            fill_opacity=0.2,
        ).move_to(UP * 0.5)

        intro_text = safe_text(
            "Your computer's brain: the CPU",
            font_size=BODY_SIZE, color=WHITE,
        ).move_to(UP * 1.8)

        self.play(Write(intro_text), run_time=1.2)
        self.play(FadeIn(cpu_box, shift=UP * 0.2), run_time=1.0)
        self.wait(HOLD_MEDIUM)

        sequential = safe_text(
            "It follows instructions one at a time, very fast",
            font_size=BODY_SIZE, color=BASELINE_GRAY,
        ).move_to(DOWN * 0.8)
        self.play(Write(sequential), run_time=1.2)
        self.wait(HOLD_LONG)

        self.play(
            FadeOut(cpu_box), FadeOut(intro_text), FadeOut(sequential),
            run_time=0.8,
        )

        # Fetch-Decode-Execute cycle
        cycle_label = safe_text(
            "The CPU repeats 3 steps, billions of times per second:",
            font_size=BODY_SIZE, color=WHITE,
        ).move_to(UP * 1.8)
        self.play(Write(cycle_label), run_time=1.2)
        self.wait(HOLD_SHORT)

        fetch_box = labeled_box(
            "1. Fetch", width=2.2, height=1.0,
            color=CHIP_BLUE, font_size=LABEL_SIZE,
        )
        decode_box = labeled_box(
            "2. Decode", width=2.2, height=1.0,
            color=DMA_ORANGE, font_size=LABEL_SIZE,
        )
        execute_box = labeled_box(
            "3. Execute", width=2.2, height=1.0,
            color=SBUF_GREEN, font_size=LABEL_SIZE,
        )

        cycle_group = VGroup(fetch_box, decode_box, execute_box).arrange(
            RIGHT, buff=1.0,
        ).move_to(UP * 0.2)

        fetch_desc = safe_text(
            "Get instruction", font_size=18, color=BASELINE_GRAY,
        ).next_to(fetch_box, DOWN, buff=0.2)
        decode_desc = safe_text(
            "Understand it", font_size=18, color=BASELINE_GRAY,
        ).next_to(decode_box, DOWN, buff=0.2)
        execute_desc = safe_text(
            "Do the math", font_size=18, color=BASELINE_GRAY,
        ).next_to(execute_box, DOWN, buff=0.2)

        arrow_fd = pipeline_arrow(fetch_box, decode_box, color=WHITE)
        arrow_de = pipeline_arrow(decode_box, execute_box, color=WHITE)

        self.play(
            FadeIn(fetch_box, shift=RIGHT * 0.2),
            FadeIn(fetch_desc),
            run_time=0.8,
        )
        self.play(
            Create(arrow_fd),
            FadeIn(decode_box, shift=RIGHT * 0.2),
            FadeIn(decode_desc),
            run_time=0.8,
        )
        self.play(
            Create(arrow_de),
            FadeIn(execute_box, shift=RIGHT * 0.2),
            FadeIn(execute_desc),
            run_time=0.8,
        )
        self.wait(HOLD_SHORT)

        # Animate highlight cycling through the 3 steps
        highlight = SurroundingRectangle(
            fetch_box, color=SPEEDUP_YELLOW, buff=0.1, stroke_width=3,
        )
        self.play(Create(highlight), run_time=0.5)
        for _ in range(2):
            self.play(
                highlight.animate.move_to(decode_box), run_time=0.4,
            )
            self.play(
                highlight.animate.move_to(execute_box), run_time=0.4,
            )
            self.play(
                highlight.animate.move_to(fetch_box), run_time=0.4,
            )

        repeat_text = safe_text(
            "Over and over, billions of times per second",
            font_size=BODY_SIZE, color=SPEEDUP_YELLOW,
        ).move_to(DOWN * 2.0)
        self.play(Write(repeat_text), run_time=1.2)
        self.wait(HOLD_LONG)

        # Fade Phase 1
        phase1 = VGroup(
            cycle_label, fetch_box, decode_box, execute_box,
            fetch_desc, decode_desc, execute_desc,
            arrow_fd, arrow_de, highlight, repeat_text,
        )
        self.play(FadeOut(phase1), FadeOut(title), run_time=0.8)

        # =====================================================
        # Phase 2: Memory hierarchy
        # =====================================================
        mem_title = safe_text(
            "But there is a problem: getting data to the CPU",
            font_size=TITLE_SIZE, color=WHITE,
        ).move_to(UP * TITLE_Y)
        self.play(Write(mem_title), run_time=1.2)
        self.wait(HOLD_MEDIUM)

        # Build from outside in: RAM -> Cache -> Register -> ALU
        ram_box = labeled_box(
            "RAM", width=5.0, height=1.0,
            color=HBM_PURPLE, font_size=BODY_SIZE,
            fill_opacity=0.15,
        ).move_to(DOWN * 2.0)
        ram_desc = safe_text(
            "Lots of space, but slow", font_size=18, color=HBM_PURPLE,
        ).next_to(ram_box, DOWN, buff=0.15)
        ram_speed = safe_text(
            "~100 ns", font_size=18, color=BASELINE_GRAY,
        ).next_to(ram_box, RIGHT, buff=0.3)

        cache_box = labeled_box(
            "Cache", width=3.5, height=0.9,
            color=SBUF_GREEN, font_size=BODY_SIZE,
            fill_opacity=0.15,
        ).move_to(DOWN * 0.5)
        cache_desc = safe_text(
            "Small, but fast", font_size=18, color=SBUF_GREEN,
        ).next_to(cache_box, RIGHT, buff=0.3)
        cache_speed = safe_text(
            "~10 ns", font_size=18, color=BASELINE_GRAY,
        ).next_to(cache_desc, DOWN, buff=0.05).align_to(cache_desc, LEFT)

        register_box = labeled_box(
            "Register", width=2.2, height=0.8,
            color=PSUM_TEAL, font_size=LABEL_SIZE,
            fill_opacity=0.2,
        ).move_to(UP * 0.8)
        reg_desc = safe_text(
            "Tiny, but instant", font_size=18, color=PSUM_TEAL,
        ).next_to(register_box, RIGHT, buff=0.3)
        reg_speed = safe_text(
            "~1 ns", font_size=18, color=BASELINE_GRAY,
        ).next_to(reg_desc, DOWN, buff=0.05).align_to(reg_desc, LEFT)

        alu_box = labeled_box(
            "ALU (Math)", width=2.0, height=0.7,
            color=CHIP_BLUE, font_size=LABEL_SIZE,
            fill_opacity=0.3,
        ).move_to(UP * 2.0)
        alu_desc = safe_text(
            "Does the actual math", font_size=18, color=CHIP_BLUE,
        ).next_to(alu_box, RIGHT, buff=0.3)

        # Animate building from outside in
        self.play(FadeIn(ram_box), FadeIn(ram_desc), FadeIn(ram_speed), run_time=1.0)
        self.wait(HOLD_SHORT)
        self.play(FadeIn(cache_box), FadeIn(cache_desc), FadeIn(cache_speed), run_time=1.0)
        self.wait(HOLD_SHORT)
        self.play(FadeIn(register_box), FadeIn(reg_desc), FadeIn(reg_speed), run_time=1.0)
        self.wait(HOLD_SHORT)
        self.play(FadeIn(alu_box), FadeIn(alu_desc), run_time=1.0)
        self.wait(HOLD_MEDIUM)

        # Animate a data dot traveling up: RAM -> Cache -> Register -> ALU
        data_dot = Dot(
            point=ram_box.get_top(), radius=0.12,
            color=SPEEDUP_YELLOW, fill_opacity=1.0,
        )
        data_label = safe_text(
            "data", font_size=16, color=SPEEDUP_YELLOW,
        ).next_to(data_dot, LEFT, buff=0.15)
        data_label.add_updater(
            lambda m: m.next_to(data_dot, LEFT, buff=0.15)
        )

        self.play(FadeIn(data_dot), FadeIn(data_label), run_time=0.5)
        self.play(
            data_dot.animate.move_to(cache_box.get_top()),
            run_time=0.8,
        )
        self.play(
            data_dot.animate.move_to(register_box.get_top()),
            run_time=0.6,
        )
        self.play(
            data_dot.animate.move_to(alu_box.get_bottom()),
            run_time=0.4,
        )
        # Flash at ALU
        self.play(
            Flash(alu_box, color=SPEEDUP_YELLOW, line_length=0.3),
            run_time=0.5,
        )
        # Travel back down
        self.play(
            data_dot.animate.move_to(register_box.get_top()),
            run_time=0.4,
        )
        self.play(
            data_dot.animate.move_to(cache_box.get_top()),
            run_time=0.6,
        )
        self.play(
            data_dot.animate.move_to(ram_box.get_top()),
            run_time=0.8,
        )
        data_label.clear_updaters()
        self.wait(HOLD_SHORT)

        travel_note = safe_text(
            "Data must travel up and down this ladder for every calculation",
            font_size=BODY_SIZE, color=DANGER_RED,
        ).move_to(DOWN * 3.0)
        self.play(Write(travel_note), run_time=1.5)
        self.wait(HOLD_LONG)

        # Fade Phase 2
        mem_group = VGroup(
            mem_title, ram_box, ram_desc, ram_speed,
            cache_box, cache_desc, cache_speed,
            register_box, reg_desc, reg_speed,
            alu_box, alu_desc,
            data_dot, data_label, travel_note,
        )
        self.play(FadeOut(mem_group), run_time=0.8)

        # =====================================================
        # Phase 3: Why CPUs are bad at matrix math
        # =====================================================
        bad_title = safe_text(
            "Why CPUs struggle with matrix math",
            font_size=TITLE_SIZE, color=WHITE,
        ).move_to(UP * TITLE_Y)
        self.play(Write(bad_title), run_time=1.2)
        self.wait(HOLD_SHORT)

        # Show a small 3x3 output grid
        grid_bg = Rectangle(
            width=3.0, height=3.0,
            color=BASELINE_GRAY, fill_opacity=0.05, stroke_width=1,
        ).move_to(LEFT * 0.0 + UP * 0.0)

        cell_size = 0.9
        cell_bgs: list[Rectangle] = []
        for r in range(3):
            for c in range(3):
                cell = Rectangle(
                    width=cell_size, height=cell_size,
                    color=BASELINE_GRAY, fill_opacity=0.0,
                    stroke_width=0.5, stroke_opacity=0.4,
                )
                x = (c - 1) * cell_size
                y = (1 - r) * cell_size
                cell.move_to(grid_bg.get_center() + RIGHT * x + UP * y)
                cell_bgs.append(cell)

        cells_group = VGroup(*cell_bgs)
        self.play(
            FadeIn(grid_bg), FadeIn(cells_group),
            run_time=0.8,
        )
        self.wait(HOLD_SHORT)

        # CPU does them one at a time -- animate a dot visiting each cell
        cpu_dot = Dot(
            radius=0.15, color=CHIP_BLUE, fill_opacity=1.0,
        ).move_to(cell_bgs[0].get_center())

        one_label = safe_text(
            "CPU: one cell at a time",
            font_size=BODY_SIZE, color=CHIP_BLUE,
        ).move_to(DOWN * 2.2)

        self.play(FadeIn(cpu_dot), Write(one_label), run_time=0.8)

        for i, cell in enumerate(cell_bgs):
            self.play(
                cpu_dot.animate.move_to(cell.get_center()),
                cell.animate.set_fill(CHIP_BLUE, opacity=0.3),
                run_time=0.3,
            )

        self.wait(HOLD_MEDIUM)

        self.play(FadeOut(cpu_dot), FadeOut(one_label), run_time=0.5)

        # Scale up the pain
        scale_text = safe_multiline(
            "For a 4096 x 4096 matrix:",
            "16 million multiplications...",
            "ONE. AT. A. TIME.",
            font_size=BODY_SIZE, color=WHITE,
        ).move_to(DOWN * 2.0)
        scale_text[2].set_color(DANGER_RED)

        self.play(Write(scale_text[0]), run_time=1.2)
        self.wait(HOLD_SHORT)
        self.play(Write(scale_text[1]), run_time=1.2)
        self.wait(HOLD_SHORT)
        self.play(Write(scale_text[2]), run_time=1.5)
        self.wait(HOLD_LONG)

        # Cliffhanger
        better_way = safe_text(
            "There has to be a better way.",
            font_size=HEADING_SIZE, color=SPEEDUP_YELLOW,
        ).move_to(UP * 0.0)

        self.play(
            FadeOut(grid_bg), FadeOut(cells_group),
            run_time=0.5,
        )
        self.play(Write(better_way), run_time=1.5)
        self.wait(HOLD_LONG)

        # -- Bottom note --
        note = bottom_note(
            "CPUs are powerful but sequential -- bad for massive parallel math"
        )
        self.play(FadeIn(note, shift=UP * 0.2), run_time=0.8)
        self.wait(HOLD_LONG)

        # -- Cleanup --
        fade_all(
            self, bad_title, scale_text, better_way, note,
        )
        self.wait(0.5)
