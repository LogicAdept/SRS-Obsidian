<!--
reps: 0
priority: 0
-->
#DSA/DataStructures/Graph #DSA/Algorithms/Search #SRS

# What is BFS and DFS

> [!abstract] Short answer
> Two systematic ways to visit every reachable vertex of a graph. **BFS** (breadth-first) expands level by level using a **queue** and therefore finds shortest paths in **unweighted** graphs. **DFS** (depth-first) dives along one branch as far as possible using a **stack** or recursion, then backtracks. Both run in **O(V + E)** time with adjacency lists and **O(V)** extra space for the visited set plus the queue/stack.

## Breadth-first search: queue and levels

BFS starts at a source, marks it visited, and repeatedly takes a vertex **from the front of the queue**, enqueueing each not-yet-visited neighbor at the back. The invariant "queue holds vertices in non-decreasing distance from the source" is what makes the first time BFS touches a vertex also the shortest unweighted distance — that is why level-order tree traversal and unweighted shortest path are the same routine; any `Deque` implementation works as the frontier, and [[Does LinkedList implement Queue and Deque in Java]] compares the two JDK candidates. Weighted graphs break the invariant: a longer-but-cheaper path can beat the one BFS finds first, and Dijkstra replaces BFS by prioritizing cost.

```java
static int[] bfs(List<List<Integer>> g, int src) {
    int n = g.size();
    int[] dist = new int[n];
    Arrays.fill(dist, -1);                 // -1 = unvisited
    Deque<Integer> q = new ArrayDeque<>();
    dist[src] = 0;
    q.add(src);
    while (!q.isEmpty()) {
        int v = q.poll();
        for (int to : g.get(v)) {
            if (dist[to] == -1) {
                dist[to] = dist[v] + 1;    // first hit = shortest
                q.add(to);
            }
        }
    }
    return dist;
}
```

**Listing 1.** BFS over an adjacency list: the distance array doubles as the visited set, and the queue (an `ArrayDeque`) produces level order.

## Depth-first search: stack and backtracking

DFS commits to one neighbor and keeps going deeper until a vertex has no unvisited neighbors, then **backtracks** to the last branching point. Implemented recursively, the **call stack** holds the path; implemented iteratively, an explicit stack does the same — the mechanics and uses of this traversal have their own card in [[What is depth-first search]]. The order DFS finishes vertices ("post-order") is the backbone of cycle detection, topological sorting on a DAG, and finding connected components.

```d2
direction: right
bfs: "BFS\nqueue · level by level\nshortest path (unweighted)" {
  width: 260
  height: 110
  style.fill: "#e3f2fd"
}
both: "O(V + E) time\nO(V) visited set" {
  width: 220
  height: 110
  style.fill: "#e8f5e9"
}
dfs: "DFS\nstack / recursion\ncycles · topo sort · components" {
  width: 260
  height: 110
  style.fill: "#fff3e0"
}
bfs -> both
dfs -> both
```

**Fig. 1.** The two traversals share the visited-set discipline and linear cost; the frontier data structure — queue vs stack — is the whole behavioral difference.

> [!warning] Weighted graphs and recursion depth
> BFS on a weighted graph does **not** give shortest paths — its "first arrival = shortest" property holds only when every edge costs the same; use Dijkstra instead. And a recursive DFS on a deep graph (a 100k-vertex path) recurses as deep as the graph is long — the pending path sits on the thread's call stack (see [[How do the stack and heap differ for multithreading in Java]]) — so in Java this is a real `StackOverflowError` risk; rewrite with an explicit stack for large inputs.

> [!tip] Interview answer
> Both traverse every reachable vertex in O(V + E) with adjacency lists. BFS uses a queue, visits in level order, and its first arrival is the shortest path — in unweighted graphs only. DFS uses a stack or recursion, goes deep and backtracks, and its finish order powers cycle detection, topological sort and components. I pick BFS for shortest unweighted distances, DFS when I need structure — ordering, cycles, components — and I remember the recursion-depth trap on big graphs.
