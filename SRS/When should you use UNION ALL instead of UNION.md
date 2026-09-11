<!--
reps: 0
priority: 0
-->
#Databases/SQL #SRS

# When should you use UNION ALL instead of UNION?

> [!abstract] Short answer
> Prefer `UNION ALL` whenever duplicate removal is **not required** (or duplicates are impossible): it skips the sort-or-hash dedup stage that `UNION` runs over the whole combined result. Use plain `UNION` only when the answer's correctness depends on distinctness — counting distinct values, merging overlapping sources, or de-duplicating rows that legitimately collide. PostgreSQL's reference says it directly: "UNION ALL is usually significantly quicker than UNION; use ALL when you can."

The cost gap is structural, not a tuning matter. `UNION ALL` streams operand rows straight into the result; `UNION` must buffer the combined set and compare every row against everything seen — an `O(n log n)` sort or an `O(n)` hash that also inflates memory/temp-file use ([[How would you explain limitations of the SQL UNION operator]]). At scale the dedup stage is often the plan's dominant node, and the optimizer cannot drop it because semantics demand it.

Decision rule with three steps: (1) can the operands produce overlapping rows? If provably not (disjoint key ranges, disjoint dates), duplicates cannot occur — `UNION ALL`. (2) Do you *want* duplicates removed as part of the answer? Then `UNION` is the honest one-step statement. (3) Are duplicates possible but harmless, or will you dedup later anyway (e.g. `GROUP BY` over the merged rows)? Take `UNION ALL` and let the next step handle it — deduping twice pays twice.

```sql
-- 2,000 generated rows folded into 100 distinct values, duplicated into `big`.
CREATE TABLE big (v INTEGER);
WITH RECURSIVE c(x) AS (SELECT 1 UNION ALL SELECT x+1 FROM c WHERE x < 2000)
INSERT INTO big SELECT x % 100 FROM c;

SELECT (SELECT COUNT(*) FROM (SELECT v FROM big UNION SELECT v FROM big)) AS union_rows,
       (SELECT COUNT(*) FROM (SELECT v FROM big UNION ALL SELECT v FROM big)) AS union_all_rows;
-- 100|4000
```

**Listing 1.** Verified on SQLite 3.53.1. Same two operands: `UNION` collapses 4,000 rows to 100 distinct values; `UNION ALL` returns all 4,000. The ALL variant does no row comparison at all — on large inputs this is the difference between a streaming step and a full dedup stage ([[Why is SELECT DISTINCT expensive]]).

```d2
direction: right
need: "Can duplicates occur?\nAre they wanted?" {width: 220; height: 100}
no_dups: "No (disjoint sources)\nor harmless" {width: 200; height: 90}
want_dedup: "Yes, distinctness is\npart of the answer" {width: 210; height: 90}
uall: "UNION ALL\nstream, no comparison" {width: 210; height: 90}
u: "UNION\nsort-or-hash dedup" {width: 190; height: 90}
need -> no_dups -> uall
need -> want_dedup -> u
```

**Fig. 1.** The default should be `UNION ALL`; promote to `UNION` only when distinctness is a correctness requirement of the answer itself.

> [!warning] `UNION ALL` changes results, not just speed — replacing one with the other is a correctness edit
> Swapping `UNION` for `UNION ALL` "to speed it up" silently duplicates rows wherever operands overlap; swapping back can hide real duplicates someone relies on. Review the sources for overlap before touching the operator, and remember `DISTINCT` later is the same cost you tried to skip ([[Why is SELECT DISTINCT expensive]]).

> [!tip] Interview answer
> I default to UNION ALL and reach for UNION only when the query's correctness needs distinct rows, because ALL streams while UNION must sort or hash the entire combined set to compare every row. If sources are provably disjoint, or a later GROUP BY handles the duplicates anyway, UNION ALL wins outright. And I would never swap the two purely for speed without checking whether overlapping operands make it a result-changing edit.
