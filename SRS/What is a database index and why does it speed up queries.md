<!--
reps: 0
priority: 0
-->
#Databases/Indexes #SRS

# What is a database index and why does it speed up queries

> [!abstract] Short answer
> An index is an auxiliary on-disk structure that maps key values to the rows holding them, so the engine can find matching rows without reading the whole table. It speeds up reads at the price of extra storage and slower writes, because every INSERT, DELETE, and relevant UPDATE must also maintain the index.

## What the structure actually is

Every major engine stores an index as a set of key entries plus a locator to the row. In a PostgreSQL B-tree the leaf entry holds the key values and a heap tuple identifier (TID); SQL Server's nonclustered index holds key values plus a row locator, which is either a physical RID on a heap or the clustered key on a clustered table. InnoDB goes further: the clustered index is the table itself, and each secondary index entry stores the indexed columns plus the primary key columns, which it uses to reach the row. The common idea is the same: the keys are sorted (in B-trees) or hashed, so a lookup follows a bounded path instead of checking every row.

## Without an index versus with one

A table with no usable index is read by a full scan: every row is examined, which is linear in the number of rows. With a B-tree, a lookup descends a shallow tree whose depth grows logarithmically with row count; SQLite's planner docs give the canonical framing that a rowid or index lookup costs proportional to log N versus N for a scan. That is why an equality lookup that would read millions of rows reads a handful of index pages plus one row instead. The same ordered structure serves range predicates and ordered output, which is why [[What is the difference between an index seek and an index scan]] matters when you read plans.

```sql
CREATE INDEX idx_orders_customer ON orders (customer_id);
SELECT * FROM orders WHERE customer_id = 42;
```

**Listing 1.** A single-column B-tree turns the lookup by `customer_id` into a tree descent instead of a scan.

## What you pay for it

The bill shows up in three places. Space: each index is a full copy of its key columns plus locators, and in InnoDB every secondary index also duplicates the primary key, which is why the manual warns against long primary keys. Write cost: the engine must insert or delete entries in every affected index, so bulk-load and OLTP insert rates drop as index count grows. Planning cost: the optimizer uses statistics over these structures, and stale numbers produce bad plans, which is the failure mode in [[How do stale statistics hurt a query plan]]. These trade-offs are exactly why [[When are database indexes a bad idea]] has real answers rather than a shrug.

> [!warning] An index is not a free cache
> The classic lie is "add an index, it can only help". A wide multi-column index on a hot insert path can cost more than the queries it saves, and unused indexes still pay write tax. Verify usage with the engine's own tools before treating an index as a win.

> [!tip] Interview answer
> An index is a separate key-to-row structure, usually a B-tree, that lets the engine locate rows by key in logarithmic time instead of scanning the table. It speeds up reads, but it duplicates data, must be maintained on every write, and its usefulness depends on selectivity and the actual query patterns. Good indexing is a trade-off: measure queries, index the selective access paths, and drop what the workload never uses.
