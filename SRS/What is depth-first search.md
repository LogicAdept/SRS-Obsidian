<!--
reps: 0
priority: 0
-->
#DSA/Algorithms/Search #DSA/DataStructures/Graph #SRS

# What is depth-first search

> [!abstract] Short answer
> **Depth-First Search (DFS)** traverses a graph or tree by going as deep as possible along one branch, then **backtracking** and continuing to other unvisited vertices. It uses a **stack** — explicit, or implicit via recursion — and runs in **O(V + E)** time with adjacency lists and **O(V)** space for visited flags and the stack.

## How the traversal runs

From the current vertex, move to the first unvisited neighbor; if there are none, go back to the previous vertex and try its next neighbor. The moment a vertex is *finished* (all descendants explored) is the signal many algorithms build on: finishing order reversed gives a topological sort of a DAG, an edge to an already-started (gray) vertex signals a cycle, and one full sweep of the visited array decomposes a graph into connected components.

```java
static void dfs(List<List<Integer>> g, int v, boolean[] visited) {
    visited[v] = true;
    for (int to : g.get(v)) {
        if (!visited[to]) {
            dfs(g, to, visited);
        }
    }
    // v is finished here — append to a list for topological order
}
```

**Listing 1.** Recursive DFS: the `visited` array is what terminates recursion; the post-visit position is where topo-sort and cycle logic hook in.

## Complexity and where it is used

Every vertex is visited once and every edge examined a bounded number of times (twice for undirected adjacency lists), so the cost is **O(V + E)**; the stack depth and visited flags are **O(V)**. Standard uses: topological sort on a DAG, cycle detection, connected components, and any problem where the structure of one root-to-leaf path matters (path existence, backtracking searches). The frontier twin is [[What is BFS DFS]] — same cost, but a queue instead of a stack, which changes what "first visit" means.

> [!warning] Visited flags are not optional, and neither is the depth
> Without a visited set, any cycle in the graph sends DFS into an infinite loop. And the recursive form commits the whole path to the **call stack** — on a long path graph (say 100 000 vertices in a chain) Java will throw `StackOverflowError` before the traversal finishes; the iterative explicit-stack form is the fix, and the call-stack cost lives in [[How do the stack and heap differ for multithreading in Java]].

> [!tip] Interview answer
> DFS dives as deep as possible, then backtracks, using a stack — recursive or explicit — and costs O(V + E) time and O(V) space. First visits explore; finishing order is the useful output: reversed finishing order is a topological sort, an edge into a vertex still on the stack means a cycle, and sweeping visited flags yields components. I always mention the visited set as mandatory and the recursion-depth trap on large graphs.
