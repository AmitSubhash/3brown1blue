"""Scene 06: Trainium Fusion -- SBUF Caching Strategy.

Shows how NeuronMM caches the XU intermediate in SBUF to avoid HBM
round-trips, then reuses it for each column block of V.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from utils.style import *


class TrainiumFusionScene(Scene):
    """Animate the SBUF caching fusion strategy on Trainium."""

    def construct(self) -> None:
        # ── Title ──
        title = safe_text(
            "Fused Kernel: SBUF Caching", font_size=TITLE_SIZE, color=WHITE,
        ).move_to(UP * TITLE_Y)
        self.play(Write(title))
        self.wait(HOLD_SHORT)

        # ── TOP: Small pipeline overview (y=[2.0, 3.2], scaled 0.5x) ──
        pipe_x = labeled_box("X", width=0.8, height=0.5, color=MATRIX_X, font_size=14)
        pipe_xu = labeled_box("X*U", width=1.0, height=0.5, color=MATRIX_U, font_size=14)
        pipe_cache = labeled_box("SBUF", width=1.0, height=0.5, color=SBUF_GREEN, font_size=14)
        pipe_cv = labeled_box("cache*V", width=1.2, height=0.5, color=MATRIX_V, font_size=14)
        pipe_o = labeled_box("O", width=0.8, height=0.5, color=SPEEDUP_YELLOW, font_size=14)

        pipeline = VGroup(pipe_x, pipe_xu, pipe_cache, pipe_cv, pipe_o).arrange(
            RIGHT, buff=0.6,
        )
        pipeline.scale(0.5)
        pipeline.move_to(UP * 2.5)

        # Arrows between pipeline stages
        pipe_arrows = VGroup()
        pipe_nodes = [pipe_x, pipe_xu, pipe_cache, pipe_cv, pipe_o]
        for i in range(len(pipe_nodes) - 1):
            arr = Arrow(
                pipe_nodes[i].get_right(), pipe_nodes[i + 1].get_left(),
                buff=0.06, color=WHITE, stroke_width=1.5,
                max_tip_length_to_length_ratio=0.2,
            )
            pipe_arrows.add(arr)

        top_group = VGroup(pipeline, pipe_arrows)

        self.play(FadeIn(top_group, shift=DOWN * 0.2))
        self.wait(HOLD_SHORT)

        # ── FadeOut title to make room for bottom content ──
        self.play(FadeOut(title))

        # ── BOTTOM CONTENT: Detailed SBUF caching animation ──
        # Region: y in [-2.5, 1.5]

        # Step 1: Draw SBUF as a large green container
        sbuf_width = 5.0
        sbuf_height = 1.8
        sbuf_outline = RoundedRectangle(
            width=sbuf_width, height=sbuf_height, corner_radius=0.12,
            color=SBUF_GREEN, fill_opacity=0.0, stroke_width=2.5,
        ).move_to(LEFT * 0.5 + DOWN * 0.2)

        sbuf_label = safe_text(
            "SBUF (24MB on-chip)", font_size=LABEL_SIZE, color=SBUF_GREEN,
        )
        sbuf_label.next_to(sbuf_outline, UP, buff=0.15)

        # Fill-level indicator (starts empty, green bar that grows)
        fill_bar_bg = Rectangle(
            width=sbuf_width - 0.4, height=0.3,
            color=GRAY_E, fill_opacity=0.3, stroke_width=1,
        )
        fill_bar_bg.move_to(sbuf_outline.get_bottom() + UP * 0.4)

        self.play(
            Create(sbuf_outline),
            Write(sbuf_label),
            FadeIn(fill_bar_bg),
        )
        self.wait(HOLD_SHORT)

        # Step 2: Show computation X * U producing a row strip
        comp_label = safe_text(
            "Compute X * U:", font_size=LABEL_SIZE, color=WHITE,
        ).move_to(LEFT * 4.0 + UP * 1.3)

        strip = Rectangle(
            width=2.5, height=0.5,
            color=MATRIX_U, fill_opacity=0.4, stroke_width=2,
        )
        strip_label = safe_text("[BM x r]", font_size=16, color=MATRIX_U)
        strip_label.move_to(strip)
        strip_group = VGroup(strip, strip_label)
        strip_group.move_to(LEFT * 3.0 + UP * 0.7)

        self.play(
            Write(comp_label),
            FadeIn(strip_group, shift=RIGHT * 0.3),
        )
        self.wait(HOLD_SHORT)

        # Step 3: Animate strip writing into SBUF
        strip_target = strip.copy().set_color(SBUF_GREEN)
        strip_target.move_to(sbuf_outline.get_center() + UP * 0.25)

        # Green fill bar rises to show capacity used
        fill_bar = Rectangle(
            width=(sbuf_width - 0.4) * 0.3,  # ~30% capacity used
            height=0.3,
            color=SBUF_GREEN, fill_opacity=0.5, stroke_width=0,
        )
        fill_bar.align_to(fill_bar_bg, LEFT)
        fill_bar.move_to(fill_bar_bg, aligned_edge=LEFT)

        cached_label = safe_text(
            "Cached!", font_size=LABEL_SIZE, color=SBUF_GREEN,
        )
        cached_label.next_to(sbuf_outline, RIGHT, buff=0.3)

        write_arrow = Arrow(
            strip_group.get_bottom(),
            sbuf_outline.get_top() + LEFT * 1.5,
            buff=0.1, color=SBUF_GREEN, stroke_width=2.5,
            max_tip_length_to_length_ratio=0.15,
        )

        self.play(
            Create(write_arrow),
            strip_group.animate.move_to(sbuf_outline.get_center() + UP * 0.25),
            FadeIn(fill_bar),
            run_time=1.5,
        )
        self.play(FadeIn(cached_label, shift=LEFT * 0.2))
        self.play(FadeOut(write_arrow), FadeOut(comp_label))
        self.wait(HOLD_SHORT)

        # Step 4: Show V split into column blocks
        n_blocks = 4
        v_blocks = VGroup()
        v_labels_group = VGroup()
        block_width = 0.7
        block_height = 1.2

        for i in range(n_blocks):
            blk = Rectangle(
                width=block_width, height=block_height,
                color=MATRIX_V, fill_opacity=0.25, stroke_width=1.5,
            )
            lbl = safe_text(f"V{i+1}", font_size=14, color=MATRIX_V)
            lbl.move_to(blk)
            v_blocks.add(blk)
            v_labels_group.add(lbl)

        v_all = VGroup()
        for blk, lbl in zip(v_blocks, v_labels_group):
            v_all.add(VGroup(blk, lbl))
        v_all.arrange(RIGHT, buff=0.12)
        v_all.move_to(RIGHT * 3.5 + DOWN * 0.2)

        v_title = safe_text(
            "V columns:", font_size=LABEL_SIZE, color=MATRIX_V,
        )
        v_title.next_to(v_all, UP, buff=0.15)

        self.play(
            FadeIn(v_all, shift=LEFT * 0.3),
            Write(v_title),
        )
        self.wait(HOLD_SHORT)

        # Step 5: PSUM accumulator
        psum_box = labeled_box(
            "PSUM", width=1.5, height=0.6, color=PSUM_TEAL, font_size=16,
        )
        psum_box.move_to(RIGHT * 3.5 + DOWN * 1.8)
        self.play(FadeIn(psum_box, shift=UP * 0.2))

        # Step 6: Reuse loop -- for each V block, read from SBUF, multiply, write to PSUM
        reuse_counter = safe_text(
            "Reuse: 0/4", font_size=LABEL_SIZE, color=ACCENT,
        )
        reuse_counter.move_to(LEFT * 4.0 + DOWN * 1.8)
        self.play(FadeIn(reuse_counter))

        no_hbm_label = safe_text(
            "No HBM!", font_size=16, color=SUCCESS_GREEN,
        )
        no_hbm_label.next_to(sbuf_outline, LEFT, buff=0.3)

        for i in range(n_blocks):
            # Highlight current V block
            current_v = v_all[i]
            highlight_rect = SurroundingRectangle(
                current_v, color=HIGHLIGHT, buff=0.06, stroke_width=2,
            )

            # Arrow from SBUF to current V block area (representing read)
            read_arrow = Arrow(
                sbuf_outline.get_right(),
                current_v.get_left(),
                buff=0.1, color=SBUF_GREEN, stroke_width=2,
                max_tip_length_to_length_ratio=0.15,
            )

            # Arrow from V block to PSUM
            psum_arrow = Arrow(
                current_v.get_bottom(),
                psum_box.get_top(),
                buff=0.1, color=PSUM_TEAL, stroke_width=2,
                max_tip_length_to_length_ratio=0.15,
            )

            new_counter = safe_text(
                f"Reuse: {i+1}/{n_blocks}", font_size=LABEL_SIZE, color=ACCENT,
            )
            new_counter.move_to(reuse_counter.get_center())

            anims = [
                Create(highlight_rect),
                Create(read_arrow),
            ]
            if i == 0:
                anims.append(FadeIn(no_hbm_label, shift=RIGHT * 0.1))

            self.play(*anims, run_time=0.6)
            self.play(
                Create(psum_arrow),
                Transform(reuse_counter, new_counter),
                run_time=0.5,
            )
            self.play(
                FadeOut(highlight_rect),
                FadeOut(read_arrow),
                FadeOut(psum_arrow),
                run_time=0.4,
            )

        self.wait(HOLD_SHORT)

        # ── Emphasize: fill never exceeds capacity ──
        capacity_note = safe_text(
            "SBUF fill never exceeds 24MB -- data stays on-chip",
            font_size=LABEL_SIZE, color=SBUF_GREEN,
        )
        capacity_note.move_to(DOWN * 2.6)
        self.play(FadeIn(capacity_note, shift=UP * 0.2))
        self.wait(HOLD_MEDIUM)

        # ── Bottom note ──
        note = bottom_note(
            "Entire intermediate cached in 24MB SBUF -- no HBM round-trip"
        )
        self.play(
            FadeOut(capacity_note),
            FadeIn(note, shift=UP * 0.2),
        )
        self.wait(HOLD_LONG)

        # ── Cleanup ──
        all_objs = [
            top_group, sbuf_outline, sbuf_label, fill_bar_bg, fill_bar,
            strip_group, cached_label,
            v_all, v_title, psum_box, reuse_counter, no_hbm_label, note,
        ]
        self.play(*[FadeOut(m) for m in all_objs])
        self.wait(0.3)
