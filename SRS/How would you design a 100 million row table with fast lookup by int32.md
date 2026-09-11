<!--
reps: 0
priority: 0
-->
#Databases/SQL #Databases/Indexes #SRS

# How would you design a 100 million row table with fast lookup by int32

> [!abstract] Short answer
> Make the int32 key the clustered primary key so point lookups are one B-tree descent into the row (InnoDB), keep the key compact and monotonic if inserts are append-heavy, add covering for the payload columns the hot query needs, and paginate by keyset predicates instead of OFFSET. Verify with plans at full volume, not with a dev subset.

## Storage and key decisions

InnoDB makes the primary key the table itself — the clustered index — so `WHERE id = ?` on an int32 PK is a single tree descent to the row; the manual's own guidance for such tables is to define the PK for the most time-critical queries, keep it short because every secondary index duplicates it, and insert in PK order for bulk loads because sequential keys leave pages about 15/16 full while random keys fragment, per [[How many clustered indexes can a table have and what is a clustered index physically]]. A monotonic int (identity, or snowflake-style if distributed generation is needed) beats random UUIDs for insert locality — the reasoning detailed in [[Should you use UUID as a primary key in PostgreSQL]]. In PostgreSQL the same lookup is a unique B-tree plus a heap hop, which makes covering design more valuable there: the payload columns of the hot query go into INCLUDE so the answer comes from the index alone, per [[How would you explain Covering index]].

```sql
-- InnoDB-oriented shape
CREATE TABLE events_100m
(
    id    INT UNSIGNED NOT NULL,
    kind  TINYINT NOT NULL,
    payload VARBINARY(256) NOT NULL,
    PRIMARY KEY (id)
) ENGINE=InnoDB;

-- hot lookup served without a second hop (PostgreSQL flavor)
CREATE INDEX idx_events_id_covering ON events_100m (id) INCLUDE (kind);
```

**Listing 1.** Compact monotonic key as the cluster; covering for the hot projection.

## Access patterns that keep it fast at 10^8

Point lookups by the key are trivial; the design work is in everything else. Secondary access paths get purpose-built composites, not one index per column, per [[How do you decide which database indexes to create]]; each added index multiplies write amplification at 100M-row scale, the budget in [[When are database indexes a bad idea]]. Range scans and pagination must ride the key order: keyset predicates (id > last ORDER BY id LIMIT n) stay O(page) while OFFSET 9999990 reads a million rows to discard them, per [[What is keyset pagination]]. Aggregations over the whole table are a different workload — that is OLAP territory, per [[When should you use OLTP versus OLAP]]-style reasoning, and columnar storage rather than more B-trees. Finally, verify at production volume with EXPLAIN ANALYZE, because cardinality-driven plan flips only show up at scale, per [[How do you read EXPLAIN ANALYZE in PostgreSQL]].

> [!warning] "Just add an index on the int column" answers the wrong question
> At 10^8 rows the interesting risks are: random keys fragmenting the clustered layout, secondary indexes duplicating a wide PK everywhere, OFFSET pagination quietly degrading with page depth, and statistics that no longer represent the data, per [[How do stale statistics hurt a query plan]]. A single extra index solves none of these; key design, covering, and access-pattern discipline do.

> [!tip] Interview answer
> I make the int32 the clustered primary key — one B-tree descent per lookup in InnoDB — keep it monotonic for insert locality and short because secondary indexes duplicate it, and cover the hot query's payload with INCLUDE where the engine supports it. Secondary paths get few purpose-built composites, pagination rides keyset predicates, and I verify plans at full volume. Aggregation-heavy needs would push me to a columnar store instead of more B-trees.
