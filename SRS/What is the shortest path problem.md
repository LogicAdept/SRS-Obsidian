<!--
reps: 0
priority: 0
-->
#DSA/Algorithms/Graph/ShortestPath #DSA/Problems #SRS

# What is the shortest path problem

> [!abstract] Short answer
> Given a graph whose edges carry weights, find a path between two vertices with the minimum total weight. The three standard variants: **single-source** (distances from one start to all vertices), **single-pair** (one target), and **all-pairs**. Shortest paths are well defined while no **negative-weight cycle** is reachable — around such a cycle a path can get cheaper forever.

## One problem, one algorithm family

The right algorithm is dictated by the edge weights, not by taste. Unweighted edges — BFS gives fewest-edge paths in O(V + E). Non-negative weights — Dijkstra, O((V + E) log V). Negative edges allowed — Bellman-Ford, O(V · E), which also detects negative cycles. All pairs at once — Floyd-Warshall, O(V³), or Johnson's algorithm on sparse graphs. A DAG — relax edges in topological order and even negative weights cost only O(V + E).

```java
// 0 -> 1 (4), 0 -> 2 (1), 2 -> 1 (2), 1 -> 3 (1), 2 -> 3 (5)
```

**Listing 1.** A tiny weighted digraph: the cheapest 0 to 3 path is `0-2-1-3` with cost 1 + 2 + 1 = 4 — not the direct-looking `0-2-3` (6) and not `0-1-3` (5). Cheapest is about total weight, not about looking direct.

Weights model anything additive: latency, price, distance, fuel. Negative weights are legitimate (cashback on an edge, energy gain), and only cycles that sum below zero break the problem itself. On a DAG even negative weights are easy because no cycle can exist. The workhorses: [[What is Dijkstra's algorithm]] for non-negative weights, [[What is the Bellman-Ford algorithm]] when edges may be negative, [[What is the Floyd-Warshall algorithm]] for all-pairs, and plain [[What is breadth-first search]] when every edge costs one hop.

> [!warning] "Shortest path = fewest edges" is only true when edges are unweighted
> With weights, a two-hop path can cost 100 while a five-hop path costs 3. The second classic conflation: a negative **edge** is fine and just makes paths cheaper, but a negative **cycle** reachable from the source means "the shortest path" does not exist — any answer can be improved by one more lap. Algorithms differ precisely in what they do about this: Dijkstra assumes away the case, Bellman-Ford reports it.

> [!tip] Interview answer
> Shortest path asks for a minimum-total-weight path, in single-source, single-pair, or all-pairs form. I pick the algorithm by weights: BFS for unweighted, Dijkstra for non-negative, Bellman-Ford when negative edges or cycle detection are in play, Floyd-Warshall or Johnson for all pairs, topological relaxation on DAGs. Negative reachable cycles make the problem undefined, not "harder".
