<!--
reps: 0
priority: 0
-->
#DSA/Algorithms/Graph/ShortestPath #DSA/DataStructures/Graph #SRS

# What is Dijkstra's algorithm

> [!abstract] Short answer
> Single-source shortest paths for graphs with **non-negative** edge weights. It greedily finalizes the closest not-yet-final vertex, relaxes its outgoing edges, and repeats, using a priority queue. Complexity **O((V + E) log V)** with a binary heap. Negative edges break the greedy invariant — that is Bellman-Ford territory.

## Finalization is the invariant

Each pop from the priority queue yields the vertex whose current distance is the true minimum: no other route can be shorter, because any alternative would have to leave the queue through something already no closer. After the pop the vertex is final — its distance never changes again. Every relaxation that improves a neighbor's distance reinserts that neighbor into the queue. Java's `PriorityQueue` has no decrease-key operation, so improved entries are simply added again; the stale ones are skipped by the `dist` comparison.

```java
record Edge(int to, int w) {}

static long[] dijkstra(List<Edge>[] g, int src) {
    long[] dist = new long[g.length];
    Arrays.fill(dist, Long.MAX_VALUE);
    dist[src] = 0;
    var pq = new PriorityQueue<long[]>(Comparator.comparingLong(a -> a[0]));
    pq.add(new long[]{0, src});
    while (!pq.isEmpty()) {
        long[] top = pq.poll();
        int v = (int) top[1];
        if (top[0] > dist[v]) continue;          // stale entry, skip
        for (Edge e : g[v]) {
            if (dist[v] + e.w() < dist[e.to()]) {
                dist[e.to()] = dist[v] + e.w();
                pq.add(new long[]{dist[e.to()], e.to()});
            }
        }
    }
    return dist;
}
```

**Listing 1.** Lazy-deletion Dijkstra. On the graph `0→1(4), 0→2(1), 2→1(2), 1→3(1), 2→3(5)` it returns `[0, 3, 1, 4]`: vertex 1 is reached cheaper through vertex 2 (1 + 2) than by the direct weight-4 edge.

The queue holds at most O(E) entries under lazy deletion, and each pop or insert costs O(log E) = O(log V) on a connected graph. The same heap machinery that drives it is dissected in [[What is a heap as a data structure]], and the per-operation costs in [[What are the time complexities of PriorityQueue operations]]. When negative weights are possible, the finalization invariant dies — see [[What is the Bellman-Ford algorithm]], which relaxes without finalizing. The problem family itself is [[What is the shortest path problem]].

> [!warning] Negative edges break it — no "but if you are careful"
> Once a vertex is popped, Dijkstra never revisits it. A negative edge discovered later could have shortened that vertex's path, and by then it is too late: the wrong distance has already propagated. Restarting or re-processing turns it into Bellman-Ford by another name. The popular claim "Dijkstra works on negative weights if you handle them carefully" is simply false for the algorithm as defined — non-negative weights are a precondition, not a detail.

> [!tip] Interview answer
> Dijkstra solves single-source shortest paths with non-negative weights: a priority queue ordered by tentative distance, pop the closest vertex — it is final at that moment — relax its edges, skip stale queue entries. O((V + E) log V) with a binary heap, no decrease-key needed with lazy insertion. Negative edges are out of scope because finalization can no longer be justified; Bellman-Ford covers that case.
