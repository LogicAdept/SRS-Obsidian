<!--
reps: 0
priority: 0
-->
#Databases/Partitioning #SystemDesign/Scalability #SRS

# How does vertical partitioning differ from horizontal partitioning

> [!abstract] Short answer
> Vertical partitioning splits a table by columns — wide rows are divided so hot, small fields live apart from heavy or rarely used ones. Horizontal partitioning splits by rows — each partition holds the same columns for a disjoint key range (by date, id, region). Vertical aims at read width and access-path separation; horizontal aims at data volume, retention and parallelism across ranges.

## The mechanics of each

Horizontal partitioning (range, list or hash — PostgreSQL's declarative syntax offers all three) divides rows so each partition is a nearly independent table with its own index: a query with a date predicate prunes to the matching partitions and scans far less, old partitions can be detached or archived wholesale, and maintenance (vacuum, index rebuild) hits one partition instead of the whole table. PostgreSQL documents this as the core motivation — partition pruning and bulk retention operations. Vertical partitioning divides columns: a users table whose profile blob, avatar bytes or audit history move to a side table referenced by the same key; the hot table's rows shrink, so more rows fit per page and index scans touch fewer bytes. In the extreme, column stores (ClickHouse) take vertical separation to its logical end, and blob-heavy fields move out of the row entirely. [[How would you explain table or index partitioning in databases]] surveys the general partitioning toolkit, and [[How would you explain horizontal database sharding]] is the next step — when horizontal partitions also move to different servers, it becomes sharding.

```text
table orders(order_id, ts, user_id, total, payload_json)

horizontal: orders_2026_01 (rows by month), orders_2026_02, ...
            -> pruning by ts, archive old months, per-partition indexes
vertical:   orders_core(order_id, ts, user_id, total)
            orders_payload(order_id, payload_json)
            -> hot pages stay narrow; payload fetched only when needed
```

**Listing 1.** The same table split both ways, with what each buys.

## Choosing between them

The split follows the workload's dominant pain. If the pain is volume over time — retention, pruning, per-period maintenance, ever-growing indexes — horizontal partitioning is the tool, and the partition key is almost always time or a monotonically growing id. If the pain is row width — queries that fetch a few columns but pay for wide rows, hot columns hostage to cold blobs — vertical partitioning helps without touching query semantics much (the join back is explicit but rare). They compose: a table can be vertically split once (core vs payload) and then horizontally partitioned by date. What vertical partitioning does not buy is write scale-out — row-splitting across servers is what sharding adds on top. [[What is cold data and hot data]] is the temperature lens on horizontal splits; [[What problem does database sharding solve]] the scale lens.

> [!warning] A vertical split that is queried together is a join tax
> Moving columns to a side table adds a join back on every read that needs both halves. Partition vertically only when access patterns genuinely differ — otherwise you pay a join to save bytes nobody needed saving.

> [!tip] Interview answer
> Vertical partitioning splits columns — hot narrow fields apart from heavy payload — to shrink rows and separate access paths. Horizontal partitioning splits rows by key range, list or hash, so queries prune partitions and old data can be archived or distributed; pushed across servers it becomes sharding. The choice follows the pain: row width versus data volume.
