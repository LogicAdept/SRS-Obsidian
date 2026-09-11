<!--
reps: 0
priority: 0
-->
#Databases/Indexes #SRS

# What is the difference between clustered and non clustered database indexes

> [!abstract] Short answer
> A clustered index stores the table's rows themselves in key order, so there can be only one per table. A nonclustered (secondary) index is a separate structure holding keys plus locators back to the rows, so a table can have many. The difference is what lives at the leaf: data, or pointers to data.

## Mechanism per major engine

InnoDB makes the equivalence exact: the clustered index is the table, keyed by the PRIMARY KEY (or a hidden row ID), and every secondary index entry stores the indexed columns plus the primary key columns, then uses that key to search the clustered index for the row. SQL Server words it as structure: a clustered table stores data rows in the clustered index; a nonclustered index holds key values and a row locator, which is a physical pointer on a heap or the clustered key on a clustered table. PostgreSQL has no clustered storage at all: tables are heaps, every index is secondary with heap TIDs, and `CLUSTER tbl USING idx` is a one-time physical rewrite that later DML gradually un-sorts. Oracle expresses the clustered idea as index-organized tables.

```sql
-- InnoDB: lookup through a secondary index is two hops
SELECT total FROM orders WHERE order_number = 'A-1024';
-- 1) B-tree seek on idx_order_number -> finds primary key order_id
-- 2) clustered index seek by order_id -> fetches the row
```

**Listing 1.** The secondary-to-clustered hop is why InnoDB wants short primary keys: every secondary entry duplicates them.

## What follows for queries and design

A clustered index serves range scans over its key brilliantly because rows are contiguous, which is why InnoDB recommends defining the PK for your most time-critical queries and inserting in PK order for bulk loads. Nonclustered indexes win when you need several access paths on one table, and they can become covering, answering from the index alone; in PostgreSQL every index is in that category by construction, and the covering variant with `INCLUDE` is described in [[How would you explain Covering index]]. Cost asymmetry matters too: many secondary indexes tax every write, and random cluster keys fragment the clustered structure, a trade-off that [[When are database indexes a bad idea]] explores from the write side.

> [!warning] Mixing up "clustered index" and "cluster command" or "cluster of servers"
> The trap is conflating three senses of the word: the clustered index (physical row order), PostgreSQL's one-shot `CLUSTER` command (a rewrite, not a maintained index), and database clustering (multiple servers). In an index question, only the first is meant; naming the second and third shows you know the term is overloaded.

> [!tip] Interview answer
> Clustered means the index leaf is the row storage, ordered by the key, so one per table: InnoDB's table is its primary-key B-tree, SQL Server stores rows in the clustered index or a heap. Nonclustered indexes are separate key-plus-locator structures, many per table, and in InnoDB they carry the primary key to hop back to the row. PostgreSQL is all heaps and secondary indexes, with CLUSTER as an optional one-shot reorder.
