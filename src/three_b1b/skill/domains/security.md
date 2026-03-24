---
name: Security Domain Rules
description: Visual vocabulary, preferred templates, notation, and patterns for security/cryptography paper explainers
tags: [manim, domain, security]
---

# Security Explainer Rules

## Visual Vocabulary

Viewers of security explainers expect these diagram types. Without them, the attack or defense remains abstract and unverifiable:

- **Threat model diagrams**: system boundary as a rectangle, attacker outside it with an arrow pointing in
- **Exploit chain walkthroughs**: numbered steps, each building on the previous, showing state at each stage
- **Trust boundary maps**: which components can talk to which, with privilege levels color-coded
- **Memory layout diagrams**: stack/heap as a vertical rectangle with labeled regions and addresses
- **Cryptographic protocol flows**: message sequence charts with labeled arrows between parties
- **Correct vs vulnerable code**: side-by-side comparison, highlighting the exact difference
- **Coverage maps**: explored vs unexplored state space, shown as a filled/unfilled region

## Preferred Layout Templates

| Concept | Template | Reason |
|---|---|---|
| Single attack/defense demonstration | FULL_CENTER | The exploit sequence IS the content |
| Correct behavior vs vulnerable behavior | DUAL_PANEL | The contrast is the key insight |
| System architecture + attack path | TOP_PERSISTENT_BOTTOM_CONTENT | System stays visible as attack unfolds |
| Multi-step exploit chain | BUILD_UP | Steps must appear in order |
| Coverage / fuzzing results | CHART_FOCUS | Progress over time is the metric |
| Multiple vulnerability classes | GRID_CARDS | Each class in its own annotated panel |

## Domain-Specific Visual Patterns

### SEC-1: Threat Model Setup
Draw the system boundary as a large rectangle (BLUE_C stroke, fill_opacity=0.05). Inside: system components as labeled boxes. Outside: the attacker as a labeled circle with a RED border. Draw the attack surface as a dashed segment of the boundary in RED. Use GrowArrow to show the attacker's entry vector. This diagram stays on screen (dimmed to DIM_OPACITY) throughout the entire video as persistent context.

Template: FULL_CENTER, then transitions to TOP_PERSISTENT_BOTTOM_CONTENT when zooming into specific components. Use at the start of any security paper.

### SEC-2: Exploit Chain Step-by-Step
Each step in the chain gets its own beat. Show the system state as a diagram (e.g., memory layout, call stack, process tree). Then animate the attacker's action: an arrow appears, a value changes color, a buffer fills up past its boundary (a Rectangle extending beyond a dashed boundary line). After each step, add a numbered badge (YELLOW circle with step number) and a one-line caption. Steps accumulate on screen so the viewer can see the full chain at any point.

Template: BUILD_UP. Use for buffer overflows, use-after-free, privilege escalation, or any multi-step exploit.

### SEC-3: What Should Happen vs What Does Happen
DUAL_PANEL. Left panel labeled "Expected" (GREEN border), right panel labeled "Actual" (RED border). Both show the same operation being performed. In the left panel, the check passes and access is granted. In the right panel, the vulnerable path is highlighted and access is incorrectly granted. Use identical layout in both panels so the viewer's eye can directly diff the two paths.

Template: DUAL_PANEL. Use for authentication bypass, access control flaws, or any case where the spec and implementation diverge.

### SEC-4: Memory Layout Diagram
Draw the address space as a tall rectangle occupying the left 40% of the frame. Divide it into regions (stack, heap, BSS, text) using horizontal DashedLine separators. Color each region: stack=BLUE_C, heap=GREEN_C, BSS=GRAY, text=TEAL_C. Animate data writing into regions (a filling Rectangle inside the region). Show the overflow as the fill extending past the dashed boundary into the next region, turning RED when it crosses.

Template: DUAL_PANEL (memory layout left, code/explanation right) or FULL_CENTER. Use for memory corruption vulnerabilities.

### SEC-5: Protocol Message Sequence
Three vertical lines representing participants (e.g., Client, Server, Attacker). Messages are horizontal arrows between lines, labeled with the message content. Legitimate messages in WHITE, attacker-injected messages in RED. Animate arrows with GrowArrow in the correct order. For replay or MITM attacks, show the attacker intercepting a message (arrow changes direction and color) before forwarding a modified version.

Template: FULL_CENTER. Use for cryptographic protocol attacks, man-in-the-middle, replay attacks.

## Color Semantics

```python
SEC_COLORS = {
    "trusted":      BLUE_C,     # trusted components, expected behavior
    "untrusted":    RED_C,      # attacker-controlled, dangerous, untrusted input
    "boundary":     GRAY_B,     # system boundaries, interfaces
    "attack_path":  RED_D,      # the actual exploit path
    "safe":         GREEN_C,    # safe behavior, successful defense
    "vulnerable":   RED_C,      # vulnerable code, flawed check
    "highlight":    YELLOW_C,   # the specific byte/instruction being discussed
    "overflow":     PURE_RED,   # buffer overflow, out-of-bounds access
    "fixed":        GREEN_D,    # the patched/correct version
    "attacker":     MAROON_C,   # the attacker entity
}
```

The trusted=blue / untrusted=red mapping mirrors how security tools (browser indicators, TLS locks) already work in the viewer's mind. Exploit severity can be shown through saturation: more saturated red = higher severity.

## Notation Conventions

- Memory addresses: always shown in hex, e.g. `\texttt{0x7fff...}` in TEAL_C monospace
- Byte sequences: `\texttt{AA AA AA...}` for padding, `\texttt{90 90}` for NOPs
- CVE numbers: include in the scene title when discussing a real vulnerability, e.g. `\text{CVE-2021-44228}`
- Privilege levels: use ring notation (Ring 0 = kernel, Ring 3 = user) when relevant
- Trust levels: show as concentric rectangles (inner = most trusted, outer = least trusted)
- Code snippets: use Tex with `\texttt{}` or a Rectangle background with BLUE_E fill for code blocks

## Equation Presentation Order

Security papers rarely use equations. The "equation" in security is the exploit chain. Prioritize:

1. Show the system as it is supposed to work (SEC-3 left panel, or SEC-5 legitimate flow)
2. Identify the assumption or invariant that the vulnerability breaks
3. Show where that assumption fails (highlight with YELLOW SurroundingRectangle)
4. Build the exploit chain step by step (SEC-2)
5. Show the impact (what the attacker can now do that they could not before)
6. Show the fix (SEC-3 right panel with the corrected check highlighted in GREEN)

## Common Explanation Mistakes

- **Starting with the vulnerable code**: showing the buggy code before the viewer knows what correct behavior looks like. Fix: always show SEC-3's expected behavior first, then the vulnerable deviation.
- **Abstract "the attacker sends a packet"**: no visualization of what the packet contains or what changes in the system. Fix: always show the memory/state diagram before and after (SEC-4 or SEC-2).
- **Skipping the threat model**: jumping straight into the exploit without establishing what the attacker can and cannot control. Fix: always show SEC-1 first.
- **No step numbering**: viewers lose track of where they are in a multi-step exploit. Fix: always use SEC-2's numbered badge pattern.
- **Only showing the attack, not the fix**: viewers leave understanding how to attack but not how to defend. Fix: always end with the patched version in GREEN.

## Scene Skeleton Recommendations

```
Scene 1 (Hook): Show the impact -- what the attacker achieves (root shell, data leak, crash)
Scene 2 (Threat Model): System diagram with trust boundaries and attacker location (SEC-1)
Scene 3 (Normal Behavior): What should happen -- the legitimate flow (SEC-3 left, or SEC-5)
Scene 4 (Vulnerability): The specific assumption that fails, highlighted in the diagram
Scene 5 (Exploit): Step-by-step attack chain (SEC-2)
Scene 6 (Root Cause): The exact code/design flaw (SEC-3 or SEC-4 at the instruction level)
Scene 7 (Fix): The patch applied, showing before/after (DUAL_PANEL with SEC-3)
Scene 8 (Takeaway): The class of vulnerability and the defensive principle it illustrates
```
