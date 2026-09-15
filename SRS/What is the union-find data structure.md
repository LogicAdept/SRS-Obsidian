<!--
reps: 0
priority: 0
-->
#DSA/DataStructures/UnionFind #SRS

# What is the union-find data structure

> [!abstract] Short answer
> A **disjoint-set forest**: n elements partitioned into sets, supporting `find(v)` (which set does v belong to?) and `union(a, b)` (merge two sets) in **O(α(n)) amortized** — α is the inverse Ackermann function, ≤ 4 for any input that fits in the observable universe, so effectively constant. No splitting: sets merge but never come apart.

## Parent forest, two optimizations, one guarantee

Each set is a tree of parent pointers; the root is the set's identifier. `find` walks up to the root — and **path halving** points every visited node at its grandparent, flattening the tree as a side effect. `union` finds both roots and attaches the **smaller** tree under the **larger** (union by size), keeping trees shallow. Either optimization alone gives O(log n); only both together give the α(n) bound.

```java
static final class Dsu {
    private final int[] parent, size;

    Dsu(int n) {
        parent = new int[n];
        size = new int[n];
        Arrays.fill(size, 1);
        for (int i = 0; i < n; i++) parent[i] = i;
    }

    int find(int v) {
        while (parent[v] != v) {
            parent[v] = parent[parent[v]];       // path halving
            v = parent[v];
        }
        return v;
    }

    boolean union(int a, int b) {
        a = find(a);
        b = find(b);
        if (a == b) return false;                // already one tree
        if (size[a] < size[b]) { int t = a; a = b; b = t; }
        parent[b] = a;
        size[a] += size[b];
        return true;
    }

    boolean connected(int a, int b) {
        return find(a) == find(b);
    }
}
```

**Listing 1.** After `union(0,1)`, `union(1,2)`, `union(3,4)`: `find(0) == find(2)` is true, `find(0) == find(3)` is false — three components over six elements. The `boolean` return of `union` is the cycle test in [[What is Kruskal's algorithm]]: false means the edge is redundant.

The structure is the connectivity engine behind Kruskal's cycle veto and the keep-if-bridge logic of [[What is the reverse-delete algorithm]], dynamic connectivity in grids, and percolation simulations. Two properties to state plainly: merges are **monotone** — there is no `split`, and undoing a union is not supported (rollback needs persistence or recomputation); and the amortized bound is per operation over a sequence, not a worst case per call.

> [!warning] Union without size or rank builds linked lists
> The naive `parent[find(b)] = find(a)` can degenerate into a chain n long, and `find` becomes O(n) — the whole structure collapses to quadratic work over a run. The second classic error is using union-find when the workload needs deletions or set splitting: nothing in the forest supports un-merging. If components must shrink, the standard move is to process queries in reverse (offline) so that "deletions" become additions.

> [!tip] Interview answer
> Union-find stores each set as a parent-pointer tree; find locates the root with path compression, union attaches the smaller tree under the larger one. With both optimizations every operation is amortized O(α(n)) — constant for any practical n. It answers only connectivity: merge and query, never split. That is exactly what Kruskal's cycle test needs and what reverse-delete's bridge logic needs.
