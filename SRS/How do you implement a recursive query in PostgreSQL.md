<!--
reps: 0
priority: 0
-->
#Databases/Relational/PostgreSQL #Databases/SQL #SRS

# How do you implement a recursive query in PostgreSQL?

> [!abstract] Short answer
> With WITH RECURSIVE: a non-recursive seed term, UNION (or UNION ALL), then a recursive term that references the CTE's own name. PostgreSQL evaluates it iteratively — seed into a working table, then repeatedly apply the recursive term to the previous iteration's rows until it returns nothing. Typical uses: org charts, BOM explosions, graph traversal. Per-row driven lookups without recursion are the LATERAL territory ([[What is a LATERAL join in PostgreSQL]]); transitive closure — walking an unknown number of levels — is the case only the recursive CTE solves.

## The shape and the loop

```sql
WITH RECURSIVE subordinates AS (
  SELECT id, manager_id, 1 AS depth          -- seed: the top manager
  FROM employees WHERE manager_id IS NULL
  UNION ALL
  SELECT e.id, e.manager_id, s.depth + 1     -- recursive step: children of last batch
  FROM employees e
  JOIN subordinates s ON e.manager_id = s.id
)
SELECT * FROM subordinates ORDER BY depth;
```

**Listing 1.** The tree walk: each iteration joins the last batch of rows (the working table) with children; depth grows per level.

Per the documentation the evaluation is: run the non-recursive term; then repeatedly substitute the working table into the recursive term's self-reference, accumulate rows into an intermediate table, and stop when it is empty. UNION deduplicates rows at each step (and is mandatory for cycle termination on cyclic graphs); UNION ALL keeps duplicates and runs faster.

```d2
seed: "Seed term\nnon-recursive rows" {width: 250; height: 70}
work: "Working table\n= last iteration output" {width: 280; height: 70}
rec: "Recursive term\njoins base table with working" {width: 300; height: 80}
stop: "Empty result? stop" {width: 220; height: 60}
seed -> work -> rec -> stop
stop -> work: "no: new rows become\nthe working table"
```

**Fig. 1.** Iteration, not recursion: the engine loops a fixed-point computation.

## Cycles and safety

For graph data with cycles, add a path array and either use UNION (deduplicates visited states) or an explicit stop:

```sql
WITH RECURSIVE graph AS (
  SELECT src, dst, ARRAY[src, dst] AS path
  FROM edges WHERE src = 1
  UNION ALL
  SELECT g.src, e.dst, g.path || e.dst
  FROM graph g JOIN edges e ON e.src = g.dst
  WHERE e.dst <> ALL (g.path)          -- cycle guard
)
SELECT * FROM graph;
```

**Listing 2.** The path-array guard prevents infinite loops; depth or cost limits serve the same purpose on trees.

> [!warning] A recursive CTE has no automatic limit
> A cycle without a guard loops forever producing rows until the query is cancelled — WITH RECURSIVE is the rare SELECT that can hang a session. Guard with UNION deduplication, path arrays, or depth caps, and set statement_timeout when running untrusted recursive SQL ([[Why do long-running transactions hurt PostgreSQL]] — a hung recursive query also pins a snapshot).

> [!tip] Interview answer
> WITH RECURSIVE: seed term, UNION ALL, then a term referencing the CTE itself; PostgreSQL iterates it against a working table until empty. Trees need a depth counter; graphs need a path array or UNION to stop cycles — there is no built-in termination. It replaces client-side tree walking for org charts, BOMs and traversals.
