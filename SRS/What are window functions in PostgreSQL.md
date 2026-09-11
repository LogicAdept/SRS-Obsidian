<!--
reps: 0
priority: 0
-->
#Databases/Relational/PostgreSQL #Databases/SQL #SRS

# What are window functions in PostgreSQL?

> [!abstract] Short answer
> Window functions compute a value across a set of related rows — a "window" defined by OVER (PARTITION BY ... ORDER BY ... frame) — without collapsing those rows the way GROUP BY does. Ranking (row_number, rank, dense_rank), offsets (lag, lead), and aggregates over sliding frames (sum over rows between ...) all work per partition while every input row stays in the output.

## The anatomy

```sql
SELECT customer_id, created_at, total,
       row_number() OVER (PARTITION BY customer_id
                          ORDER BY created_at)              AS nth,
       sum(total)    OVER (PARTITION BY customer_id)        AS customer_total,
       lag(created_at) OVER (PARTITION BY customer_id
                             ORDER BY created_at)           AS prev_order
FROM orders;
```

**Listing 1.** Three windows over one scan: sequence per customer, group total attached to each row, and the previous order's date.

- PARTITION BY splits rows into independent groups.
- ORDER BY inside OVER orders each partition (and enables frames and offsets).
- The frame (RANGE/ROWS/GROUPS between ...) controls which rows an aggregate sees — the difference between running totals and whole-partition totals.

```d2
grp: "GROUP BY\ncollapse: one row per group" {width: 300; height: 80}
win: "Window\nevery row stays,\ngroup context attached" {width: 300; height: 80}
use1: "Top-N per group\nrow_number() = 1..N" {width: 280; height: 70}
use2: "Deltas and totals\nlag, lead, running sums" {width: 300; height: 70}
grp vs win: "contrast"
win -> use1
win -> use2
```

**Fig. 1.** The defining contrast with GROUP BY: no row reduction.

## Rules worth knowing

- Window functions may appear only in the SELECT list and ORDER BY of a query — they run after WHERE, GROUP BY and HAVING, so filters on window results need a subquery or CTE ([[What is CTE materialization in PostgreSQL]] for wrapping).
- Aggregate functions can be used as window functions (`sum(...) OVER (...)`); non-aggregate ranks and offsets are window-only.
- Frames default to RANGE UNBOUNDED PRECEDING..CURRENT ROW with ORDER BY, which surprises people expecting per-row sums — the "running total" default is actually cumulative.
- PostgreSQL also supports explicit frame exclusion and window named definitions via the WINDOW clause ([[How does GROUP BY handle NULL in SQL]] stays a GROUP BY-level concern).

> [!warning] A window function cannot appear in WHERE
> WHERE runs before windows exist; filtering `row_number() = 1` inline is an error. Wrap it: subquery or CTE, filter outside. The second common lie is that windows are slow — an index that feeds the PARTITION/ORDER order often lets PostgreSQL stream the computation without a sort ([[How do you avoid a sort with an index]]).

> [!tip] Interview answer
> Window functions compute over a partition of rows while keeping every row in the output: rank and row_number for top-N per group, lag and lead for deltas, aggregates over explicit frames for running totals. They are evaluated after WHERE, so filtering their result needs a wrapped subquery — and unlike GROUP BY they never collapse rows.
