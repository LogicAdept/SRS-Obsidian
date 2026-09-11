<!--
reps: 0
priority: 0
-->
#Messaging/Tools/Kafka #Databases/OLAP/ClickHouse #SRS

# What is the Kafka to ClickHouse materialized view pattern?

> [!abstract] Short answer
> The canonical wiring: a Kafka engine table holds no data and acts as a consumer, and one materialized view per target subscribes to it — on every consumed block the view's SELECT runs and its result inserts into the MergeTree destination. The view is simultaneously the ETL step (casts, filtering, renaming) and the delivery mechanism ([[How do you ingest Kafka into ClickHouse]]).

## Why the view is the natural join point

```d2
direction: down
engine: "Kafka engine table\nbatches arrive" {
  width: 260
  height: 90
  style.fill: "#e3f2fd"
}
mv: "Materialized view\nSELECT with cast/filter" {
  width: 270
  height: 100
  style.fill: "#e8f5e9"
}
mt1: "MergeTree: events" {
  width: 220
  height: 80
  style.fill: "#fff3e0"
}
mv2: "Second view\nfiltered SELECT" {
  width: 240
  height: 90
  style.fill: "#f3e5f5"
}
mt2: "MergeTree: errors only" {
  width: 230
  height: 80
  style.fill: "#fff3e0"
}
engine -> mv -> mt1
engine -> mv2 -> mt2
```

**Fig. 1.** One engine table can feed several views, each fanning the same consumed blocks into a different target with its own transformation — fan-out is free because it happens at insert time.

ClickHouse materialized views are trigger-based: when rows land in the source — here, the engine table's consumed batch — the view executes and inserts the result into its `TO` table. Stacked on the Kafka engine this gives a precise, declarative ingestion contract: parsing and casting happen in the view's SELECT (treating malformed messages as strings and cleansing them, when needed), enrichment joins are possible per block, and routing by predicate sends subsets to different tables. Multiple views over one engine give topic fan-out to several targets without extra Kafka consumers; alternatively, one engine reading several topics with per-topic views filters by `_topic` — the docs recommend exactly this shape to limit consumer sprawl ([[How do you choose the number of partitions for a Kafka topic]]).

## The semantics you sign up for

The view fires per consumed block, at-least-once: a lost offset commit replays the block, so the pattern tolerates duplicates by design and leans on target-side dedup (ReplicatedMergeTree) where exactness matters ([[What are at-most-once at-least-once and exactly-once semantics in Kafka]]). It also commits you to view lifecycle discipline: changing the engine table's settings or its column mapping means dropping the view, recreating the engine table, and re-attaching the view — consumption resumes from committed offsets when the engine is recreated ([[What is Kafka Consumer position for]]). Higher delivery guarantees on the ClickHouse side come from quorum inserts, which are set on the user profile, not on the view — a detail that surprises teams hunting for a per-view setting ([[What Kafka topic settings matter in practice]]).

> [!warning] The view is not a continuously running query
> A materialized view over Kafka only sees the blocks the engine consumes while it exists; it never backfills from history, and creating it does not retroactively process anything. If you detach or drop the view, blocks consumed during that window pass by unseen except through offset rollback — treat view recreation as an operational event, not a convenience.

> [!tip] Interview answer
> The pattern: Kafka engine table as a no-storage consumer plus a trigger-based materialized view whose SELECT transforms each consumed block and inserts into a MergeTree with a TO clause. One engine can fan out to several views, transforms live in the SELECT, delivery is at-least-once so dedupe on the target, and lifecycle is strict — recreate the engine table, re-attach the view, consumption resumes from offsets.

