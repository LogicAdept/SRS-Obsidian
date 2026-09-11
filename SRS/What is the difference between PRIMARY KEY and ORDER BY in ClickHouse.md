<!--
reps: 0
priority: 0
-->
#Databases/OLAP/ClickHouse #Databases/Indexes #SRS

# What is the difference between PRIMARY KEY and ORDER BY in ClickHouse?

> [!abstract] Short answer
> In MergeTree, `ORDER BY` is the sorting key: it defines the physical order of rows inside every part and is mandatory (use `ORDER BY tuple()` to opt out). `PRIMARY KEY` is the index key: the set of columns whose granule-start marks live in `primary.idx`. If you omit `PRIMARY KEY`, ClickHouse reuses the sorting key; if you specify it, it must be a prefix of the sorting key.

## Two roles, one default

Because rows are sorted by `ORDER BY`, a mark at a granule start for the full sort tuple guarantees ranges are contiguous — the index and the layout coincide, which is the common case. Splitting them lets you index a shorter prefix while still sorting by more columns: `ORDER BY (CounterID, EventDate, UserID) PRIMARY KEY (CounterID, EventDate)` indexes the two equality-ish columns while keeping rows additionally ordered by `UserID` inside each `(CounterID, EventDate)` range. This is unlike PostgreSQL, where `PRIMARY KEY` is a uniqueness constraint backed by its own secondary index and `ORDER BY` in a query is just result ordering — see [[What is the difference between PostgreSQL and ClickHouse]] for the semantic clash.

```sql
-- typical: index = sort key (PRIMARY KEY omitted)
CREATE TABLE h1 (CounterID UInt32, EventDate Date, UserID UInt64)
ENGINE = MergeTree ORDER BY (CounterID, EventDate, UserID);

-- shorter index than sort order
CREATE TABLE h2 (CounterID UInt32, EventDate Date, UserID UInt64)
ENGINE = MergeTree
ORDER BY (CounterID, EventDate, UserID)
PRIMARY KEY (CounterID, EventDate);

-- no ordering at all (append-only raw log)
CREATE TABLE raw (payload String) ENGINE = MergeTree ORDER BY tuple();
```

**Listing 1.** The three configurations of index versus sort key in MergeTree DDL.

```d2
orderby: "ORDER BY\nsorting key\nphysical row order per part" {
  width: 300
  height: 100
  style.fill: "#e3f2fd"
}
pk: "PRIMARY KEY\nindex key\nmarks in primary.idx" {
  width: 280
  height: 100
  style.fill: "#e8f5e9"
}
same: "Default: identical\nindex == sort key" {
  width: 260
  height: 80
  style.fill: "#fff3e0"
}
prefix: "Explicit: prefix subset\nindex shorter than sort" {
  width: 300
  height: 90
  style.fill: "#fff3e0"
}
orderby -> same
pk -> same
orderby -> prefix
pk -> prefix
```

**Fig. 1.** `PRIMARY KEY` defaults to the sorting key and may only narrow it to a prefix — never reorder or extend it.

> [!warning] PRIMARY KEY in ClickHouse does not enforce uniqueness
> Unlike PostgreSQL, nothing stops duplicate key values — deduplication only happens at merge time in `ReplacingMergeTree` ([[What is ReplacingMergeTree]]), visible via `FINAL`. Interviewers love this: a "primary key" here is purely a data-layout optimization, not a constraint; uniqueness must be enforced upstream or checked with queries.

> [!tip] Interview answer
> `ORDER BY` is mandatory and controls the physical sort of rows in each part; `PRIMARY KEY` controls which columns get index marks and defaults to the sort key, possibly shortened to a prefix. It is a layout-and-index knob, not a uniqueness constraint — duplicates are allowed and only cleaned by ReplacingMergeTree merges.
