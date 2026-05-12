<!--
reps: 0
priority: 0
-->
#DSA/Algorithms/Search #DSA/DataStructures/Graph #SRS #New
# What is depth-first search

**Depth-First Search (DFS)** traverses a graph or tree by going as deep as possible along one branch, then **backtracks** and continues to other unvisited vertices.

Idea: from the current vertex, move to the first unvisited neighbor; if there are none, go back. Data structure: a **stack** (explicit, or implicit via recursion and the call stack).

Complexity: **O(V + E)** time with adjacency lists; **O(V)** space for visited flags and the stack.

Uses: topological sort (on a DAG), cycle detection, connected components, tree/graph interview problems.
