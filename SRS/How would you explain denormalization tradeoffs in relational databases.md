<!--
reps: 0
priority: 0
-->
#Databases/Relational #SystemDesign/Tradeoffs #SystemDesign/Performance #SRS

# How would you explain denormalization tradeoffs in relational databases

> [!abstract] Short answer
> In a relational database, denormalization trades the normal-form guarantees for read performance: you accept redundancy, wider rows and heavier writes in exchange for fewer JOINs, simpler hot queries and precomputed aggregates. The tradeoff is favorable when reads dominate and the duplicated data changes rarely; it turns negative when update frequency, consistency requirements, or storage costs of the copies rise.

## What you give up and what you get

Normalization exists to make every write update one fact in one place; denormalization deliberately breaks that so reads touch one place. The gains are concrete: queries drop JOINs (fewer nested-loop or hash-join plans to go wrong), read-only copies can be indexed in query-shaped ways the normalized core cannot support, and aggregates stop being recomputed per request. The costs are symmetric: every write now touches several rows (or fires triggers / CDC updates), storage grows with the redundancy, and the schema must document which copy is authoritative. Consistency becomes the central risk — two copies of the same fact can diverge unless updates are transactional or eventually consistent by design. That is why the decision belongs with measurements: a slow JOIN that fires millions of times a day justifies the copies; a report run once a night does not. [[What is database denormalization for]] gives the motivation and mechanics; [[What is eventual consistency]] covers the async-update case; [[What are the ACID properties of database transactions]] anchors what the relational side is protecting.

```text
write path:  UPDATE orders            -> row + agg row + trigger/CDC
             cost: 1 fact write becomes N copy updates
read path:   SELECT name, total FROM orders_agg
             cost: 1 indexed lookup, no JOIN, no GROUP BY
risk:        copies diverge unless all writers follow one rule
```

**Listing 1.** The tradeoff ledger: N-way writes and a coherence rule bought for a one-lookup read.

## When the trade is worth it

Favorable cases share a shape: read-heavy workloads (catalogs, leaderboards, dashboards), aggregates that are expensive to recompute, and read models whose shape differs from the normalized core — the query side of CQRS is exactly a managed denormalization. Unfavorable cases: highly mutable attributes copied widely (every write fans out), strict read-after-write consistency that async copies cannot meet, and storage-bound tables where redundancy doubles cost. Partial strategies soften the trade: index-only covering duplicates a few columns inside the index ([[How would you explain Covering index]]-style read without full row copies), materialized views refresh on schedule rather than per write, and separate read replicas carry denormalized copies only on the read path. [[When should you use NoSQL and when should you use SQL]] extends the same logic across engines: many "NoSQL wins" are really denormalization wins.

> [!warning] The copy, not the table, is the liability
> Denormalized data fails quietly: the main row is right, a copy is stale, and reports disagree. Every copy needs an owner (trigger, transaction, pipeline) and a reconciliation check, or the redundancy will outlive the memory of why it existed.

> [!tip] Interview answer
> Denormalization buys read speed with redundancy: fewer JOINs and precomputed aggregates, paid as heavier writes, more storage and divergence risk. It is the right trade for read-heavy, slowly changing data with measured hot queries — and the wrong one when copies mutate often or freshness is a hard requirement.
