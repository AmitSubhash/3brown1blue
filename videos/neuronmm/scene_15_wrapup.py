"""Scene 15: Wrap-up -- recap the journey, open questions, citation.

Duration target: ~45s
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from utils.style import *


class WrapUpScene(Scene):
    def construct(self) -> None:
        # ---- Title ----
        title = section_title("What We Learned")
        self.play(Write(title), run_time=1.2)
        self.wait(2)
        self.play(FadeOut(title))

        # ==================================================================
        # Phase 1 -- Full stack recap (vertical pipeline)
        # ==================================================================
        steps = [
            ("AI Chatbot", WHITE),
            ("Matrix Multiplication", MATRIX_W),
            ("GPU / Trainium", CHIP_BLUE),
            ("Memory Hierarchy", HBM_PURPLE),
            ("SVD Splitting", MATRIX_U),
            ("NeuronMM Caching", SBUF_GREEN),
            ("2.49x Faster!", SPEEDUP_YELLOW),
        ]

        boxes = VGroup()
        for label, color in steps:
            box = labeled_box(
                label, width=3.8, height=0.55, color=color,
                font_size=LABEL_SIZE, fill_opacity=0.2,
            )
            boxes.add(box)

        boxes.arrange(DOWN, buff=0.25).move_to(ORIGIN + LEFT * 1.5)

        # Ensure it fits vertically
        if boxes.height > SAFE_HEIGHT - 0.6:
            boxes.scale_to_fit_height(SAFE_HEIGHT - 0.6)

        # Highlight the last box
        highlight_rect = SurroundingRectangle(
            boxes[-1], color=SPEEDUP_YELLOW, buff=0.08, stroke_width=3,
        )

        # Build arrows between consecutive boxes
        arrows = VGroup()
        for i in range(len(boxes) - 1):
            arr = Arrow(
                boxes[i].get_bottom(),
                boxes[i + 1].get_top(),
                buff=0.08, color=GRAY_B, stroke_width=2,
                max_tip_length_to_length_ratio=0.25,
            )
            arrows.add(arr)

        # Animate one at a time
        for i, box in enumerate(boxes):
            anims = [FadeIn(box, shift=DOWN * 0.2)]
            if i > 0:
                anims.append(Create(arrows[i - 1]))
            self.play(*anims, run_time=0.8)

        self.play(Create(highlight_rect), run_time=0.8)

        journey_txt = safe_text(
            "We traced the path from chatbot to chip and back",
            font_size=BODY_SIZE, color=ACCENT,
        ).to_edge(RIGHT, buff=0.5).shift(UP * 0.5)
        if journey_txt.width > 5.0:
            journey_txt.scale_to_fit_width(5.0)
        self.play(Write(journey_txt), run_time=1.3)
        self.wait(3)

        # Clean up phase 1
        phase1 = VGroup(boxes, arrows, highlight_rect, journey_txt)
        self.play(FadeOut(phase1), run_time=1.2)

        # ==================================================================
        # Phase 2 -- What's still open
        # ==================================================================
        open_title = safe_text(
            "Still being explored:",
            font_size=HEADING_SIZE, color=ACCENT,
        ).to_edge(UP, buff=0.6)
        self.play(Write(open_title), run_time=1.2)

        bullets_text = [
            "Speed up attention layers too (currently only 70% of the model)",
            "Connect multiple Trainium chips together",
            "Apply these ideas to other custom chips",
        ]
        bullets = VGroup()
        for txt in bullets_text:
            bullet = safe_text(txt, font_size=BODY_SIZE, color=GRAY_B, max_width=10.5)
            bullets.add(bullet)
        bullets.arrange(DOWN, buff=0.5, center=True).next_to(open_title, DOWN, buff=0.7)

        for b in bullets:
            self.play(FadeIn(b, shift=UP * 0.2), run_time=1.2)
            self.wait(2)

        self.wait(2)

        phase2 = VGroup(open_title, bullets)
        self.play(FadeOut(phase2), run_time=1.2)

        # ==================================================================
        # Phase 3 -- Citation card
        # ==================================================================
        card_bg = RoundedRectangle(
            width=8.0, height=4.5, corner_radius=0.3,
            color=CHIP_BLUE, fill_opacity=0.08, stroke_width=2,
        ).move_to(ORIGIN)

        paper_title = safe_text(
            "NeuronMM", font_size=TITLE_SIZE, color=CHIP_BLUE,
        )
        authors = safe_text(
            "Song, Xu, Yang, Su, Li (2025)",
            font_size=BODY_SIZE, color=GRAY_B,
        )
        arxiv = safe_text(
            "arXiv: 2510.25977",
            font_size=BODY_SIZE, color=SPEEDUP_YELLOW,
        )
        github = safe_text(
            "github.com/dinghongsong/NeuronMM",
            font_size=LABEL_SIZE, color=CHIP_BLUE,
        )

        card_content = VGroup(paper_title, authors, arxiv, github)
        card_content.arrange(DOWN, buff=0.4).move_to(card_bg)

        card = VGroup(card_bg, card_content)
        self.play(FadeIn(card, scale=0.9), run_time=1.5)
        self.wait(3)

        note = bottom_note("Making AI faster, cheaper, and more accessible")
        self.play(FadeIn(note, shift=UP * 0.2), run_time=1.2)
        self.wait(3)

        fade_all(self, card, note)
        self.wait(0.5)
