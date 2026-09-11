<!--
reps: 0
priority: 0
-->
#Databases/Indexes #SRS

# How many clustered indexes can a table have and what is a clustered index physically

> [!abstract] Short answer
> Exactly one. A clustered index defines the physical order of the stored rows themselves, and a set of rows can be physically sorted only one way, so engines allow at most one clustered index per table. Physically it is the table's data organized as the leaf level of a B-tree keyed by the cluster key.

## Why the number is one by construction

SQL Server's documentation states it directly: clustered indexes sort and store the data rows by their key values, the data rows can be stored in only one order, and a table with no clustered index is a heap. InnoDB is even more literal: each InnoDB table has a special index called the clustered index that stores the row data. It uses the PRIMARY KEY as the clustered index; without one it takes the first UNIQUE NOT NULL index; and if neither exists it builds a hidden clustered index `GEN_CLUST_INDEX` over a synthetic 6-byte monotonically increasing row ID. The number of secondary indexes is unbounded, which is why this question is about the single physical arrangement, not about a licensing limit.

```sql
-- InnoDB: this table IS a B-tree keyed by (customer_id, order_id)
CREATE TABLE orders (
    order_id    BIGINT       NOT NULL,
    customer_id BIGINT       NOT NULL,
    total       DECIMAL(9,2),
    PRIMARY KEY (customer_id, order_id)
) ENGINE=InnoDB;
```

**Listing 1.** The primary key becomes the clustered index, so rows for one customer sit adjacent in the file, which also helps range reads by customer.

## Consequences you should mention

Because the leaf holds full rows, secondary indexes pay twice: their entries carry the clustered key, and a lookup through them is two structures deep, which is why InnoDB's manual advises short primary keys. Inserts into random cluster keys cause page splits and fragmentation, while monotonic keys append cheaply; the same physical-order reasoning explains the value of [[What is a column-store index and when would you use one]] for analytics, where no row order can serve every predicate. PostgreSQL is the counterexample worth naming: its heap tables are never physically clustered by an index, and `CLUSTER` is a one-shot rewrite command rather than a maintained property, as [[What is the difference between clustered and non clustered database indexes]] details.

> [!warning] "Primary key = clustered index" is a vendor default, not a law
> The claim is true for InnoDB and the SQL Server default (a PRIMARY KEY constraint creates the clustered index unless one already exists), but SQL Server can enforce the PK with a nonclustered index on a heap, and PostgreSQL does not cluster storage at all. Answer per engine, not as a universal rule.

> [!tip] Interview answer
> One clustered index per table, because it defines the physical order of the data and rows can only be stored in one order. Physically, the leaf level of that B-tree is the table itself: InnoDB stores rows in the primary-key B-tree and synthesizes a hidden row-ID clustered index when no key exists, SQL Server stores the table in the clustered index or as a heap, and every secondary index then points into that one arrangement.
