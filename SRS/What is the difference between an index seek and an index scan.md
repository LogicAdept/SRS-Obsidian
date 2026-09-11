<!--
reps: 0
priority: 0
-->
#Databases/Indexes #SRS

# What is the difference between an index seek and an index scan

> [!abstract] Short answer
> A seek positions directly into the index's sorted structure at the start of the matching key range — a descent from root to leaf that touches only the relevant pages. A scan reads index pages sequentially: the whole index, or a contiguous range, because no seek point could be derived. Seeks answer selective predicates; scans are what remains when the predicate, statistics, or volume say reading everything is cheaper.

## The mechanics in plan vocabulary

SQL Server names the operations directly: an index seek uses the B-tree to position at the first matching key and reads forward only while keys match (the docs' seek-and-scan terminology distinguishes the seek predicate from the residual predicate applied during the scan part); an index scan reads the index level by level. PostgreSQL's plans express the same split differently: Index Scan and Index Only Scan show a boundary condition on the index plus a filter on the heap side, while a Bitmap Index Scan batches page pointers before heap access, and a Seq Scan means no index positioning at all. The engine's ability to seek is exactly the sargability question — the predicate must bound a contiguous range of the stored keys, per [[What is sargability in SQL]], and PostgreSQL's B-tree page lists the operators and pattern shapes that qualify.

```d2
direction: right
seek: "SEEK\nroot -> leaf -> first matching key\nreads only the range" {
  width: 300
  height: 110
  style.fill: "#e8f5e9"
}
scan: "SCAN\nread index pages end to end\n(or the whole table)" {
  width: 300
  height: 110
  style.fill: "#ffebee"
}```

**Fig. 1.** Same index, two access modes: positioned descent versus sequential read. The plan tells you which one the planner bought.

## Why plans choose scans on purpose

A scan is not a failure state: when the predicate matches a large fraction of rows, or the table is small, sequential reads beat random positioning — the crossover in [[When is a full table scan cheaper than using an index]] and the selectivity math in [[What is selectivity and cardinality for indexes]]. Non-sargable shapes (functions on the column, leading wildcards, type casts on the column side) force scans even with perfect indexes, per [[Why does a function on a column prevent index use]] and [[How does implicit type conversion hide an index]]. In between sits the bitmap scan, which uses index information but reads the heap in physical order, per [[What is a bitmap index scan in SQL plans]]. The reading skill — distinguishing the index condition from the residual filter, and estimated from actual rows — is the EXPLAIN discipline in [[How do you read EXPLAIN ANALYZE in PostgreSQL]] and [[What is Index Cond versus Filter in EXPLAIN]].

> [!warning] "Seek good, scan bad" is a heuristic, not a rule
> The trap is treating scans as bugs: for a reporting query matching 30 percent of rows, a scan is the correct plan and forcing seeks via hints would be slower. The precise framing: a seek requires a boundable key range; everything else is a scan by necessity or by cost choice. Also, in SQL Server a seek can still contain a scan part — the seek positions, then reads a range; if the range is the whole level, seek versus scan distinction collapses.

> [!tip] Interview answer
> A seek positions into the B-tree at the start of the matching key range and reads only that range — possible when the predicate bounds the stored order, i.e. is sargable. A scan reads index (or table) pages sequentially, chosen when the predicate cannot bound a range, the match rate is high, or the table is small. Plans say which: seek versus scan operators in SQL Server, Index Scan versus Seq Scan and the bitmap middle ground in PostgreSQL.
