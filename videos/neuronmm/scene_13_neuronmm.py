"""Scene 13: NeuronMM's core solution explained via kitchen analogy.

Duration target: ~120s
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from utils.style import *


class NeuronMMSolutionScene(Scene):
    def construct(self) -> None:
        # ---- Title ----
        title = section_title("NeuronMM: The Solution")
        self.play(Write(title), run_time=1.2)
        self.wait(2)

        # ==================================================================
        # Phase 1 -- The problem (kitchen analogy)
        # ==================================================================
        self.play(FadeOut(title))

        # Kitchen elements
        countertop = RoundedRectangle(
            width=4.5, height=1.4, corner_radius=0.15,
            color=SBUF_GREEN, fill_opacity=0.2, stroke_width=2,
        ).shift(UP * 0.8 + LEFT * 1.5)
        ct_label = safe_text("Countertop", font_size=LABEL_SIZE, color=SBUF_GREEN)
        ct_label.next_to(countertop, UP, buff=0.15)
        ct_cap = safe_text("24 MB  (fast, small)", font_size=18, color=GRAY_B)
        ct_cap.next_to(countertop, DOWN, buff=0.1)

        fridge = RoundedRectangle(
            width=3.0, height=2.5, corner_radius=0.15,
            color=HBM_PURPLE, fill_opacity=0.15, stroke_width=2,
        ).shift(DOWN * 1.8 + RIGHT * 3.0)
        fr_label = safe_text("Fridge", font_size=LABEL_SIZE, color=HBM_PURPLE)
        fr_label.next_to(fridge, UP, buff=0.15)
        fr_cap = safe_text("16 GB  (big, slow)", font_size=18, color=GRAY_B)
        fr_cap.next_to(fridge, DOWN, buff=0.1)

        kitchen = VGroup(
            countertop, ct_label, ct_cap,
            fridge, fr_label, fr_cap,
        )
        self.play(FadeIn(kitchen), run_time=1.2)
        self.wait(2)

        # Recall SVD
        recall = safe_text(
            "Remember: SVD splits one big multiply into two steps",
            font_size=BODY_SIZE, color=ACCENT,
        ).to_edge(UP, buff=0.4)
        self.play(Write(recall), run_time=1.3)
        self.wait(2.5)
        self.play(FadeOut(recall))

        # Step 1 -- compute X * U on countertop
        step1_txt = safe_text(
            "Step 1: Compute X times U on the countertop",
            font_size=BODY_SIZE,
        ).to_edge(UP, buff=0.4)
        self.play(Write(step1_txt), run_time=1.3)

        result_block = RoundedRectangle(
            width=1.8, height=0.7, corner_radius=0.1,
            color=MATRIX_Y, fill_opacity=0.5, stroke_width=2,
        ).move_to(countertop.get_center() + RIGHT * 0.8)
        result_label = safe_text("result", font_size=18, color=WHITE)
        result_label.move_to(result_block)
        result_grp = VGroup(result_block, result_label)

        self.play(FadeIn(result_grp, scale=0.6), run_time=1.2)
        self.wait(2)
        self.play(FadeOut(step1_txt))

        # Naive approach: send to fridge
        naive_txt = safe_text(
            "Naive approach: put the result in the fridge",
            font_size=BODY_SIZE, color=DANGER_RED,
        ).to_edge(UP, buff=0.4)
        self.play(Write(naive_txt), run_time=1.3)
        self.wait(2)

        # Slow arrow to fridge
        dma_arrow_down = Arrow(
            countertop.get_right() + RIGHT * 0.2,
            fridge.get_top() + UP * 0.1,
            buff=0.15, color=DMA_ORANGE, stroke_width=4,
        )
        slow1 = safe_text("slow...", font_size=18, color=DMA_ORANGE)
        slow1.next_to(dma_arrow_down, RIGHT, buff=0.1)

        result_copy = result_grp.copy()
        self.play(
            Create(dma_arrow_down),
            FadeIn(slow1),
            result_copy.animate.move_to(fridge.get_center()),
            run_time=1.5,
        )
        self.wait(2)
        self.play(FadeOut(naive_txt))

        # Step 2 -- need result back
        step2_txt = safe_text(
            "Step 2: Need that result again for times V",
            font_size=BODY_SIZE,
        ).to_edge(UP, buff=0.4)
        self.play(Write(step2_txt), run_time=1.3)

        dma_arrow_up = Arrow(
            fridge.get_top() + UP * 0.1,
            countertop.get_right() + RIGHT * 0.2,
            buff=0.15, color=DMA_ORANGE, stroke_width=4,
        )
        slow2 = safe_text("slow...", font_size=18, color=DMA_ORANGE)
        slow2.next_to(dma_arrow_up, LEFT, buff=0.1)
        self.play(Create(dma_arrow_up), FadeIn(slow2), run_time=1.5)
        self.wait(2)
        self.play(FadeOut(step2_txt))

        # Big red verdict
        red_verdict = safe_text(
            "Two extra trips to the fridge!",
            font_size=HEADING_SIZE, color=DANGER_RED,
        ).to_edge(UP, buff=0.4)
        self.play(Write(red_verdict), run_time=1.2)
        self.wait(2)

        stat = safe_text(
            "65% more data movement -- actually SLOWER",
            font_size=BODY_SIZE, color=DANGER_RED,
        ).next_to(red_verdict, DOWN, buff=0.4)
        self.play(FadeIn(stat, shift=UP * 0.2), run_time=1.2)
        self.wait(3)

        # Clean up phase 1
        phase1_all = VGroup(
            kitchen, result_grp, result_copy,
            dma_arrow_down, dma_arrow_up,
            slow1, slow2, red_verdict, stat,
        )
        self.play(FadeOut(phase1_all), run_time=1.2)

        # ==================================================================
        # Phase 2 -- NeuronMM's insight
        # ==================================================================
        insight_title = safe_text(
            "NeuronMM's Insight",
            font_size=TITLE_SIZE, color=ACCENT,
        ).to_edge(UP, buff=0.4)
        self.play(Write(insight_title), run_time=1.2)

        # Rebuild kitchen (cleaner layout)
        ct2 = RoundedRectangle(
            width=5.0, height=1.6, corner_radius=0.15,
            color=SBUF_GREEN, fill_opacity=0.2, stroke_width=2,
        ).shift(UP * 0.3)
        ct2_label = safe_text("Countertop (SBUF)", font_size=LABEL_SIZE, color=SBUF_GREEN)
        ct2_label.next_to(ct2, UP, buff=0.15)

        fr2 = RoundedRectangle(
            width=3.5, height=1.2, corner_radius=0.15,
            color=HBM_PURPLE, fill_opacity=0.15, stroke_width=2,
        ).shift(DOWN * 2.2)
        fr2_label = safe_text("Fridge (HBM)", font_size=LABEL_SIZE, color=HBM_PURPLE)
        fr2_label.next_to(fr2, DOWN, buff=0.1)

        kitchen2 = VGroup(ct2, ct2_label, fr2, fr2_label)
        self.play(FadeIn(kitchen2), run_time=1.2)

        insight_txt = safe_text(
            "KEEP the result on the countertop!",
            font_size=BODY_SIZE, color=SUCCESS_GREEN,
        ).next_to(insight_title, DOWN, buff=0.35)
        self.play(Write(insight_txt), run_time=1.3)
        self.wait(2)

        # Step 1 result stays on countertop
        res2 = RoundedRectangle(
            width=1.8, height=0.7, corner_radius=0.1,
            color=MATRIX_Y, fill_opacity=0.5, stroke_width=2,
        ).move_to(ct2.get_center() + LEFT * 1.0)
        res2_lbl = safe_text("result", font_size=18, color=WHITE)
        res2_lbl.move_to(res2)
        res2_grp = VGroup(res2, res2_lbl)
        self.play(FadeIn(res2_grp, scale=0.6), run_time=1.2)

        stays = safe_text("Stays here!", font_size=LABEL_SIZE, color=SUCCESS_GREEN)
        stays.next_to(res2, DOWN, buff=0.15)
        self.play(FadeIn(stays, shift=UP * 0.2), run_time=1.2)

        # SBUF fill bar
        fill_bar_bg = Rectangle(
            width=3.0, height=0.3,
            color=GRAY_B, fill_opacity=0.1, stroke_width=1,
        ).next_to(ct2, RIGHT, buff=0.4)
        fill_bar = Rectangle(
            width=0.9, height=0.3,
            color=SBUF_GREEN, fill_opacity=0.6, stroke_width=0,
        ).align_to(fill_bar_bg, LEFT).move_to(fill_bar_bg, aligned_edge=LEFT)
        fill_label = safe_text("~30% used", font_size=16, color=SBUF_GREEN)
        fill_label.next_to(fill_bar_bg, UP, buff=0.1)
        fits_txt = safe_text("It fits! No fridge needed!", font_size=18, color=SUCCESS_GREEN)
        fits_txt.next_to(fill_bar_bg, DOWN, buff=0.1)

        self.play(
            FadeIn(fill_bar_bg),
            FadeIn(fill_bar),
            FadeIn(fill_label),
            run_time=1.2,
        )
        self.play(FadeIn(fits_txt, shift=UP * 0.2), run_time=1.2)
        self.wait(3)

        # Clean up phase 2 partial (keep kitchen)
        self.play(
            FadeOut(insight_title), FadeOut(insight_txt),
            FadeOut(stays), FadeOut(fill_bar_bg),
            FadeOut(fill_bar), FadeOut(fill_label), FadeOut(fits_txt),
            run_time=1.0,
        )

        # ==================================================================
        # Phase 3 -- The reuse loop
        # ==================================================================
        reuse_title = safe_text(
            "The Reuse Loop",
            font_size=TITLE_SIZE, color=ACCENT,
        ).to_edge(UP, buff=0.4)
        self.play(Write(reuse_title), run_time=1.2)

        split_txt = safe_text(
            "Split V into small pieces",
            font_size=BODY_SIZE,
        ).next_to(reuse_title, DOWN, buff=0.3)
        self.play(Write(split_txt), run_time=1.2)
        self.wait(2)

        # V blocks on the right
        v_blocks = VGroup()
        v_labels_list = ["V1", "V2", "V3", "V4"]
        for i, name in enumerate(v_labels_list):
            blk = RoundedRectangle(
                width=0.9, height=0.6, corner_radius=0.08,
                color=MATRIX_V, fill_opacity=0.35, stroke_width=2,
            )
            lbl = safe_text(name, font_size=16, color=MATRIX_V)
            lbl.move_to(blk)
            v_blocks.add(VGroup(blk, lbl))
        v_blocks.arrange(RIGHT, buff=0.2).next_to(ct2, DOWN, buff=0.5).shift(RIGHT * 1.5)
        self.play(LaggedStart(*[FadeIn(b, scale=0.7) for b in v_blocks], lag_ratio=0.15), run_time=1.3)
        self.wait(2)

        # Reuse counter
        reuse_counter = safe_text("Reuse 0/4", font_size=LABEL_SIZE, color=SPEEDUP_YELLOW)
        reuse_counter.to_edge(RIGHT, buff=0.8).shift(UP * 2.0)
        self.play(FadeIn(reuse_counter), run_time=0.8)

        # Output area in fridge
        output_slots = VGroup()
        for i in range(4):
            slot = RoundedRectangle(
                width=0.7, height=0.5, corner_radius=0.06,
                color=SPEEDUP_YELLOW, fill_opacity=0.0, stroke_width=1,
            )
            output_slots.add(slot)
        output_slots.arrange(RIGHT, buff=0.15).move_to(fr2.get_center())

        self.play(FadeIn(output_slots), run_time=0.8)

        # Animate reuse loop
        for i in range(4):
            # Green arrow: read from countertop (fast)
            green_arrow = Arrow(
                res2.get_bottom(),
                v_blocks[i].get_top(),
                buff=0.1, color=SUCCESS_GREEN, stroke_width=3,
            )
            fast_lbl = safe_text("fast!", font_size=14, color=SUCCESS_GREEN)
            fast_lbl.next_to(green_arrow, LEFT, buff=0.08)

            self.play(Create(green_arrow), FadeIn(fast_lbl), run_time=0.8)

            # Result goes to fridge (final output only)
            out_arrow = Arrow(
                v_blocks[i].get_bottom(),
                output_slots[i].get_top(),
                buff=0.1, color=SPEEDUP_YELLOW, stroke_width=2,
            )
            filled_slot = output_slots[i].copy().set_fill(
                SPEEDUP_YELLOW, opacity=0.5,
            )
            new_counter = safe_text(
                f"Reuse {i + 1}/4",
                font_size=LABEL_SIZE, color=SPEEDUP_YELLOW,
            ).move_to(reuse_counter)

            self.play(
                Create(out_arrow),
                FadeIn(filled_slot),
                Transform(reuse_counter, new_counter),
                run_time=0.8,
            )
            self.play(
                FadeOut(green_arrow), FadeOut(fast_lbl), FadeOut(out_arrow),
                run_time=0.5,
            )

        self.wait(2)

        reuse_summary = safe_text(
            "Intermediate result reused 4 times from fast memory!",
            font_size=BODY_SIZE, color=SUCCESS_GREEN,
        ).to_edge(UP, buff=0.4)
        self.play(
            FadeOut(reuse_title), FadeOut(split_txt),
            Write(reuse_summary),
            run_time=1.3,
        )
        self.wait(2)

        zero_trips = safe_text(
            "Zero extra trips to the fridge",
            font_size=BODY_SIZE, color=SPEEDUP_YELLOW,
        ).next_to(reuse_summary, DOWN, buff=0.35)
        self.play(FadeIn(zero_trips, shift=UP * 0.2), run_time=1.2)
        self.wait(3)

        # Clean up phase 3
        phase3_all = VGroup(
            kitchen2, res2_grp, v_blocks, reuse_counter,
            output_slots, filled_slot,
            reuse_summary, zero_trips,
        )
        self.play(FadeOut(phase3_all), run_time=1.2)

        # ==================================================================
        # Phase 4 -- Technical name
        # ==================================================================
        tech_title = safe_text(
            "The Technical Name",
            font_size=TITLE_SIZE, color=ACCENT,
        ).to_edge(UP, buff=0.5)
        self.play(Write(tech_title), run_time=1.2)

        line1 = safe_text(
            "This is called kernel fusion with SBUF caching",
            font_size=BODY_SIZE, color=WHITE,
        )
        line2 = safe_text(
            "Kernel fusion = combining two operations into one",
            font_size=BODY_SIZE, color=CHIP_BLUE,
        )
        line3 = safe_text(
            "SBUF caching = keeping intermediate data in fast memory",
            font_size=BODY_SIZE, color=SBUF_GREEN,
        )
        tech_lines = VGroup(line1, line2, line3).arrange(DOWN, buff=0.5).next_to(tech_title, DOWN, buff=0.6)

        for line in [line1, line2, line3]:
            self.play(Write(line), run_time=1.3)
            self.wait(2)

        note = bottom_note(
            "NeuronMM: fuse the two matmuls, cache intermediate in fast on-chip memory"
        )
        self.play(FadeIn(note, shift=UP * 0.2), run_time=1.2)
        self.wait(3)

        fade_all(self, tech_title, line1, line2, line3, note)
        self.wait(0.5)
