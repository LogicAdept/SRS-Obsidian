<!--
reps: 0
priority: 0
-->
#DSA/Algorithms/Search #SRS

# What is bidirectional search

> [!abstract] Short answer
> Run two searches at once — one forward from the source, one backward from the target — and stop when the frontiers touch. The branching blow-up drops from roughly **b^d** nodes to about **2 · b^(d/2)**, which on wide graphs is the difference between days and seconds. Path length is the sum of the two sides' levels.

## Two frontiers and the handshake

Each side keeps its own frontier and seen set. Per step, the **smaller** frontier expands one full level — balancing work keeps memory even. When expanding a node produces a neighbor already seen by the other side, the searches have shaken hands: the answer is the source-side level plus the target-side level.

```java
static int bidirectionalBfs(Map<Integer, List<Integer>> g, int s, int t) {
    if (s == t) return 0;
    Set<Integer> frontS = new HashSet<>(Set.of(s));
    Set<Integer> frontT = new HashSet<>(Set.of(t));
    boolean[] seenS = new boolean[g.size()];
    boolean[] seenT = new boolean[g.size()];
    seenS[s] = true;
    seenT[t] = true;
    int levelS = 0, levelT = 0;
    while (!frontS.isEmpty() && !frontT.isEmpty()) {
        boolean expandS = frontS.size() <= frontT.size();   // expand the smaller frontier
        Set<Integer> front = expandS ? frontS : frontT;
        boolean[] seenMine = expandS ? seenS : seenT;
        boolean[] seenOther = expandS ? seenT : seenS;
        var next = new HashSet<Integer>();
        for (int v : front) {
            for (int n : g.get(v)) {
                if (seenOther[n]) {                         // frontiers touched: path found
                    return expandS ? levelS + 1 + levelT : levelS + levelT + 1;
                }
                if (!seenMine[n]) {
                    seenMine[n] = true;
                    next.add(n);
                }
            }
        }
        if (expandS) { frontS = next; levelS++; } else { frontT = next; levelT++; }
    }
    return -1;                                              // no path
}
```

**Listing 1.** On the undirected graph `0-1, 0-2, 1-3, 2-4, 3-5, 4-5` the search from 0 and from 5 meets after two source-side levels and one target-side level: `levelS + levelT + 1 = 3` — exactly the length of `0-1-3-5`. On a graph where 3 is unreachable it returns −1.

The backward search needs edges **into** the target direction — on a directed graph that means the reverse adjacency, which may not be available or cheap to build. The underlying level-by-level expansion is plain [[What is breadth-first search]] from both ends; the win is the exponent halving described in [[What is Big-O]] terms.

> [!warning] The first handshake is not automatically the optimal path
> The naive version returns as soon as any frontier pair touches, but a later node completing the same level can still yield a shorter total — careful implementations finish expanding the current level and take the minimum of `levelS + levelT` over all overlaps. Second trap: the textbook b^(d/2) claim assumes roughly equal branching in both directions and a balanced alternation; with a wildly lopsided frontier or a missing reverse graph, the guarantee quietly evaporates.

> [!tip] Interview answer
> Bidirectional search interleaves BFS from the source and from the target, expanding whichever frontier is smaller, until the two seen-sets intersect; the distance is the sum of the levels. The point is the exponent: 2·b^(d/2) instead of b^d — for depth 10 and branching 4, that is thousands of nodes instead of a million. It needs the target known upfront and reverse reachability; and the first meeting node must not be trusted blindly — finish the level, then take the minimum.
