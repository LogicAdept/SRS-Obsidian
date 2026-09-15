<!--
reps: 0
priority: 0
-->
#DSA/Algorithms/Search #SRS

# What is the A star algorithm

> [!abstract] Short answer
> Best-first search guided by **f(v) = g(v) + h(v)**: the cost already paid plus an optimistic estimate of what remains. If `h` is **admissible** (never overestimates the true remaining cost), the first time the goal is popped its cost is **optimal**. With `h = 0` A* degenerates exactly to Dijkstra; with priority = `h` alone it degenerates to greedy best-first search.

## What the two terms buy

`g` keeps the search honest — a node reached cheaply stays interesting even if its heuristic looks bad. `h` aims the search at the goal, expanding nodes that are both cheap-so-far and geographically promising. The PQ is ordered by `f`, and the pop of a vertex with a better-known `g` value than recorded is skipped, the same lazy-deletion pattern Dijkstra uses.

```java
static int aStar(Map<Integer, List<Edge>> g, int start, int goal, int[] h) {
    var open = new PriorityQueue<int[]>(Comparator.comparingInt(a -> a[1] + h[a[0]]));
    Map<Integer, Integer> best = new HashMap<>();
    open.add(new int[]{start, 0});
    best.put(start, 0);
    while (!open.isEmpty()) {
        int[] cur = open.poll();
        int v = cur[0], gCost = cur[1];
        if (v == goal) return gCost;
        if (gCost > best.getOrDefault(v, Integer.MAX_VALUE)) continue;
        for (Edge e : g.getOrDefault(v, List.of())) {
            int nCost = gCost + e.w();
            if (nCost < best.getOrDefault(e.to(), Integer.MAX_VALUE)) {
                best.put(e.to(), nCost);
                open.add(new int[]{e.to(), nCost});
            }
        }
    }
    return -1;
}
```

**Listing 1.** With edges `0→1(1), 0→2(4), 1→2(2), 1→3(6), 2→3(3)` and heuristic `h = {3, 2, 1, 0}` (a valid straight-line guess toward 3), A* returns cost **6** via `0-1-2-3` — the true optimum — while never expanding anything irrelevant.

Admissibility (`h ≤ true remaining cost`) is what makes the first pop of the goal final: an unpopped node could still reach it at `f` no better, and admissible `h` guarantees the goal's `f` is never an overestimate. If `h` is also **consistent** (`h(v) ≤ w(v, u) + h(u)`), recorded `g` values never need reopening and each vertex is expanded once. Classic admissible choices on grids: Manhattan distance for 4-directional movement, octile for 8, Euclidean when movement is unconstrained. The pure-heuristic sibling is [[What is best-first search]]; the `h = 0` baseline is [[What is Dijkstra's algorithm]]; the problem family is [[What is the shortest path problem]].

> [!warning] An inadmissible heuristic silently trades optimality for speed
> If `h` can overestimate, a cheaper route may still be sitting in the queue when the goal pops — A* then returns a valid but suboptimal path with no error signal. That is sometimes the right trade (weighted A*, weighted heuristics), but it must be a decision, not an accident. Second trap: admissible but wildly loose heuristics (always returning 0) leave you running plain Dijkstra while paying for the PQ.

> [!tip] Interview answer
> A* is best-first search on f = g + h: cost so far plus an optimistic estimate to the goal. With an admissible heuristic the first time the goal is dequeued its cost is optimal; with a consistent heuristic every node expands at most once. h = 0 makes it Dijkstra, so the heuristic is pure speedup. I check admissibility explicitly — an overestimating heuristic is fast but silently suboptimal.
