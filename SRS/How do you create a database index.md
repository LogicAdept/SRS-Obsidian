<!--
reps: 0
priority: 0
-->
#Databases/Indexes #Databases/SQL/DDL #SRS

# How do you create a database index

> [!abstract] Short answer
> CREATE INDEX ON table (columns) with the engine's options: USING type and opclass in PostgreSQL, ASC/DESC and INCLUDE in covering cases, CREATE UNIQUE INDEX for uniqueness, or a UNIQUE/PK constraint which creates the index implicitly. On live systems use the non-blocking forms — CONCURRENTLY in PostgreSQL, online DDL in MySQL, ALTER TABLE ADD INDEX in ClickHouse — and know that the constraint route and the explicit route produce equivalent index objects.

## The standard forms

The base statement is uniform across engines: CREATE INDEX name ON table (column_list), with the index type selected explicitly when needed — PostgreSQL's USING hash/gin/gist/brin per [[What types of database indexes exist]], MySQL's USING BTREE/HASH. Uniqueness comes either from CREATE UNIQUE INDEX or from a UNIQUE or PRIMARY KEY constraint, which creates the index implicitly; PostgreSQL additionally allows INCLUDE payload columns for covering, per [[How would you explain Covering index]], and partial indexes take a WHERE clause, per [[What is a partial index in PostgreSQL]]. Expression indexes take a functional form with the expression in parentheses, per [[What is an expression index in PostgreSQL]]. ClickHouse differs structurally: skip indexes are attached to the table definition via ALTER TABLE ... ADD INDEX ... TYPE ... GRANULARITY N and must be materialized for existing data, per [[How do you materialize a skip index on existing ClickHouse data]].

```sql
-- PostgreSQL
CREATE INDEX idx_orders_cust ON orders (customer_id, created_at DESC);
CREATE UNIQUE INDEX idx_users_email ON users (lower(email));
CREATE INDEX CONCURRENTLY idx_big ON big_table (payload);

-- MySQL (online DDL)
ALTER TABLE orders ADD INDEX idx_orders_cust (customer_id), ALGORITHM=INPLACE, LOCK=NONE;
```

**Listing 1.** The explicit DDL route in both engines, with the non-blocking variants for production.

## Production discipline

The reason CONCURRENTLY and online DDL exist: a plain CREATE INDEX takes a lock that blocks writes for the build duration, which on large tables is an outage. PostgreSQL's CREATE INDEX CONCURRENTLY builds without blocking writes, at the cost of two table scans, extra work, and a failure mode that leaves an INVALID index to drop and retry; MySQL 8's InnoDB builds secondary indexes online with ALGORITHM=INPLACE, LOCK=NONE. Naming and idempotency are practical hygiene: pick a consistent scheme (table_columns_idx), check pg_indexes or SHOW INDEX before creating, and audit usage afterwards via pg_stat_user_indexes or sys schema views per [[How do you find unused indexes in PostgreSQL]]. The decision of what to index precedes all of this, per [[How do you decide which database indexes to create]].

> [!warning] "CREATE INDEX is instant" and "constraints and indexes are unrelated"
> On a multi-gigabyte table the plain form blocks writes for the whole build — the reason the concurrent variants exist and why their caveats (INVALID leftovers, no CONCURRENTLY inside a transaction in PostgreSQL) matter. The second half-truth: UNIQUE and PK constraints are enforced by indexes, so creating the constraint creates the index; in PostgreSQL you can also back a constraint with an existing index (ALTER TABLE ... ADD CONSTRAINT ... USING INDEX), which is the same object wearing the constraint hat.

> [!tip] Interview answer
> CREATE INDEX ON table (cols) with USING for the type, UNIQUE or a constraint for uniqueness, INCLUDE for covering, and WHERE for partial indexes — plus expression indexes when the predicate needs a transformed form. On production tables I use CONCURRENTLY in PostgreSQL or online DDL in MySQL to avoid blocking writes, and I track the result in the catalogs and usage statistics afterwards.
