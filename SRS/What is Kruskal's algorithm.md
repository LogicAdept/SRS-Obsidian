<!--
reps: 0
priority: 0
-->
#DSA/DataStructures/Graph #DSA/Algorithms/Greedy #SRS

# What is Kruskal's algorithm

> [!abstract] Short answer
> Builds a **minimum spanning forest**: sort all edges by weight, then keep an edge exactly when its endpoints are in **different components** of a union-find — the first edge examined that would close a cycle is skipped. Cost: **O(E log E)** for the sort; the union-find passes are near-linear. Works on disconnected graphs, where it returns a forest, not a tree.

## Sort, then let the DSU veto cycles

The scan is one pass over sorted edges. `union(a, b)` returning `false` means `find(a) == find(b)` — the endpoints are already connected by cheaper edges, so this edge is the most expensive way to close that cycle and is discarded. Kept edges total exactly V − 1 on a connected graph.

```java
record UEdge(int from, int to, int w) {}

static long kruskalMst(int n, List<UEdge> edges) {
    edges.sort(Comparator.comparingInt(e -> e.w()));
    var dsu = new Dsu(n);
    long total = 0;
    for (UEdge e : edges) {
        if (dsu.union(e.from(), e.to())) total += e.w();  // kept only if it joins two trees
    }
    return total;
}
```

**Listing 1.** On edges `0-1(2), 0-3(6), 1-2(3), 1-3(8), 1-4(5), 2-4(7), 3-4(9)` the scan keeps weights 2, 3, 5, 6 and rejects 7, 8, 9 — total **16**, matching [[What is Prim's algorithm]] on the same graph. The component test itself is [[What is the union-find data structure]].

Because the veto is a connectivity question and not a position question, edge order within equal weights does not matter, and disconnected inputs simply yield one tree per component. The cycle-avoidance here is the mirror image of the reverse-delete method, which starts from the full graph and **removes** the most expensive redundant edges — see [[What is the reverse-delete algorithm]]. The greedy justification (cut property) is shared with Prim.

> [!warning] A visited flag is not a cycle test
> Checking `visited[from] && visited[to]` instead of `find(from) == find(to)` is wrong: both endpoints can already be visited yet live in **different** components, where the edge must be kept. Only the DSU answers the question "already connected by cheaper edges?". Second trap: `Arrays.sort` on a boxed edge array costs O(E log E) either way, but comparing with a comparator that can return 0 for distinct equal-weight edges is fine — ties just mean several MSTs exist, and any of them is minimal.

> [!tip] Interview answer
> Kruskal sorts all edges ascending and sweeps once, keeping an edge only if union-find says its endpoints are in different components — otherwise that edge would be the priciest way to close a cycle. O(E log E) dominated by the sort, near-linear DSU work. It naturally produces a minimum spanning forest on disconnected graphs, unlike Prim. With distinct weights the MST is unique, so Prim and Kruskal return the same total.
