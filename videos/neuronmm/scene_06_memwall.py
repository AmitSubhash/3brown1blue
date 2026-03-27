"""Scene 06: The Memory Hierarchy.

Teaches the universal speed-vs-size tradeoff using a kitchen analogy,
then maps it to real hardware numbers, and explains why it matters for AI.
Duration target: ~120 seconds.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from utils.style import *


class MemoryHierarchyScene(Scene):
    """Memory hierarchy: kitchen analogy, real numbers, memory wall."""

    def construct(self) -> None:
        self.phase_1_kitchen_analogy()
        self.phase_2_real_numbers()
        self.phase_3_why_it_matters()

    # -- Phase 1: The Kitchen Analogy ------------------------------------------

    def phase_1_kitchen_analogy(self) -> None:
        title: Text = section_title("The Memory Hierarchy")
        self.play(Write(title), run_time=1.2)
        self.wait(2)

        # Build kitchen scene left to right
        hands: VGroup = VGroup(
            Circle(radius=0.3, color=PSUM_TEAL, fill_opacity=0.3, stroke_width=2),
            safe_text("Hands", font_size=18, color=PSUM_TEAL),
        )
        hands[1].next_to(hands[0], DOWN, buff=0.15)
        hands_desc: Text = safe_text("Instant, tiny", font_size=14, color=GRAY_B)
        hands_desc.next_to(hands[1], DOWN, buff=0.1)
        hands_group: VGroup = VGroup(hands, hands_desc).move_to(LEFT * 4.0 + DOWN * 0.2)

        counter: VGroup = VGroup(
            RoundedRectangle(
                width=1.4, height=0.8, corner_radius=0.1,
                color=SBUF_GREEN, fill_opacity=0.25, stroke_width=2,
            ),
            safe_text("Counter", font_size=18, color=SBUF_GREEN),
        )
        counter[1].next_to(counter[0], DOWN, buff=0.15)
        counter_desc: Text = safe_text("Arm's reach", font_size=14, color=GRAY_B)
        counter_desc.next_to(counter[1], DOWN, buff=0.1)
        counter_group: VGroup = VGroup(counter, counter_desc).move_to(LEFT * 1.3 + DOWN * 0.2)

        fridge: VGroup = VGroup(
            RoundedRectangle(
                width=1.8, height=1.2, corner_radius=0.1,
                color=CHIP_BLUE, fill_opacity=0.2, stroke_width=2,
            ),
            safe_text("Fridge", font_size=18, color=CHIP_BLUE),
        )
        fridge[1].next_to(fridge[0], DOWN, buff=0.15)
        fridge_desc: Text = safe_text("Walk over", font_size=14, color=GRAY_B)
        fridge_desc.next_to(fridge[1], DOWN, buff=0.1)
        fridge_group: VGroup = VGroup(fridge, fridge_desc).move_to(RIGHT * 1.5 + DOWN * 0.2)

        warehouse: VGroup = VGroup(
            RoundedRectangle(
                width=2.4, height=1.6, corner_radius=0.1,
                color=HBM_PURPLE, fill_opacity=0.15, stroke_width=2,
            ),
            safe_text("Warehouse", font_size=18, color=HBM_PURPLE),
        )
        warehouse[1].next_to(warehouse[0], DOWN, buff=0.15)
        warehouse_desc: Text = safe_text("Drive there", font_size=14, color=GRAY_B)
        warehouse_desc.next_to(warehouse[1], DOWN, buff=0.1)
        warehouse_group: VGroup = VGroup(warehouse, warehouse_desc).move_to(RIGHT * 4.2 + DOWN * 0.2)

        kitchen_items: list = [hands_group, counter_group, fridge_group, warehouse_group]
        for item in kitchen_items:
            self.play(FadeIn(item, shift=UP * 0.3), run_time=1.0)
            self.wait(1)

        # Chef dot moves to each
        chef: Dot = Dot(color=SPEEDUP_YELLOW, radius=0.15)
        chef.move_to(hands_group[0][0].get_center())
        self.play(FadeIn(chef, scale=0.5), run_time=0.5)

        # Hands: instant flash
        self.play(
            hands[0].animate.set_fill(PSUM_TEAL, opacity=0.6),
            Flash(chef, color=PSUM_TEAL, line_length=0.2, num_lines=6),
            run_time=0.5,
        )
        self.play(hands[0].animate.set_fill(PSUM_TEAL, opacity=0.3), run_time=0.3)

        # Counter: quick move
        self.play(chef.animate.move_to(counter[0].get_center()), run_time=0.6)
        self.play(
            counter[0].animate.set_fill(SBUF_GREEN, opacity=0.5),
            run_time=0.4,
        )
        self.play(counter[0].animate.set_fill(SBUF_GREEN, opacity=0.25), run_time=0.3)

        # Fridge: walk
        self.play(chef.animate.move_to(fridge[0].get_center()), run_time=1.0)
        self.play(
            fridge[0].animate.set_fill(CHIP_BLUE, opacity=0.4),
            run_time=0.4,
        )
        self.play(fridge[0].animate.set_fill(CHIP_BLUE, opacity=0.2), run_time=0.3)

        # Warehouse: long trip
        self.play(chef.animate.move_to(warehouse[0].get_center()), run_time=1.5)
        self.play(
            warehouse[0].animate.set_fill(HBM_PURPLE, opacity=0.4),
            run_time=0.4,
        )
        self.play(warehouse[0].animate.set_fill(HBM_PURPLE, opacity=0.15), run_time=0.3)
        self.wait(1)

        tradeoff: Text = safe_text(
            "Faster memory is ALWAYS smaller. Bigger memory is ALWAYS slower.",
            font_size=BODY_SIZE, color=ACCENT,
        )
        tradeoff.move_to(DOWN * 3.0)
        self.play(FadeIn(tradeoff, shift=UP * 0.2), run_time=1.2)
        self.wait(3)

        fundamental: Text = safe_text(
            "This is the fundamental tradeoff in ALL computers.",
            font_size=BODY_SIZE, color=WHITE,
        )
        fundamental.move_to(DOWN * 3.0)
        self.play(ReplacementTransform(tradeoff, fundamental), run_time=1.0)
        self.wait(2.5)

        fade_all(
            self, title, *kitchen_items, chef, fundamental,
        )
        self.wait(0.5)

    # -- Phase 2: Real Numbers -------------------------------------------------

    def phase_2_real_numbers(self) -> None:
        title: Text = section_title("Real Hardware Numbers")
        self.play(Write(title), run_time=1.2)
        self.wait(1.5)

        # Vertical stack: fastest at top
        levels: list[tuple[str, str, str, str]] = [
            ("Registers",    "1 ns",       "1 KB",    PSUM_TEAL),
            ("L1 Cache",     "4 ns",       "64 KB",   SBUF_GREEN),
            ("L2 Cache",     "10 ns",      "1 MB",    "#27AE60"),
            ("Main Memory",  "100 ns",     "16 GB",   HBM_PURPLE),
            ("SSD / Disk",   "100,000 ns", "1 TB",    BASELINE_GRAY),
        ]

        rows: VGroup = VGroup()
        for i, (name, speed, size, color) in enumerate(levels):
            # Width proportional to capacity (visual metaphor)
            bar_width: float = 1.5 + i * 1.8
            bar: RoundedRectangle = RoundedRectangle(
                width=bar_width, height=0.55, corner_radius=0.08,
                color=color, fill_opacity=0.25, stroke_width=2,
            )

            name_text: Text = safe_text(name, font_size=LABEL_SIZE, color=color)
            speed_text: Text = safe_text(speed, font_size=18, color=WHITE)
            size_text: Text = safe_text(size, font_size=18, color=GRAY_B)

            name_text.move_to(bar.get_left() + RIGHT * 0.1).shift(RIGHT * name_text.width / 2)
            speed_text.next_to(bar, RIGHT, buff=0.3)
            size_text.next_to(speed_text, RIGHT, buff=0.4)

            row: VGroup = VGroup(bar, name_text, speed_text, size_text)
            rows.add(row)

        rows.arrange(DOWN, buff=0.2, center=True)
        rows.move_to(DOWN * 0.3)

        # Left-align bars
        for row in rows:
            row[0].align_to(rows[0][0], LEFT)
            row[1].move_to(row[0].get_left() + RIGHT * 0.1).shift(RIGHT * row[1].width / 2)

        for row in rows:
            self.play(
                Create(row[0]), Write(row[1]),
                FadeIn(row[2]), FadeIn(row[3]),
                run_time=0.9,
            )
            self.wait(0.5)

        self.wait(1.5)

        # Speedup callout
        speedup: Text = safe_text(
            "Registers are 100,000x faster than disk!",
            font_size=BODY_SIZE, color=SPEEDUP_YELLOW,
        )
        speedup.move_to(DOWN * 3.0)
        self.play(FadeIn(speedup, shift=UP * 0.2), run_time=1.2)
        self.wait(3)

        fade_all(self, title, rows, speedup)
        self.wait(0.5)

    # -- Phase 3: Why This Matters for AI --------------------------------------

    def phase_3_why_it_matters(self) -> None:
        title: Text = section_title("Why This Matters for AI")
        self.play(Write(title), run_time=1.2)
        self.wait(1.5)

        # Explanation lines
        line1: Text = safe_text(
            "Matrix multiplication needs LOTS of data",
            font_size=BODY_SIZE,
        )
        line1.move_to(UP * 1.5)
        self.play(Write(line1), run_time=1.2)
        self.wait(2)

        line2: Text = safe_text(
            "The data lives in slow memory (RAM / HBM)",
            font_size=BODY_SIZE, color=HBM_PURPLE,
        )
        line2.next_to(line1, DOWN, buff=0.5)
        self.play(Write(line2), run_time=1.2)
        self.wait(2)

        line3: Text = safe_text(
            "The processor computes fast, but WAITING for data is the bottleneck",
            font_size=BODY_SIZE, color=DANGER_RED,
        )
        line3.next_to(line2, DOWN, buff=0.5)
        self.play(Write(line3), run_time=1.5)
        self.wait(2)

        # Visual: processor spinning, slow data trickle
        self.play(FadeOut(line1), FadeOut(line2), FadeOut(line3), run_time=0.8)

        processor: VGroup = labeled_box(
            "Processor", width=2.0, height=1.2,
            color=CHIP_BLUE, fill_opacity=0.3,
        )
        processor.move_to(RIGHT * 2.0)

        hbm_box: VGroup = labeled_box(
            "HBM", width=2.0, height=1.2,
            color=HBM_PURPLE, fill_opacity=0.2,
        )
        hbm_box.move_to(LEFT * 2.5)

        self.play(FadeIn(processor), FadeIn(hbm_box), run_time=1.0)

        # Spinning indicator on processor
        spinner: Dot = Dot(color=SPEEDUP_YELLOW, radius=0.08)
        spinner.move_to(processor.get_center() + UP * 0.3)

        # Data dots trickling slowly from HBM to processor
        data_dots: VGroup = VGroup()
        for i in range(5):
            dd: Dot = Dot(color=HBM_PURPLE, radius=0.06)
            dd.move_to(hbm_box.get_right() + RIGHT * 0.3 + RIGHT * i * 0.5)
            data_dots.add(dd)

        self.play(FadeIn(spinner), run_time=0.3)
        self.play(
            Rotate(spinner, angle=TAU * 3, about_point=processor.get_center(), rate_func=linear),
            LaggedStart(
                *[dd.animate.move_to(processor.get_left() + LEFT * 0.1) for dd in data_dots],
                lag_ratio=0.4,
            ),
            run_time=3.0,
        )
        self.wait(1)

        # "Idle" label
        idle_label: Text = safe_text("Waiting...", font_size=LABEL_SIZE, color=DANGER_RED)
        idle_label.next_to(processor, UP, buff=0.3)
        self.play(FadeIn(idle_label, shift=DOWN * 0.1), run_time=0.8)
        self.wait(1.5)

        wall_text: Text = safe_text(
            "This is called the MEMORY WALL",
            font_size=HEADING_SIZE, color=DANGER_RED,
        )
        wall_text.move_to(DOWN * 2.0)
        self.play(FadeIn(wall_text, shift=UP * 0.3), run_time=1.2)
        self.wait(2.5)

        note: Text = bottom_note(
            "The memory wall: processors are fast, but feeding them data is slow"
        )
        self.play(
            FadeOut(wall_text),
            FadeIn(note, shift=UP * 0.2),
            run_time=1.0,
        )
        self.wait(3)

        fade_all(
            self, title, processor, hbm_box, spinner,
            data_dots, idle_label, note,
        )
        self.wait(0.5)
