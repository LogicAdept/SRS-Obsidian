<!--
reps: 0
priority: 0
-->
#Databases/Relational #Databases/OLAP #SRS

# When should you use OLTP versus OLAP

> [!abstract] Short answer
> **OLTP systems serve many short, mixed read-write transactions over individual rows — orders, payments, sessions; OLAP systems serve long analytical scans and aggregations over historical data — dashboards, funnels, cohorts.** The physical designs diverge accordingly: row-oriented storage and point-index lookups for OLTP; columnar storage, compression, and append-friendly bulk loads for OLAP.

## What each workload actually does to the engine

An OLTP request touches a handful of rows by key and must commit in milliseconds: "insert this order, decrement stock, charge the card". Row-oriented storage wins because a row's whole life lives together — point lookups, updates, and row-level locking are cheap (PostgreSQL's MVCC, InnoDB's clustered index). An OLAP query aggregates millions of rows but touches few columns: "average order value by region per month for the last year". Columnar engines (ClickHouse, Snowflake) win because each column is stored contiguously — reading one column of a billion rows reads megabytes, not the whole rows — vectorized execution uses CPU caches efficiently, and column data compresses orders of magnitude better; the cost is the mirror image: point updates and tiny inserts are pathological (ClickHouse parts and mutations prefer big append-only batches), per the engine drills in [[How do you choose ORDER BY in ClickHouse]] and [[How do you drop old data quickly in ClickHouse]].

```d2
direction: right
oltp: "OLTP — row store\nshort txns · point reads/writes\nindexes by key · ms latency" {
  width: 300
  height: 110
  style.fill: "#e8f5e9"
}
pipe: "CDC / batch ETL\n(append, don't hammer)" {
  width: 240
  height: 100
  style.fill: "#eeeeee"
}
olap: "OLAP — columnar\nscans · aggregates · compression\nbulk append · seconds per query" {
  width: 320
  height: 110
  style.fill: "#e3f2fd"
}
oltp -> pipe -> olap
```

**Fig. 1.** The standard topology: transactions run on the row store; data flows by CDC or batch ETL into a columnar warehouse, which is queried analytically without touching the OLTP source.

When to use which: anything with user-facing writes and strict per-record integrity stays OLTP — that is where ACID and row locks pay, as in the store-family comparison [[What is the difference between SQL and NoSQL data stores]]. Company-wide reporting, metrics over months, ML feature tables — OLAP; running those aggregates directly on the production OLTP database is the anti-pattern that motivated the split in the first place. Teams that keep both use the OLTP system's logical replication or change stream to feed the warehouse near-real-time, per the ingestion drill [[How do you ingest Kafka into ClickHouse]].

> [!warning] OLTP vs OLAP is a workload split, not a product endorsement — and mixing them hurts both sides
> Heavy analytics on an OLTP row store evicts its buffer cache, locks hot rows, and slows every checkout; tiny streaming inserts into a columnar store explode part counts and mutation queues. The trap in interviews is answering "PostgreSQL vs ClickHouse" with a product ranking instead of the design trade: row layout optimizes for touching one row, column layout for scanning one column. There is also a hybrid middle (HTAP-ish systems, PostgreSQL BRIN and partitioning for mild analytical loads) — name it before someone else does.

The engine-level detail for both ends: [[How does PostgreSQL declarative partitioning work]] and [[How does ClickHouse compress data]]; the data model backdrop: [[What database categories or types do you know]].

> [!tip] Interview answer
> OLTP is many short transactions over individual rows — row storage, indexes, locking, millisecond commits. OLAP is long scans and aggregations over history — columnar storage, compression, bulk appends. Production runs both: OLTP takes user writes; a CDC or ETL pipe feeds a columnar warehouse for analytics. Mixing them degrades both, so the split is an architecture decision, not a preference.
