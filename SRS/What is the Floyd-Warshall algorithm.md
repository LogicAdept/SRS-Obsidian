<!--
reps: 0
priority: 0
-->
#DSA/Algorithms/Graph/ShortestPath #SRS

# What is the Floyd-Warshall algorithm

> [!abstract] Short answer
> **All-pairs** shortest paths by dynamic programming over intermediate vertices: three nested loops and the recurrence `d[i][j] = min(d[i][j], d[i][k] + d[k][j])`. Cost: **O(V³)** time, O(V²) memory. Handles negative edges; a negative cycle shows up as `d[i][i] < 0`. The loop over `k` must be the **outermost** one.

## The k-th vertex decides what paths may use

The invariant: after iteration `k`, `d[i][j]` is the cheapest path from `i` to `j` allowed to pass only through vertices from `{0..k}` as intermediates. Iteration `k` asks one question for every pair: does splitting the route through vertex `k` beat the best route that avoided it? The update runs in place, and that is legitimate because row `k` and column `k` cannot improve themselves during iteration `k` (`d[k][k] = 0`), so the values being read are the previous stage's.

```java
static final long INF = Long.MAX_VALUE / 4;      // avoid overflow on INF + w

static long[][] floydWarshall(long[][] d) {
    int n = d.length;
    for (int k = 0; k < n; k++)                  // k must be the OUTER loop
        for (int i = 0; i < n; i++)
            for (int j = 0; j < n; j++)
                if (d[i][k] + d[k][j] < d[i][j])
                    d[i][j] = d[i][k] + d[k][j];
    return d;
}
```

**Listing 1.** On the digraph `0→2(1), 0→3(5), 1→3(2), 2→1(−3)` the matrix ends with `0→1 = −2` (via vertex 2) and `0→3 = 0` (0→2→1→3): negative edges shave the direct routes down. No cycle exists in that graph, so the numbers are final.

Three practical notes: initialize the matrix with zeros on the diagonal and INF where no edge exists, using a value like `INF/4` so that `INF + w` cannot overflow into a fake cheap path; a negative diagonal afterwards (`d[i][i] < 0`) certifies a negative cycle through vertex `i`; and reconstructing the actual path needs a separate `next[i][j]` successor matrix filled during the updates. The single-source counterpart with negative weights is [[What is the Bellman-Ford algorithm]]; running Dijkstra from every vertex — see [[What is Dijkstra's algorithm]] — wins on sparse graphs with non-negative weights. The problem family is [[What is the shortest path problem]].

> [!warning] k in an inner loop silently gives wrong answers
> The recurrence is defined over "paths using intermediates from a growing set", and only the outer-`k` order implements that. Swap the loops and the code still runs, still terminates, and produces plausible-looking but incorrect matrices — there is no exception to notice. Second trap: V³ dies fast — at 10,000 vertices that is 10¹² operations; all-pairs at that scale calls for repeated Dijkstra from each source on sparse graphs.

> [!tip] Interview answer
> Floyd-Warshall computes all-pairs shortest paths with a DP over intermediate vertices: for each k, try routing every pair through k — min of keep and d i k plus d k j. O(V³) time, O(V²) space, negative edges are fine, and a negative diagonal after the run signals a negative cycle. The k loop must be outermost; past a few thousand vertices I switch to repeated Dijkstra or Johnson.
