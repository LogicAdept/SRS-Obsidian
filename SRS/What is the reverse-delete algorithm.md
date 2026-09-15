<!--
reps: 0
priority: 0
-->
#DSA/Algorithms/Graph/ReverseDelete #SRS

# What is the reverse-delete algorithm

> [!abstract] Short answer
> The mirror image of Kruskal: start with the **full graph**, scan edges from **heaviest to lightest**, and delete every edge whose removal keeps the graph connected. What survives is exactly the minimum spanning tree — every surviving edge was a **bridge** at the moment it was examined.

## Deletion is the primitive, not addition

An edge is dispensable precisely when its endpoints remain connected without it — that means a cheaper alternative route exists, so keeping it can never help a minimum tree. The heaviest redundant edges go first; by the time the scan reaches a light edge, everything that could replace it is either gone or the edge is load-bearing. Sorting costs O(E log E); each candidate needs a connectivity check over the surviving graph, O(V + E) by BFS, giving the textbook O(E · (V + E)) total.

```java
static long reverseDeleteMst(int n, List<UEdge> edges) {
    edges.sort(Comparator.comparingInt((UEdge e) -> e.w()).reversed());
    boolean[] alive = new boolean[edges.size()];         // start with the full graph
    Arrays.fill(alive, true);
    for (int i = 0; i < edges.size(); i++) {             // heaviest first
        alive[i] = false;                                // try deleting this edge
        UEdge e = edges.get(i);
        if (!connected(n, edges, alive, e.from(), e.to())) {
            alive[i] = true;                             // deletion broke connectivity: bridge, keep
        }
    }
    long total = 0;
    for (int i = 0; i < edges.size(); i++) {
        if (alive[i]) total += edges.get(i).w();
    }
    return total;
}
```

**Listing 1.** The `connected` helper is a plain BFS over the `alive` edges. On edges `0-1(2), 0-3(6), 1-2(3), 1-3(8), 1-4(5), 2-4(7), 3-4(9)` the survivors are 2, 3, 5, 6 — total **16**, identical to Kruskal and Prim on the same graph.

The shortcut people reach for — "scan descending, keep an edge if its endpoints are not yet connected in a DSU" — is where the trap lives, and it is dissected in the warning below. The honest incremental structure is the mirror of [[What is Kruskal's algorithm]], which adds the cheapest safe edges, and the connectivity core is [[What is the union-find data structure]]. Like Kruskal, it tolerates disconnected input, returning the minimum spanning forest. The cut-property justification is shared with [[What is Prim's algorithm]].

> [!warning] "Keep if not yet connected" while scanning heaviest-first builds a MAXIMUM spanning tree
> Reusing Kruskal's union pattern with a reversed sort direction is not reverse-delete — it greedily keeps the heaviest edges first and produces the heaviest spanning tree (on the listing's graph: 30 instead of 16; the harness check caught exactly this). The direction of the primitive is inverted: reverse-delete starts from everything and **deletes** what stays connected. An edge survives only if it is a bridge. An equivalent DSU formulation exists, but it must ask about connectivity among strictly lighter edges, not about what has been kept so far.

> [!tip] Interview answer
> Reverse-delete is Kruskal upside down: sort edges descending, try to delete each one, and keep it only when deletion disconnects the graph — survivors are the MST, total 16 on my test graph, same as Kruskal and Prim. The connectivity re-test makes naive runs O(E · (V + E)) on top of the O(E log E) sort. The classic mistake is porting Kruskal's union logic to a descending scan — that builds the maximum spanning tree.
