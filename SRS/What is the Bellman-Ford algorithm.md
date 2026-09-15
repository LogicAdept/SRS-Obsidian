<!--
reps: 0
priority: 0
-->
#DSA/Algorithms/Graph/ShortestPath #SRS

# What is the Bellman-Ford algorithm

> [!abstract] Short answer
> Single-source shortest paths that **tolerate negative edge weights**. It relaxes every edge, repeating that sweep **V − 1 times**; after that, distances are final — unless one more sweep can still relax something, which proves a reachable **negative cycle**. Cost: **O(V · E)** time, O(V) space. Slower than Dijkstra but with no weight restrictions.

## Why V − 1 passes are exactly enough

A shortest path visits each vertex at most once, so it contains at most V − 1 edges. Pass `i` guarantees that every shortest path using at most `i` edges is already correct — distances "grow" one hop per sweep. After V − 1 sweeps every acyclic shortest path is found. A pass that changes nothing means the table has converged and the loop can exit early; on a graph where the frontier grows one layer per pass, that halves the work.

```java
record DirEdge(int from, int to, int w) {}

static long[] bellmanFord(int n, List<DirEdge> edges, int src) {
    long[] dist = new long[n];
    Arrays.fill(dist, Long.MAX_VALUE);
    dist[src] = 0;
    for (int i = 1; i < n; i++) {                // n-1 passes are enough
        for (DirEdge e : edges) {
            if (dist[e.from()] != Long.MAX_VALUE && dist[e.from()] + e.w() < dist[e.to()]) {
                dist[e.to()] = dist[e.from()] + e.w();
            }
        }
    }
    for (DirEdge e : edges) {                    // pass n: any relaxation = negative cycle
        if (dist[e.from()] != Long.MAX_VALUE && dist[e.from()] + e.w() < dist[e.to()]) {
            throw new IllegalStateException("negative cycle reachable from src");
        }
    }
    return dist;
}
```

**Listing 1.** On edges `0→1(4), 0→2(5), 1→3(−3), 2→1(1), 2→3(6)` it returns `[0, 4, 5, 1]`: the −3 edge makes the route through vertex 1 to vertex 3 cost 1, beating the direct weight-6 edge. On `0→1(1), 1→2(−2), 2→1(1)` the final sweep still finds a relaxation and the method throws — the cycle `1→2→1` sums to −1.

The guard against `Long.MAX_VALUE` matters: relaxing from an unreachable vertex would otherwise turn "infinity plus something" into a fake finite distance. For all-pairs needs the same job is done by [[What is the Floyd-Warshall algorithm]]; for non-negative weights the faster default is [[What is Dijkstra's algorithm]]. Both belong to the family in [[What is the shortest path problem]].

> [!warning] Negative edge is not a negative cycle
> The classic interview conflation. A negative **edge** is ordinary — it simply makes some paths cheaper, and Bellman-Ford handles it natively. A negative **cycle** (a loop whose total weight is negative) reachable from the source destroys the problem: "shortest path" can loop down to −∞, and the correct answer is to report it, which is exactly what pass V does. Also note the detection says nothing about vertices not reachable from the source — their cycles stay invisible.

> [!tip] Interview answer
> Bellman-Ford relaxes all edges V − 1 times — one sweep per possible hop count of a shortest path — giving O(V · E) time and full support for negative weights. A V-th sweep that still finds a relaxation certifies a reachable negative cycle, which Dijkstra cannot even survive. In practice I add the early-exit when a sweep changes nothing; distributed routing protocols use the same relaxation idea per node.
