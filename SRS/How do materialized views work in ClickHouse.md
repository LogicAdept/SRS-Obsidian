<!--
reps: 0
priority: 0
-->
#Databases/OLAP/ClickHouse #SRS

# How do materialized views work in ClickHouse?

> [!abstract] Short answer
> A ClickHouse materialized view is a trigger on INSERT: every inserted block runs the view's SELECT, and the result is written into a target table. Incremental state rows are then merged in the target — which is why targets use AggregatingMergeTree/SummingMergeTree engines and `-State` combinators — shifting computation from query time to insert time.

## The trigger model

Unlike PostgreSQL's stored materialized views, nothing is computed at CREATE time (without POPULATE) and nothing refreshes on a schedule by default: `CREATE MATERIALIZED VIEW mv TO target AS SELECT ...` attaches to the source table, and each subsequent INSERT block flows through the SELECT into the target. The target is a normal table you query directly — typically with an `AggregatingMergeTree` engine so partial aggregation states (`uniqState(x)`, `sumState(y)`) from successive blocks merge into running results you read with their `-Merge` combinators. The Null engine can replace a physical source when raw data should not be stored at all — the view becomes a pure router/transformer.

```sql
CREATE TABLE votes (... Id UInt32, CreationDate Date ...) ENGINE = MergeTree ORDER BY Id;

CREATE TABLE votes_per_day
(
    day Date,
    votes AggregateFunction(count)
)
ENGINE = AggregatingMergeTree ORDER BY day;

CREATE MATERIALIZED VIEW mv_votes_per_day TO votes_per_day AS
SELECT CreationDate AS day, countState() AS votes
FROM votes GROUP BY day;

-- read side:
SELECT day, countMerge(votes) FROM votes_per_day GROUP BY day;
```

**Listing 1.** Insert-time aggregation with partial states, and the `-Merge` read — the pattern from [[What is the Kafka to ClickHouse materialized view pattern]].

## Pitfalls and the refreshable variant

Because the trigger sees only new blocks, a JOIN inside the view reads the *right-hand* table as of insert time — new rows inserted into the joined table later never re-trigger old aggregates; the same class of surprise applies to `POPULATE` (backfilling while data still arrives loses concurrent inserts) — safe usage either backfills from a static source or recreates the view. For workloads that genuinely want periodic recomputation, refreshable materialized views re-run their query on a schedule (with APPEND or atomic REPLACE semantics) — trading real-time freshness for simplicity over batch sources like data lakes. Choosing between an MV pipeline and part-level [[What are projections in ClickHouse]] is then an operational decision: MVs are visible tables and can join/fan out, projections are automatic but table-local.

> [!warning] The MV does not watch the tables it reads — only the one it is attached to
> A classic bug: the view's SELECT joins a lookup table, and months later someone updates the lookup and "the aggregates are stale". By design, only inserts into the attached source trigger the view. State this explicitly in design reviews — it is the single most common misunderstanding of ClickHouse MVs in interviews and production alike.

> [!tip] Interview answer
> ClickHouse MVs are insert-time triggers: each inserted block is transformed by the SELECT and lands in a target table, usually an AggregatingMergeTree holding partial states that background merges fold. Reads hit the target with -Merge combinators. They shift cost from query to insert time, but only watch their source table — joins read right-side snapshots, and refreshable MVs exist for scheduled full recomputation.
