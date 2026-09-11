<!--
reps: 0
priority: 0
-->
#Databases/OLAP/ClickHouse #SRS

# Why might a ClickHouse skip index not help

> [!abstract] Short answer
> Because skip indexes only exclude whole blocks of granules, they fail whenever the predicate cannot rule out blocks: values spread across every block (no correlation with the sorting key), the wrong index type for the predicate, too-fine GRANULARITY relative to value spread, or an index not materialized on old parts. In those cases you pay index evaluation plus the full read.

## The correlation failure is the big one

The docs' skip-index best practices walk the core example: with timestamp as the primary key and an index on visitor_id, a query for one visitor_id must test every block — if visitor_id values are uniformly spread, every block contains a few of them, every bloom/minmax answers yes, and nothing is skipped; a row-store secondary index would have pointed at five rows, the skip index skips nothing. The stated best practice is that a useful skip index requires strong correlation between the primary key and the indexed expression, or insert-time batching that groups related values into shared granules (for example, inserting one site's events together so site_id blocks are homogeneous). High-cardinality sparse values are the other good case, like rare error codes.

```d2
direction: right
corr: "Correlated with key\nblocks homogeneous -> skip" {
  width: 280
  height: 100
  style.fill: "#e8f5e9"
}
mixed: "Uncorrelated\nevery block has a match -> read all" {
  width: 290
  height: 100
  style.fill: "#ffebee"
}```

**Fig. 1.** Same index type, opposite outcomes: block homogeneity, not index existence, decides whether granules are skipped.

## The mechanical reasons a declared index does nothing

Several non-correlation failures produce the same symptom. Type mismatch: minmax never applies to array or map expressions, and set(max_size) silently becomes empty when a block exceeds the cap, per [[What data skipping indexes exist in ClickHouse]]. Not materialized: ALTER ADD INDEX affects only new parts until MATERIALIZE INDEX runs, so historical queries see nothing, per [[How do you materialize a skip index on existing ClickHouse data]]. Coarse GRANULARITY: one index block covering many granules dilutes exclusion power. Unmatched function shape: the predicate must hit the indexed expression and an index-supported function, which is why token predicates pair with the text index rather than arbitrary LIKE, per [[What is a text index in ClickHouse]]. Verification is the granule before/after counts in EXPLAIN indexes = 1 plus trace logs, per [[How do you verify a ClickHouse index is used]] — and if skipping cannot work, the redesign levers are the sorting key, projections, or materialized views, with key choice in [[How do you choose ORDER BY in ClickHouse]] and projections in [[What are projections in ClickHouse]].

> [!warning] "I added the index, SELECT is faster now" — check the counters
> The trap is attributing the speedup to the wrong thing: often the query was always fast or the primary key did the work. The opposite trap: keeping a useless skip index that taxes ingestion and every query evaluation while skipping nothing. The docs' closing advice is test, test, test on real data with variations of type, granularity, and parameters — and remember the cost model: if a value occurs even once in a block, the whole block is read.

> [!tip] Interview answer
> Skip indexes exclude granule blocks, so they fail when blocks cannot be ruled out: values uniformly spread across blocks because there is no correlation with the ORDER BY, the wrong type for the predicate shape, granularity too coarse, or the index never materialized on old parts. Then you pay evaluation plus the full read. I verify with EXPLAIN indexes = 1 granule counts and fix the root cause — key design, insert batching, or projections — not the index type.
