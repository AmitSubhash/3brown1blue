"""Scene 10: Limitations and Open Questions -- closing scene with citation.

Duration: ~45s
Template: FULL_CENTER
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from utils.style import *


LIMITATIONS: list[tuple[str, str]] = [
    ("MLP layers only (70% of params)", DANGER_RED),
    ("attention compression causes accuracy loss", DANGER_RED),
    ("Single NeuronCore only, multi-chip untested", DMA_ORANGE),
    ("Requires offline SVD + LoRA fine-tuning", DMA_ORANGE),
    ("Trainium-specific optimizations", DMA_ORANGE),
]

OPEN_QUESTIONS: list[str] = [
    "Can attention layers be compressed differently?",
    "Multi-chip NCCL overhead for distributed inference?",
]


class LimitationsScene(Scene):
    """Limitations, open questions, and paper citation."""

    def construct(self) -> None:
        self.camera.background_color = BLACK

        # -- Title --
        title = safe_text(
            "Limitations and Open Questions",
            font_size=TITLE_SIZE, color=CHIP_BLUE,
        ).move_to(UP * TITLE_Y)
        self.play(FadeIn(title, shift=DOWN * 0.3), run_time=1.0)
        self.wait(HOLD_SHORT)

        # ============================================================
        # Phase 1: Limitation bullets (one at a time)
        # ============================================================
        bullet_items = VGroup()
        for text_str, color in LIMITATIONS:
            dot = Dot(radius=0.06, color=color).shift(LEFT * 0.15)
            label = safe_text(
                text_str, font_size=BODY_SIZE, color=color, max_width=9.5,
            )
            row = VGroup(dot, label).arrange(RIGHT, buff=0.25)
            bullet_items.add(row)

        bullet_items.arrange(DOWN, buff=0.35, aligned_edge=LEFT)
        bullet_items.move_to(LEFT * 0.5 + UP * 0.5)

        for item in bullet_items:
            self.play(FadeIn(item, shift=RIGHT * 0.3), run_time=0.7)
            self.wait(0.4)

        self.wait(HOLD_MEDIUM)

        # ============================================================
        # Phase 2: Open Questions
        # ============================================================
        oq_header = safe_text(
            "Open Questions",
            font_size=HEADING_SIZE, color=WHITE,
        ).next_to(bullet_items, DOWN, buff=0.6, aligned_edge=LEFT)

        oq_items = VGroup()
        for q_text in OPEN_QUESTIONS:
            q_dot = Dot(radius=0.05, color=GRAY_B).shift(LEFT * 0.1)
            q_label = safe_text(
                q_text, font_size=LABEL_SIZE, color=GRAY_B, max_width=9.5,
            )
            oq_items.add(VGroup(q_dot, q_label).arrange(RIGHT, buff=0.2))

        oq_items.arrange(DOWN, buff=0.25, aligned_edge=LEFT)
        oq_items.next_to(oq_header, DOWN, buff=0.3, aligned_edge=LEFT)

        self.play(Write(oq_header), run_time=0.6)
        for item in oq_items:
            self.play(FadeIn(item, shift=RIGHT * 0.2), run_time=0.6)
        self.wait(HOLD_MEDIUM)

        # ============================================================
        # Phase 3: Fade limitations, show citation card
        # ============================================================
        self.play(
            FadeOut(bullet_items),
            FadeOut(oq_header),
            FadeOut(oq_items),
            run_time=0.8,
        )

        # Citation card
        cite_box = RoundedRectangle(
            width=8.5, height=3.2, corner_radius=0.2,
            color=CHIP_BLUE, fill_opacity=0.08, stroke_width=2,
        ).move_to(DOWN * 0.1)

        cite_title = safe_text(
            "NeuronMM: Optimizing MatMul on Trainium",
            font_size=BODY_SIZE, color=WHITE, max_width=7.5,
        )
        cite_authors = safe_text(
            "Song, Xu, Yang, Su, Li (2025)",
            font_size=LABEL_SIZE, color=GRAY_B, max_width=7.0,
        )
        cite_arxiv = safe_text(
            "arXiv: 2510.25977",
            font_size=LABEL_SIZE, color=SPEEDUP_YELLOW, max_width=7.0,
        )
        cite_github = safe_text(
            "github.com/dinghongsong/NeuronMM",
            font_size=LABEL_SIZE, color=CHIP_BLUE, max_width=7.0,
        )

        cite_content = VGroup(
            cite_title, cite_authors, cite_arxiv, cite_github,
        ).arrange(DOWN, buff=0.3).move_to(cite_box)

        self.play(
            Create(cite_box),
            FadeIn(cite_content, shift=UP * 0.2),
            run_time=1.5,
        )
        self.wait(HOLD_MEDIUM)

        # -- Bottom note --
        note = bottom_note("Open-sourced for the Trainium ecosystem")
        self.play(FadeIn(note, shift=UP * 0.2), run_time=0.8)
        self.wait(HOLD_LONG)

        # -- Cleanup --
        fade_all(self, title, cite_box, cite_content, note)
        self.wait(0.5)
