<!--
reps: 0
priority: 0
-->
#DSA/Algorithms/Search #DSA/DataStructures/Graph #SRS

# What is breadth-first search

> [!abstract] Short answer
> A graph traversal that explores level by level: first the start vertex, then everything one edge away, then two edges away, and so on. It uses a **queue** (FIFO), runs in **O(V + E)** time and space, and on an **unweighted** graph the first time it reaches a vertex is automatically via a fewest-edges path.

## The queue, the seen set, and the levels

BFS keeps a queue of vertices to expand and a `seen` set. The discipline that matters: a vertex is marked seen **when it is enqueued**, not when it is dequeued — that is what guarantees every vertex enters the queue at most once. The queue then holds at most two adjacent levels of the graph at any moment, which is why the traversal order is exactly non-decreasing distance from the start.

```java
static List<Integer> bfs(Map<Integer, List<Integer>> g, int start) {
    List<Integer> order = new ArrayList<>();
    boolean[] seen = new boolean[g.size()];
    Queue<Integer> queue = new ArrayDeque<>();
    seen[start] = true;
    queue.add(start);
    while (!queue.isEmpty()) {
        int v = queue.poll();
        order.add(v);
        for (int next : g.get(v)) {
            if (!seen[next]) {
                seen[next] = true;      // mark on enqueue, not on dequeue
                queue.add(next);
            }
        }
    }
    return order;
}
```

**Listing 1.** BFS over an adjacency list; on the six-vertex graph `0:[1,2], 1:[0,3], 2:[0,3,4], 3:[1,2,5], 4:[2,5], 5:[3,4]` it returns `[0, 1, 2, 3, 4, 5]` — strictly level by level.

Each level of the traversal is the frontier: all vertices at exactly distance `k`. Recording `dist[next] = dist[v] + 1` at enqueue time turns the same loop into single-source shortest paths for unweighted graphs. With weighted edges, BFS's level structure no longer matches cheapest cost — that problem needs [[What is Dijkstra's algorithm]], and the general problem family is [[What is the shortest path problem]]. The stack-driven counterpart is [[What is depth-first search]], which goes deep instead of wide.

> [!warning] Marking on dequeue instead of enqueue
> If vertices are marked seen only when dequeued, the same vertex can be enqueued many times before it is processed — the queue can accumulate up to one entry per edge instead of per vertex, and on dense or grid graphs this is the classic slowdown behind "my BFS is quadratic". A second trap: reusing BFS on a graph with cycles without a seen set at all — it never terminates.

> [!tip] Interview answer
> Breadth-first search expands the frontier level by level using a FIFO queue and a seen set marked at enqueue time, so every vertex is processed once in O(V + E). Because levels equal hop distance, it finds shortest paths by edge count on unweighted graphs. For weighted graphs I switch to Dijkstra; for memory-bounded deep searches, to depth-first or depth-limited search.
