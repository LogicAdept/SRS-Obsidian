<!--
reps: 0
priority: 0
-->
#DSA/DataStructures/Graph #DSA/Algorithms/Greedy #SRS

# What is Prim's algorithm

> [!abstract] Short answer
> Builds a **minimum spanning tree** by growing a single tree from an arbitrary seed: at every step add the **cheapest edge that crosses** from the tree to a new vertex. With a binary heap it runs in **O(E log V)**. The greedy step is justified by the cut property — the cheapest edge across any cut is safe to take.

## One tree, a heap of crossing edges

The priority queue holds edges with exactly one endpoint inside the tree. Pop the cheapest; if its far endpoint is already in the tree, skip it (a stale entry — the lazy-deletion pattern again); otherwise admit the vertex, add the edge's weight, and push all edges leaving the new vertex. The seed costs 0, so the total accumulates V − 1 edges.

```java
record Vw(int to, int w) {}

static long primMst(List<Vw>[] g) {
    boolean[] in = new boolean[g.length];
    var pq = new PriorityQueue<Vw>(Comparator.comparingInt(e -> e.w()));
    pq.add(new Vw(0, 0));                        // seed vertex 0 at cost 0
    long total = 0;
    while (!pq.isEmpty()) {
        Vw e = pq.poll();
        if (in[e.to()]) continue;
        in[e.to()] = true;
        total += e.w();
        for (Vw next : g[e.to()]) {
            if (!in[next.to()]) pq.add(next);
        }
    }
    return total;
}
```

**Listing 1.** On the undirected graph with edges `0-1(2), 0-3(6), 1-2(3), 1-3(8), 1-4(5), 2-4(7), 3-4(9)` the total is **16** — the same tree that [[What is Kruskal's algorithm]] and the reverse-delete method produce on the same graph, because with distinct weights the MST is unique.

Prim's natural habitat is a **dense** graph: the heap only ever holds edges touching the current tree, while Kruskal must sort all E edges upfront. The heap machinery and its costs are detailed in [[What is a heap as a data structure]] and [[What are the time complexities of PriorityQueue operations]]. It assumes a **connected** graph — on a forest it builds the tree of the seed's component only; Kruskal handles disconnection naturally. The greedy framing it shares with the rest of the family is in [[What is a greedy algorithm]].

> [!warning] Prim is not Dijkstra with a different name
> The classic conflation: both pop from a priority queue and both relax edges. The difference is what the priority means. Dijkstra's key is the **total distance from the source** (`dist[u] + w`); Prim's key is the **weight of a single crossing edge** — nothing is ever accumulated along the path. Swap them and Dijkstra's distances give a valid but non-minimal spanning tree, and Prim's keys give wrong shortest-path distances.

> [!tip] Interview answer
> Prim grows one MST from a seed vertex using a priority queue of crossing edges: pop the cheapest, skip stale entries, admit the vertex, push its outgoing edges — O(E log V) with a binary heap. Correctness comes from the cut property: the lightest edge across the tree-to-rest cut is always safe. Unlike Kruskal it needs a connected graph; unlike Dijkstra it never accumulates path distance — the priority is a single edge weight.
