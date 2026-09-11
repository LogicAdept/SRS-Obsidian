<!--
reps: 0
priority: 0
-->
#Databases/RelationalAlgebra #SRS

# How would you explain transitive relations in relational algebra

> [!abstract] Short answer
> **A relation is transitive when A→B and B→C implies A→C; in database terms this shows up twice — as transitive dependencies that 3NF removes (employee → department → location) and as chains you must compute, not store: "manages" or "contains" expanded transitively with a recursive CTE.** The distinction is whether the transitive closure is a *constraint problem* or a *query problem*.

## Two faces of transitivity

**The dependency face.** If key → A and A → B for non-key columns, then key → B holds transitively — the fact B is really about A, not the key. That is exactly 3NF's target: the chain employee → department → location stores a department fact on every employee row, with the redundancy and anomalies it brings; the cure is decomposition, per [[How would you explain third normal form in relational databases]]. Interviewers use "transitive" in this sense when they say a table is "not in 3NF because of a transitive dependency".

**The traversal face.** "Is A an ancestor of B?" over a reflexive parent relation is not one join — parent chains have arbitrary depth. The relational-algebra answer is the transitive closure: repeatedly join the relation with its own result until nothing new appears. SQL implements that loop with a recursive CTE, which PostgreSQL documents as precisely the tool for transitive closure over graphs.

```sql
WITH RECURSIVE subordinates AS (
  SELECT id, manager_id FROM employees WHERE id = :boss
  UNION ALL
  SELECT e.id, e.manager_id
  FROM employees e
  JOIN subordinates s ON e.manager_id = s.id   -- one step deeper per pass
)
SELECT id FROM subordinates;
```

**Listing 1.** Transitive closure of the reflexive manager relation: the recursive term joins each discovered row back to the base table until the chain ends.

```d2
direction: right
a: "A manages B" {
  width: 170
  height: 70
  style.fill: "#e3f2fd"
}
b: "B manages C" {
  width: 170
  height: 70
  style.fill: "#fff3e0"
}
c: "A transitively\nmanages C" {
  width: 190
  height: 80
  style.fill: "#e8f5e9"
}
a -> b -> c
```

**Fig. 1.** Transitivity composes edges: two stored facts yield a third that was never stored — computing it is the recursive CTE's job.

> [!warning] Never store the closure alongside the edges
> Materializing "everyone's every ancestor" into a table duplicates every path as data: a single re-org must update thousands of closure rows, and the closure can silently disagree with the edges it came from. Store the primitive relation, derive transitivity by query (or maintain a documented, explicitly-synced materialization if the read cost is proven). Also mind the difference from the dependency face: a transitive *dependency* is something to eliminate, while transitive *reachability* is something to compute — using the word without saying which face you mean is the interview trap.

The 3NF consumer of the dependency face: [[What is normalization]] and [[How would you explain third normal form in relational databases]]; the reflexive base relation being traversed: [[How would you explain reflexive relations in relational algebra]].

> [!tip] Interview answer
> Transitivity means A→B and B→C implies A→C, and databases meet it twice. As a dependency it violates 3NF — a non-key fact about another non-key fact, fixed by decomposition. As a graph property over a self-referencing table it is the transitive closure — "all subordinates of a manager" — computed with a recursive CTE rather than stored, because materialized closures go stale on every edge update.
