<p align="center">
  <img src="assets/header.png" width="100%" alt="Claude Code Manim Skill">
</p>

<h2 align="center"><b>Describe It. Claude Animates It. 3Blue1Brown Quality.</b></h2>

<p align="center">
  <b><i>A Claude Code skill that turns natural language into production Manim videos.</i></b>
</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="MIT License"></a>
  <a href="https://docs.manim.community"><img src="https://img.shields.io/badge/Manim_CE-v0.20%2B-6B8FD6?logo=python&logoColor=white" alt="Manim v0.20+"></a>
  <a href="https://python.org"><img src="https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white" alt="Python 3.10+"></a>
  <a href="https://github.com/anthropics/claude-code"><img src="https://img.shields.io/badge/Claude_Code-Skill-cc785c?logo=anthropic&logoColor=white" alt="Claude Code Skill"></a>
  <img src="https://img.shields.io/badge/Tested-32_Scenes-brightgreen?logo=checkmarx&logoColor=white" alt="32 Scenes Tested">
  <img src="https://img.shields.io/badge/Rule_Files-21-blue" alt="21 Rule Files">
  <img src="https://img.shields.io/badge/Gotchas_Caught-12-orange" alt="12 Gotchas">
  <img src="https://img.shields.io/badge/3b1b_Patterns-22-purple" alt="22 Patterns">
</p>

---

## One Command. One Video.

```
> Animate the derivation of the Euler identity in 3Blue1Brown style
```

Claude reads the rules, writes safe Manim code, renders, and returns a video. No Manim experience required.

---

## What Is This?

**You describe it. Claude animates it.**

Drop this skill into `~/.claude/skills/` and Claude becomes a production-capable Manim developer. It writes correct Manim code on the first try because it has 21 rule files encoding the full API surface, 12 crash-prevention patterns, and 22 visual design recipes extracted from 422 analyzed 3Blue1Brown frames.

<table>
<tr><td><b>Input</b></td><td><code>"Explain attention mechanisms visually"</code></td><td>Natural language prompt to Claude Code</td></tr>
<tr><td><b>Output</b></td><td><code>scene.py</code> + <code>MyScene.mp4</code></td><td>Correct Manim code + rendered 1080p video</td></tr>
<tr><td><b>Safety Net</b></td><td><code>safe_manim.py</code></td><td>Drop-in wrappers that prevent 6 known Manim crashes</td></tr>
<tr><td><b>Templates</b></td><td><code>style.py</code>, <code>equation_explainer.py</code>, <code>paper_explainer.py</code></td><td>Ready-to-customize scaffolds for common video types</td></tr>
<tr><td><b>Knowledge</b></td><td>21 rule files, ~220KB</td><td>Full Manim API coverage: equations, 3D, cameras, design, production</td></tr>
</table>

---

## Quick Start

### Prerequisites

```bash
pip install manim          # Manim Community Edition
# Also needed: LaTeX (TeX Live / MacTeX) + ffmpeg
```

### Install

```bash
git clone https://github.com/AmitSubhash/3brown1blue ~/.claude/skills/manim
```

That's it. Claude Code auto-discovers skills in `~/.claude/skills/`.

### Use

Open Claude Code in any project:

```
> Animate step-by-step how matrix multiplication works
> Create a paper explainer for this PDF on diffusion models
> Render a 3D surface with a moving camera flythrough
```

Claude reads the relevant rules, writes the scene, and renders:

```bash
manim -pql scene.py MyScene    # preview (480p, fast)
manim -pqh scene.py MyScene    # production (1080p)
manim -pqk scene.py MyScene    # 4K
```

---

## How It Works

```
                    ┌─────────────────────────────────────────────────────┐
                    │              Claude Code Manim Skill                │
                    └─────────────────────────────────────────────────────┘

  "Animate the         ┌──────────┐    ┌──────────┐    ┌──────────┐
   Euler identity" ──> │  SKILL   │──> │  Rules   │──> │ Template │
                       │  .md     │    │ (1-4 of  │    │ match    │
                       │ (entry)  │    │  21)     │    │          │
                       └──────────┘    └──────────┘    └──────────┘
                                                             │
                                                             v
                       ┌──────────┐    ┌──────────┐    ┌──────────┐
                       │  Video   │<── │  Render  │<── │  Write   │
                       │  .mp4    │    │  manim   │    │  scene   │
                       │          │    │  -pqh    │    │  .py     │
                       └──────────┘    └──────────┘    └──────────┘
                                                             │
                                            ┌────────────────┤
                                            v                v
                                     ┌────────────┐   ┌────────────┐
                                     │ safe_manim │   │  style.py  │
                                     │ .py crash  │   │  colors,   │
                                     │ prevention │   │  fonts,    │
                                     │ (6 wraps)  │   │  timing    │
                                     └────────────┘   └────────────┘
```

1. **SKILL.md** is the entry point -- Claude reads it first, sees the gotchas, picks relevant rule files
2. **Rule files** provide API knowledge: only 1-4 are loaded per task (equations, 3D, cameras, etc.)
3. **Templates** give a starting scaffold for common patterns (equation explainers, paper explainers)
4. **safe_manim.py** wraps 6 crash-prone APIs with safe alternatives
5. **style.py** enforces consistent colors, fonts, and timing across multi-scene videos

---

## What Makes It Different

| Feature | Without This Skill | With This Skill |
|---------|-------------------|-----------------|
| **Crash rate** | Claude hits ~40% of Manim's common gotchas | 12 gotchas caught before they happen |
| **Visual quality** | Generic animations, no design system | 22 patterns from 422 analyzed 3b1b frames |
| **API coverage** | Claude knows basic Manim | 21 rule files covering the full API surface |
| **Multi-scene** | Each scene is independent, inconsistent | `style.py` contract: shared colors, fonts, timing |
| **Equation work** | Frequent MathTex/Transform bugs | dim-and-reveal, TransformMatchingTex done right |
| **Paper explainers** | No structure | 5-section scaffold with domain-specific patterns |
| **3D scenes** | Hit-or-miss camera angles | ThreeDScene rules, surface best practices |
| **Production** | No quality checks | Pre/post-render checklists, container bounds, alignment |

---

## Design Philosophy

This skill encodes visual explanation principles from three masters:

| Source | Principle | In Practice |
|--------|-----------|-------------|
| **3Blue1Brown** (Sanderson) | Geometry before algebra | Show the shape first, let the equation formalize what the viewer already sees |
| **3Blue1Brown** | Structure around one "aha" | Every video needs one surprising connection that reframes everything |
| **Bret Victor** | "If you can't play with it, you don't understand it" | ValueTracker sliders over static diagrams |
| **Edward Tufte** | Annotations on the object | Labels belong on the thing, not beside it |
| **Cognitive science** | Opacity layering | Direct attention through brightness, not removal -- dim prior elements to 30% |
| **3Blue1Brown** | Persistent context | Keep prior elements visible rather than clearing the scene |

**12 core principles** live in `rules/visual-design-principles.md`.
**22 implementable patterns** (extracted from 422 3b1b frames) live in `rules/visual-design-catalog.md`.

---

## What's Included

### File Inventory

| Path | Purpose |
|------|---------|
| `SKILL.md` | Entry point -- Claude reads this first to understand capabilities and gotchas |
| `scripts/safe_manim.py` | Drop-in wrappers for 6 crash-prone Manim APIs |
| `scripts/render_scene.sh` | One-command render with quality selection (`l`/`m`/`h`/`k`) |
| `templates/style.py` | Shared color palette, font sizes, timing constants, reusable components |
| `templates/equation_explainer.py` | Dim-and-reveal equation scene template |
| `templates/paper_explainer.py` | 5-section paper explainer scaffold |
| `rules/*.md` | 21 focused rule files (see breakdown below) |

<details>
<summary><b>All 21 Rule Files</b> (click to expand)</summary>

**Core** (start here if unfamiliar with Manim)
| File | Coverage |
|------|----------|
| `first-scene-tutorial.md` | Install, hello world, render commands |
| `mobjects.md` | Mobject hierarchy, positioning, styling, VGroup |
| `animations.md` | Animation lifecycle, Transform, rate functions, composition |
| `scene-lifecycle.md` | Scene types, construct(), play/wait/add/remove |

**Equations and Math**
| File | Coverage |
|------|----------|
| `equations.md` | MathTex, submobjects, `{{ }}` notation, TransformMatchingTex |
| `equation-derivations.md` | Dim-and-reveal, step-by-step derivation patterns |
| `graphs-plots.md` | Axes, plots, parametric curves, BarChart |
| `matrices-linalg.md` | Matrix, linear transformations |
| `decorations.md` | SurroundingRectangle, Brace, Arrow annotations |

**Dynamic and 3D**
| File | Coverage |
|------|----------|
| `updaters-trackers.md` | ValueTracker, add_updater, always_redraw |
| `three-d.md` | ThreeDScene, camera angles, surfaces, 3D shapes |
| `moving-camera.md` | MovingCameraScene, zoom, pan, follow |

**Visual Design**
| File | Coverage |
|------|----------|
| `visual-design-principles.md` | 12 core principles from Tufte, Bret Victor, 3Blue1Brown |
| `visual-design-catalog.md` | 22 implementable patterns from 422 analyzed 3b1b frames |

**Video Production**
| File | Coverage |
|------|----------|
| `scene-planning.md` | Multi-scene layout templates, agent prompt structure, style.py contract |
| `paper-explainer.md` | Explainer video structure, domain-specific patterns |
| `production-quality.md` | Spatial layout, container bounds, pre/post-render quality checks |
| `animation-design-thinking.md` | Pacing, narration sync, animate vs static decisions |
| `project-organization.md` | Multi-scene projects, render scripts, file structure |
| `remotion-integration.md` | Manim + Remotion pipeline for web-embeddable video |

**Reference**
| File | Coverage |
|------|----------|
| `config-rendering.md` | Quality presets, CLI flags, output formats |
| `color-palettes.md` | Accessible palettes, color operations |
| `troubleshooting.md` | Common errors and fixes |
| `manimgl-differences.md` | Community Edition vs ManimGL comparison |

</details>

---

## Multi-Scene Video Projects

For longer videos with multiple scenes, the skill provides a project structure with `style.py` as the shared contract:

```
my_video/
├── utils/
│   └── style.py              # copy from templates/style.py, customize once
├── scenes/
│   ├── scene_01_intro.py      # imports from utils.style
│   ├── scene_02_setup.py
│   └── scene_03_reveal.py
├── render_all.sh              # renders all scenes, stitches into final video
└── media/                     # manim output (gitignore this)
```

`style.py` defines semantic colors (`primary`, `secondary`, `accent`), font sizes (`TITLE_SIZE`, `BODY_SIZE`, `EQ_SIZE`), timing constants (`HOLD_SHORT`, `HOLD_LONG`), and reusable components (`labeled_box()`, `section_title()`).

**Why this matters:** Viewers learn the visual vocabulary. "Blue = input" carries between scenes. Consistency is what separates a tutorial from a 3Blue1Brown video.

---

## License

MIT -- see [LICENSE](LICENSE) for details.

---

<p align="center">
  <sub>Built for <a href="https://github.com/anthropics/claude-code">Claude Code</a> by <a href="https://github.com/AmitSubhash">Amit Subhash</a></sub>
</p>
