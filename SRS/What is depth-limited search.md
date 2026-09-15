<!--
reps: 0
priority: 0
-->
#DSA/Algorithms/Search #SRS

# What is depth-limited search

> [!abstract] Short answer
> Depth-first search with a hard **depth cutoff**: recursion stops once the limit reaches zero. It trades completeness for bounded time and memory — O(limit) stack instead of unbounded depth — and it is the engine inside **iterative deepening**, which reruns it with limits 0, 1, 2, … until the goal appears.

## The cutoff and the bookkeeping

Each recursive call carries the remaining budget. At the goal — return success; at zero — report failure for that branch and unwind. A seen-set restricted to the current path prevents cycling within the budget, which is the same discipline the parent algorithm needs — see [[What is depth-first search]] for the stack-driven baseline.

```java
static boolean dls(Map<Integer, List<Integer>> g, int v, int goal, int limit, boolean[] seen) {
    if (v == goal) return true;
    if (limit == 0) return false;
    seen[v] = true;
    for (int next : g.get(v)) {
        if (!seen[next] && dls(g, next, goal, limit - 1, seen)) return true;
    }
    return false;
}
```

**Listing 1.** On the chain `0→1→2→3`, searching for 2 with limit 1 fails (the goal sits two hops away), with limit 2 it succeeds. The cutoff is what makes the search terminate on graphs with cycles without a global visited set.

The catch is right in the numbers: if the goal is deeper than the limit, the search is **incomplete** — it will confidently report "not found" about a goal that exists. Rerunning with a growing limit fixes that: iterative deepening repeats the wasted shallow work, but the total is dominated by the last iteration (branching b: b + b² + … + b^d ≈ b^(d+1)/(b−1)), so asymptotically it matches breadth-first search while using O(depth) memory instead of O(b^d). BFS's own trade-offs are in [[What is breadth-first search]].

> [!warning] "Not found" at limit d means nothing
> A depth-limited miss is not evidence of absence — the goal may simply live one level deeper. Reporting failure without stating the cutoff is the classic misuse. Second trap: reusing one seen array across iterative-deepening iterations; the array must be reset per run, or shallower iterations will poison the deeper ones with stale visited marks.

> [!tip] Interview answer
> Depth-limited search is DFS with a recursion budget: goal check, then limit check, then recurse with limit minus one. It bounds memory to O(limit) but loses completeness — a miss only means "not within the limit". Its real role is as the building block of iterative deepening, which reruns it with growing limits and gets BFS-like completeness with DFS-like memory, at asymptotically the same node count as BFS.
