<!--
reps: 0
priority: 0
-->
#DSA/Algorithms/Search #SRS

# What is best-first search

> [!abstract] Short answer
> A greedy search that always expands the node whose **heuristic** `h(v)` — estimated distance to the goal — looks smallest, using a priority queue. It finds **some** path quickly, but has **no optimality guarantee**: cheap-looking steps can lead down an expensive road. Formally it is A* with the `g` term removed.

## The priority queue is the whole idea

The frontier is a PQ ordered by `h` only. Pop the most promising node, expand its neighbors, repeat until the goal pops. A visited set keeps it finite on cyclic graphs. Because the algorithm ignores what it has already spent, it commits early to whatever region *looks* close — which is exactly why it is fast on well-behaved heuristics and exactly why it can be wrong.

```java
// unweighted adjacency for the search; edge costs live in the caller for the optimality check
static List<Integer> greedyBestFirst(Map<Integer, List<Integer>> g, int start, int goal, int[] h) {
    var open = new PriorityQueue<Integer>(Comparator.comparingInt(v -> h[v]));
    Map<Integer, Integer> parent = new HashMap<>();
    Set<Integer> visited = new HashSet<>();
    open.add(start);
    visited.add(start);
    while (!open.isEmpty()) {
        int v = open.poll();
        if (v == goal) break;
        for (int next : g.getOrDefault(v, List.of())) {
            if (!visited.contains(next)) {
                visited.add(next);
                parent.put(next, v);
                open.add(next);
            }
        }
    }
    if (!visited.contains(goal)) return List.of();
    var path = new ArrayList<Integer>();
    for (Integer at = goal; at != null; at = parent.get(at)) path.add(at);
    Collections.reverse(path);
    return path;
}
```

**Listing 1.** With `h = {3, 1, 1, 0}` and real edge costs `0-1 = 1, 1-3 = 8, 0-2 = 2, 2-3 = 3`, the search returns the path `0-1-3` with total cost **9**, while the optimal path `0-2-3` costs **5** — both neighbors of the start have the same `h`, so the greedy choice is a coin flip that happens to be wrong.

Where optimality matters, `g` must re-enter the priority: that is exactly [[What is the A star algorithm]], optimal with an admissible heuristic. When weights are absent altogether, plain [[What is breadth-first search]] gives fewest-edge paths and needs no heuristic at all. The PQ mechanics are the same as in any heap-driven search — see [[What is a heap as a data structure]].

> [!warning] Greedy best-first is not A*
> The common interview slip: both use "a heuristic and a priority queue", but A* orders by `g + h` and is optimal under admissibility; greedy best-first orders by `h` and answers "a path, quickly". On maze-like inputs it also has a failure mode of its own: convex obstacles lure it into dead ends it must back out of, expanding more nodes than the apparently "smarter" A* would.

> [!tip] Interview answer
> Best-first search is the greedy variant: a priority queue ordered by the heuristic alone, always expanding whatever looks closest to the goal. It is fast and finds a valid path, but ignores cost already paid, so nothing about the path is optimal — my example returns cost 9 where the optimum is 5. Add the g term back and it becomes A*; drop the weights and BFS is enough.
