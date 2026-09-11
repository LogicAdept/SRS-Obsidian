<!--
reps: 0
priority: 0
-->
#Databases/Indexes #SystemDesign/Tradeoffs #SRS

# When are database indexes a bad idea

> [!abstract] Short answer
> When the write cost exceeds the read value: tiny tables where scans are already instant, write-heavy paths with rarely-used indexes, low-selectivity predicates that never get chosen, columns that update constantly (each update maintaining the index and, in PostgreSQL, blocking HOT updates), and speculative indexes nothing queries — all measurable, all fixable by dropping them.

## The write-side bill, concretely

Every index on a table is a structure updated inside the same DML: each INSERT adds an entry per index, each DELETE marks or removes entries, and each UPDATE touches every index containing a modified column. Bulk loads are the sharpest case — loading millions of rows into a table with a dozen indexes rebuilds a dozen structures — which is why ETL practice loads into unindexed or minimally indexed tables and builds indexes after. In InnoDB the tax compounds through the clustered model: every secondary index entry carries the primary key, so wide PKs multiply across all indexes, per [[Is a primary key implemented as an index and why]]. PostgreSQL adds a specific mechanism: an update of any indexed column prevents the HOT (heap-only tuple) optimization, forcing new index entries per update — the reason hot, frequently updated columns are poor index candidates.

```sql
-- measure before keeping
SELECT indexrelname, idx_scan, pg_size_pretty(pg_relation_size(indexrelid))
FROM pg_stat_user_indexes
WHERE relname = 'events' ORDER BY idx_scan;
-- candidates: idx_scan = 0 on a write-heavy table -> drop
```

**Listing 1.** The audit that turns "bad idea" from opinion into data: scans counted against write volume and size.

## The read-side losers that never get chosen

Some indexes are bad ideas on the read side alone: an index on a tiny table (the scan is cheaper than any tree walk, per [[When is a full table scan cheaper than using an index]]), a standalone index on a low-selectivity column whose predicates match large fractions, per [[Does it make sense to index low-cardinality columns]], and indexes whose predicates never occur in the workload — speculation from the scattergun style in [[What goes wrong with indexing every field combination for flexible search]]. The engineering answer is the decision workflow of [[How do you decide which database indexes to create]] plus the audit loop of [[How do you find unused indexes in PostgreSQL]], with MySQL offering invisible indexes (drop the planner's access while keeping the structure) as a rehearsal before deletion, and the whole budget question framed by [[What is selectivity and cardinality for indexes]].

> [!warning] "Indexes never hurt reads" and "just drop all indexes to speed up writes" are both half-truths
> Indexes can hurt reads indirectly: planner overhead grows, cache fills with index pages, and misleading statistics over many similar indexes produce worse plans. But mass-dropping indexes to save writes ignores that the surviving queries then scan — the right move is measuring which indexes earn their scans and dropping only those that do not. The second nuance: uniqueness constraints are indexes with a correctness job; their write cost is not optional and not a tuning candidate.

> [!tip] Interview answer
> Indexes are a bad idea when the write bill beats the read value: tiny tables, write-heavy paths with unqueried indexes, low-selectivity single-column indexes, and hot updated columns that block HOT updates in PostgreSQL. I make it measurable — idx_scan against write volume, index size, bulk-load impact — and drop what does not earn it, keeping uniqueness constraints out of the conversation since those are correctness, not tuning.
