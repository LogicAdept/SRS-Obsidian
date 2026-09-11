<!--
reps: 0
priority: 0
-->
#Databases/Indexes #Databases/OLAP #SRS

# What is a column-store index and when would you use one

> [!abstract] Short answer
> A columnstore index stores table data column by column instead of row by row: each column's values in a rowgroup are compressed together and carry metadata that lets the engine skip segments during scans. You use it for analytical scans and aggregations over large tables, where you typically touch a few columns of billions of rows, and not for row-level OLTP lookups.

## How SQL Server's columnstore is built

Microsoft's docs define the columnstore as column-wise physical storage, the standard for large data-warehousing fact tables, with up to an order of magnitude better query performance and compression versus row storage. A rowgroup is a batch of rows compressed together, normally the maximum 1,048,576 rows; each rowgroup holds one column segment per column, and segment metadata enables segment elimination without reading them. Incoming rows go to a deltastore, a B-tree staging area, until a delta rowgroup fills and a background tuple-mover compresses it; since SQL Server 2019 a background merge also handles small or trimmed rowgroups. Deletions are tracked rather than applied, which is why long update-heavy workloads degrade columnstore quality.

```sql
CREATE CLUSTERED COLUMNSTORE INDEX cci_fact
    ON dbo.fact_sales;
-- or a nonclustered columnstore index for analytics on an OLTP table
CREATE NONCLUSTERED COLUMNSTORE INDEX ncci_fact
    ON dbo.fact_sales (customer_id, product_id, amount, sale_date);
```

**Listing 1.** Since SQL Server 2016 SP1 a table can be operational (rowstore) and still offer real-time analytics through a nonclustered columnstore index.

## When it is the right answer and when it is not

Use it when queries aggregate or filter over many rows but few columns: per-segment compression makes scans of `SUM(amount) GROUP BY day` dramatically cheaper, and the column layout compresses repetitions far better than rows. Avoid it for point lookups, wide-row fetches, or update-heavy OLTP, where the rowstore B-tree wins; a heap or clustered rowstore stays the OLTP base. The same storage idea powers ClickHouse's MergeTree at larger scale, so this card pairs with [[When should you use OLTP versus OLAP]]-style questions about workload shape and with the columnar-native design in [[What is a sparse primary index in ClickHouse]].

> [!warning] "Columnstore is just another index type" hides the storage inversion
> The trap is treating it as a B-tree variant. It changes the physical layout of the data, its delete model (bitmaps, deltastore, tuple-mover), and its update profile. Listing a columnstore index as a fix for a slow OLTP point lookup is a category error: that is a job for a rowstore B-tree, as in [[What is the difference between an index seek and an index scan]].

> [!tip] Interview answer
> A columnstore index stores each column's values in compressed segments per rowgroup of about a million rows, with deltastore staging for writes. Segment metadata lets scans skip reading columns and rowgroups that cannot match. It is the standard for data-warehouse fact tables, giving large compression and scan speedups on aggregations, while rowstore stays the choice for point lookups and heavy updates.
