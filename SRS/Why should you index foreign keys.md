<!--
reps: 0
priority: 0
-->
#Databases/Indexes #SRS

# Why should you index foreign keys

> [!abstract] Short answer
> Because the database must find child rows by parent key in three hot paths: queries that filter or join on the FK column, cascaded ON DELETE/UPDATE actions that scan the child table per parent row, and lock probes that take locks on matching children. Without an index on the child column each of these becomes a child-table scan.

## The three workloads that break without it

Lookups and joins first: `WHERE order_id = ?` on a child table or a join from parent to child is exactly the seek-into-index case, and without the index every such query scans the child. Cascades second: when a parent row is deleted, the engine must locate every referencing child row to delete or nullify them; with `ON DELETE CASCADE` this happens per parent row inside the delete statement, so an un-indexed FK turns a parent cleanup into a full child scan each time — the cost compounds with the FK behaviors in [[What is foreign key cascading in a relational database]]. Locking third: locks on parent rows can require the engine to examine matching child rows for certain foreign-key checks; PostgreSQL's docs on foreign keys note that adding an index on the referencing column is a good idea for performance of cascaded deletes and shared-lock probes, while being explicit that the referencing-column index is not created automatically.

```sql
-- PostgreSQL does NOT auto-index the referencing side
CREATE TABLE orders (
    id          BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    customer_id BIGINT NOT NULL REFERENCES customers(id)
);
CREATE INDEX idx_orders_customer ON orders (customer_id);
```

**Listing 1.** The referencing column's index must be added by hand in PostgreSQL; the docs recommend it for cascade and lookup performance.

## Engine differences worth naming

MySQL's InnoDB automatically creates an index on the referencing column if one does not exist, because its FK implementation requires one — so the "forgot to index FK" bug is a PostgreSQL-classic. SQLite likewise does not require it but documents that the child key index is strongly recommended for performance when deleting or updating parent rows. Oracle and SQL Server also leave the decision to you. This asymmetry is a favorite interview probe because it looks like trivia but predicts real production incidents: deletes that hang, locks piling up, and plans switching to hash joins over full scans, as in [[What is the difference between Nested Loop Hash Join and Merge Join]].

> [!warning] "The FK constraint creates an index" — not everywhere
> The claim is true for InnoDB and false for PostgreSQL, SQLite, Oracle, and SQL Server. The related myth is that indexing the FK fixes referential enforcement performance generally; the index serves lookups, cascades, and lock probes, while constraint validation cost on bulk loads is a separate matter. Check `pg_stat_user_indexes` or MySQL's index list before assuming the index exists.

> [!tip] Interview answer
> Index the FK column because three paths scan the child without it: queries and joins filtering by parent key, cascaded deletes and updates that must find every referencing row, and lock probes against children. PostgreSQL does not create this index automatically, so it is a manual step; InnoDB creates one for you. Missing it usually shows up as slow parent deletes and join plan degradation.
