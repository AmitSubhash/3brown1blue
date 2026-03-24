---
name: Algorithms Domain Rules
description: Visual vocabulary, preferred templates, notation, and patterns for algorithms paper explainers
tags: [manim, domain, algorithms]
---

# Algorithms Explainer Rules

## Visual Vocabulary

Viewers of algorithms explainers expect these diagram types. Without them, an algorithm is just pseudocode -- there is no understanding of WHY it works:

- **State diagrams**: the data structure at each step, with the current operation highlighted
- **Pseudocode with execution cursor**: code on screen with a highlighted line that advances step by step
- **Complexity plots**: input size n on x-axis, operations on y-axis, comparing O(n log n) vs O(n^2)
- **Decision trees and recursion trees**: branching structures that show subproblem decomposition
- **Comparison tables**: algorithm A vs B on dimensions like time, space, stability, cache behavior
- **Graph/tree visualizations**: nodes and edges with state (visited/unvisited, in-queue, finalized)
- **Sorted/unsorted array bars**: classic bar chart where height encodes value, sorting creates ascending order

## Preferred Layout Templates

| Concept | Template | Reason |
|---|---|---|
| Single algorithm running on concrete data | FULL_CENTER | State diagram needs maximum space |
| Algorithm A vs Algorithm B | DUAL_PANEL | Two executions side by side |
| Pseudocode + execution state | TOP_PERSISTENT_BOTTOM_CONTENT | Code at top; data structure changes below |
| Step-by-step data structure transformation | BUILD_UP | Each step adds/removes/reorders elements |
| Complexity comparison | CHART_FOCUS | Growth curves are the main content |
| Multiple algorithms or O-classes | GRID_CARDS | One algorithm or complexity class per card |

## Domain-Specific Visual Patterns

### ALGO-1: Concrete Data Execution
Before explaining anything, run the algorithm on a small concrete input (N <= 10 elements). Show the actual data structure (array, graph, tree) on screen. As the algorithm executes, change element colors to show state: unvisited=GRAY, current=YELLOW, processed=GREEN, in-queue=BLUE. Each step is one beat -- one operation, one color change, one wait. The viewer watches the algorithm run like a debugger, not reads a description.

Template: FULL_CENTER or TOP_PERSISTENT_BOTTOM_CONTENT. Required for every algorithm introduction. Never explain an algorithm abstractly before showing it on concrete data.

### ALGO-2: Pseudocode Cursor
Place pseudocode as a VGroup of Text lines in the top-right or left panel (font: monospace via Tex \texttt{}). Add a YELLOW Rectangle behind the current line (the cursor). As execution proceeds, animate the cursor moving down using cursor.animate.move_to(lines[i]). This gives the viewer spatial context: they can always look at the code to know "where are we." Color variables in the code to match the corresponding elements in the data structure visualization.

Template: TOP_PERSISTENT_BOTTOM_CONTENT (pseudocode at top, data structure below) or DUAL_PANEL. Use for any algorithm where control flow matters (loops, recursion, conditionals).

### ALGO-3: Complexity Growth Visualization
Use CHART_FOCUS with Axes. Plot multiple curves simultaneously using different colors. For each complexity class, add an annotation showing one concrete example (e.g., n=1000, O(n^2) = 1,000,000 ops). Use always_redraw with a ValueTracker for n to sweep from 1 to N_max and show all curves growing in real time. When two curves cross, flash a YELLOW Dot at the intersection and label the crossover point.

Template: CHART_FOCUS. Use in any paper proposing a faster algorithm. Always show the constant factors, not just the asymptotic classes.

### ALGO-4: Recursion Tree Build
Show the recursive decomposition as a tree that grows top-down. Each node is a labeled_box with the subproblem input. Children appear below their parent with GrowArrow for the tree edges. After all leaves appear, animate the combine step bottom-up: leaf nodes light up GREEN, then their parent computes from them and turns GREEN, cascading upward. This makes divide-and-conquer feel like a physical process.

Template: FULL_CENTER. Use for merge sort, quicksort, FFT, any divide-and-conquer algorithm.

### ALGO-5: Before-After Array State
Show the array as a row of Rectangle bars (height encodes value) with integer labels below each bar. This is the classic sorting visualization. Each comparison swaps two bars: use self.play(Swap(bar_i, bar_j)) or ReplacementTransform. Color the sorted portion GREEN cumulatively. For algorithms with auxiliary structures (heap, pivot), show those structures in a separate VGroup below the main array, updating in sync with the main array.

Template: FULL_CENTER or DUAL_PANEL (array top, auxiliary structure bottom treated as two panels). Use for any sorting, selection, or partitioning algorithm.

## Color Semantics

```python
ALGO_COLORS = {
    "unvisited":    GRAY_B,     # elements not yet considered
    "current":      YELLOW_C,   # element being processed right now
    "in_queue":     BLUE_C,     # in queue, stack, or open set
    "finalized":    GREEN_C,    # permanently processed, sorted, found optimal
    "discarded":    GRAY,       # pruned, rejected, out of consideration
    "comparison":   PURE_YELLOW,# the two elements currently being compared
    "pivot":        RED_C,      # pivot element in partitioning
    "sorted":       GREEN_D,    # fully sorted / in final position
    "highlight":    PURE_YELLOW,# current line in pseudocode, current node
    "complexity_n2": RED_C,     # worse complexity (higher is worse)
    "complexity_nlogn": GREEN_C,# better complexity
}
```

The GRAY -> YELLOW -> GREEN -> GRAY pipeline (unvisited -> active -> done -> dimmed) is a universal state machine for algorithm animations. Viewers who have seen any sorting visualization will recognize it immediately.

## Notation Conventions

- Array indexing: use 0-based indexing consistently; label indices below each bar or node
- Big O: `\mathcal{O}(n \log n)` not `O(n log n)` -- calligraphic O looks more professional
- Comparison count: show a live counter `\text{comparisons: } k` as a Running Counter (pattern #3)
- Invariant: always state the loop invariant on screen when introducing it; use a colored border on the invariant region of the array
- Swaps vs comparisons: track both with separate counters when they are independently meaningful (e.g., QuickSort analysis)
- Graph notation: label vertices with letters (A, B, C...) not numbers when the graph has identity; label with numbers when it is a generic graph used for complexity analysis

## Equation Presentation Order

1. Run the algorithm on a concrete example (ALGO-1: viewers see it work)
2. Identify the pattern in what they just watched (what invariant was maintained?)
3. State the algorithm formally (pseudocode, pattern ALGO-2)
4. Prove correctness (the invariant holds at each step -- BUILD_UP, one step per beat)
5. Analyze complexity (ALGO-3: show the growth curve)
6. Compare to alternatives (DUAL_PANEL or CHART_FOCUS with multiple curves)

Never prove correctness before showing the algorithm run on concrete data. Proofs without examples feel unmotivated and the viewer has nothing to anchor the induction to.

## Common Explanation Mistakes

- **Abstract description instead of execution**: saying "the algorithm visits each node" without showing nodes changing color. Fix: always use ALGO-1 with concrete data as the first scene.
- **Too large an example**: using N=50 so the viewer cannot track individual elements. Fix: use N <= 10 for demonstrations; scale up only for complexity visualization.
- **Pseudocode without a cursor**: code on screen but no indicator of which line is executing. Fix: always use ALGO-2's cursor rectangle.
- **Complexity plots without concrete numbers**: showing O(n^2) vs O(n log n) curves without showing what that means for n=1000. Fix: annotate the crossover and at least one concrete (n, cost) point.
- **Correctness proof before the algorithm makes intuitive sense**: proving the loop invariant without first showing why the invariant is useful. Fix: show the algorithm succeed on a case where a "wrong" approach fails, THEN prove correctness.

## Scene Skeleton Recommendations

```
Scene 1 (Hook): Show the algorithm solving a problem that would be hard to do by hand
Scene 2 (Naive Approach): Show the brute force solution running -- slow but obviously correct
Scene 3 (Concrete Execution): Run the new algorithm on the same input (ALGO-1)
Scene 4 (Pseudocode): Walk through the code with the cursor (ALGO-2) tied to the execution
Scene 5 (Correctness): The key invariant that makes it work (BUILD_UP proof sketch)
Scene 6 (Complexity): Growth curves compared to naive approach (ALGO-3)
Scene 7 (Comparison): Table or side-by-side vs related algorithms (DUAL_PANEL or GRID_CARDS)
Scene 8 (Takeaway): The algorithmic idea, stripped of implementation details
```
