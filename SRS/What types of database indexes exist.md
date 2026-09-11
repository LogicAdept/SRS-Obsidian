<!--
reps: 0
priority: 0
-->
#Databases/Indexes #SRS

# What types of database indexes exist

> [!abstract] Short answer
> The common families are: ordered tree indexes (B-tree and its variants), hash indexes for pure equality, inverted or full-text indexes for token search, bitmap indexes for low-cardinality analytics, columnar indexes for OLAP aggregation, and special-purpose trees like GiST, SP-GiST, and BRIN for geometric, partitioned, or range-correlated data. Each engine packages these differently.

## Ordered trees: the default

B-tree is the default in PostgreSQL, MySQL, SQL Server, and Oracle because it handles equality and ranges on sortable data and returns ordered results. The sub-flavors differ in what is stored at the leaf: a clustered index stores the row itself (InnoDB's primary index, SQL Server clustered index, Oracle index-organized tables), while a secondary or nonclustered index stores a locator. This split is the subject of [[What is the difference between clustered and non clustered database indexes]]. Hash indexes store a hash of the key and answer only equality: PostgreSQL hash indexes support only the `=` operator, and InnoDB exposes the same idea as an automatic Adaptive Hash Index over hot B-tree pages rather than a user-managed structure.

## Inverted, bitmap, and columnar

GIN in PostgreSQL, the text index in ClickHouse, and FULLTEXT in MySQL are inverted indexes: they map each token or component value to the rows containing it, which is what makes `WHERE doc @@ query` or `MATCH ... AGAINST` fast. Bitmap indexes (Oracle's native type, or the bitmap scan over B-trees in PostgreSQL) represent which rows match each key value as bit vectors and combine them with AND/OR; they shine on low-cardinality analytical read-mostly data. Columnstore indexes (SQL Server) or column-oriented MergeTree storage (ClickHouse) invert the physical layout itself, compressing each column in rowgroups, which is why [[What is a column-store index and when would you use one]] is an analytics question, not an OLTP one.

## Specialized trees

PostgreSQL also ships GiST (an infrastructure for geometric and range types, plus nearest-neighbor queries), SP-GiST (partitioned trees like quadtrees and radix trees), and BRIN, which stores per-block-range min/max summaries and is tiny but only helps when values correlate with physical order. ClickHouse replaces the per-row index idea with a sparse primary index over granules plus data-skipping indexes; that design lives in [[What is a sparse primary index in ClickHouse]] and [[What data skipping indexes exist in ClickHouse]]. LSM-trees with SSTables are the write-optimized counterpart used by storage engines such as RocksDB, described in [[What are SSTables and LSM trees]].

```sql
CREATE INDEX idx_btree  ON events USING btree  (user_id);
CREATE INDEX idx_hash   ON events USING hash   (session_token);
CREATE INDEX idx_gin    ON events USING gin    (tags);
CREATE INDEX idx_brin   ON events USING brin   (created_at);
```

**Listing 1.** PostgreSQL's index type menu, selected with `USING`. B-tree is the default; the others solve specific predicate shapes.

> [!warning] "Which index is fastest?" is unanswerable without the predicate
> The trap is claiming one type wins in general. Hash beats B-tree only for equality and cannot serve ranges at all; GIN is superb for containment but heavier to maintain; BRIN is megabytes where B-tree is gigabytes but useless on shuffled data. The type must match the operators and data layout, which is the whole point of [[What is sargability in SQL]].

> [!tip] Interview answer
> Name the families by what predicate they serve: B-tree for equality, ranges, and sorting; hash for equality only; inverted indexes like GIN or FULLTEXT for tokens and containment; bitmap for low-cardinality analytics; columnstore for aggregation-heavy OLAP; and specialized trees like GiST, SP-GiST, and BRIN for geometry and physically-correlated data. Then say the engine matters: InnoDB makes the table the clustered index, while ClickHouse uses a sparse index plus skip indexes.
