<!--
reps: 0
priority: 0
-->
#Databases/Indexes #SRS

# What is selectivity and cardinality for indexes

> [!abstract] Short answer
> Cardinality is the count of distinct values in a column or index; selectivity is the fraction of rows a predicate matches. High cardinality and high selectivity (a small matched fraction) are what make an index valuable: the seek touches few rows, so the tree walk pays off. Low selectivity flips the math toward scans.

## Definitions that survive follow-ups

Cardinality is a property of the data: `status` with three distinct values has cardinality 3; `email` in a million-row users table has cardinality near 1 million. Selectivity is a property of a predicate against that data: `status = 'active'` on a table 90% active has selectivity 0.9 (low selectivity in the useful sense — it matches too much), while `email = 'a@b.c'` has selectivity near 1/1000000 (high selectivity). The planner's estimated row count is just row_count x selectivity summed across predicates. MySQL surfaces the concept in SHOW INDEX's Cardinality column — an estimate of unique values in the index, refreshed by ANALYZE TABLE and used by the optimizer alongside index statistics. PostgreSQL keeps n_distinct and most_common_vals per column in pg_stats, and the planner's row-estimation machinery combines them, as its row-estimation examples chapter details.

```d2
direction: right
hi: "High selectivity\n1 row per 1M" {
  width: 240
  height: 90
  style.fill: "#e8f5e9"
}
mid: "Moderate\nbitmap scan territory" {
  width: 240
  height: 90
  style.fill: "#fff3e0"
}
lo: "Low selectivity\nmatches 40% -> seq scan" {
  width: 250
  height: 90
  style.fill: "#ffebee"
}```

**Fig. 1.** The same index serves three regimes; only the high-selectivity end makes a plain index scan obviously cheaper than a scan of the table.

## Consequences for index design

The planner's crossover is the point: an index scan pays the tree walk plus one heap fetch per row, so when the predicate matches a large fraction, a sequential scan's bulk reads win — the same economics behind [[When is a full table scan cheaper than using an index]] and the bitmap middle ground in [[What is a bitmap index scan in SQL plans]]. Design follows: index columns that appear in selective predicates, prefer composite prefixes that sharpen selectivity (customer_id + date beats date alone), and consider partial indexes to exclude the low-selectivity bulk entirely, as in [[What is a partial index in PostgreSQL]]. Low-cardinality columns are not automatically worthless — they earn their keep in composites, bitmaps, or partial definitions, the nuance in [[Does it make sense to index low-cardinality columns]] — and estimates drift with the data, which is why [[How do stale statistics hurt a query plan]] pairs with this card.

> [!warning] "Low cardinality means never index it" and "unique means always index it"
> Both absolutes fail. A low-cardinality column can be the cheap leading column of a composite (where it partitions the key space) or the predicate of a partial index. A unique column's index is mandatory only as a constraint mechanism; whether the workload queries that column at all decides its value as an access path. The real rule is about predicate selectivity in the actual workload, measured in the plan, not about column statistics in isolation.

> [!tip] Interview answer
> Cardinality is the number of distinct values; selectivity is the fraction of rows a predicate matches. The planner multiplies row count by estimated selectivity to cost plans, and indexes pay off only when selectivity is high enough that seeking beats scanning. Design consequence: index selective access paths, use composites and partial indexes to sharpen or exclude, and keep statistics fresh so the estimates driving these decisions stay honest.
