<!--
reps: 0
priority: 0
-->
#Databases/Relational #Databases/NoSQL #Databases/OLAP #SRS

# What database categories or types do you know

> [!abstract] Short answer
> **By data model: relational, document, key-value, wide-column, graph, search, and the special-purpose vector and time-series categories; by workload: OLTP row stores versus OLAP columnar engines.** The two axes cross — ClickHouse is both "OLAP" and its own model choice — so name the axis you are sorting by.

## The model axis, with a representative each

**Relational** (PostgreSQL, MySQL, Oracle): data as keyed tuples over declared schemas, SQL, ACID transactions, joins — the default for transactional systems. **Document** (MongoDB, Couchbase): JSON-like documents with flexible fields inside collections; nested shapes without joins, schema validation instead of rigid schema. **Key-value** (Redis, DynamoDB-style): opaque values behind keys — a data-structure server in Redis's case (strings, hashes, lists, sets, streams), optimized for single-key latency. **Wide-column** (Cassandra, ScyllaDB): sparse row-column matrices partitioned across nodes, tuned for huge write volumes and key-range scans. **Graph** (Neo4j): nodes and edges as first-class citizens for relationship-heavy traversals (fraud rings, recommendations). **Search** (Elasticsearch, OpenSearch): inverted indexes over text with relevance scoring. **Vector** (pgvector, dedicated vector stores): embeddings with ANN indexes for similarity search. **Time-series** (ClickHouse's home turf, InfluxDB): append-heavy, time-partitioned, retention-driven.

The workload axis is orthogonal and often decisive: **OLTP** — many short read-write transactions over individual rows (banking, orders), the relational home ground; **OLAP** — long scans and aggregations over billions of rows, where columnar layouts and compression dominate, per [[When should you use OLTP versus OLAP]]. A warehouse is frequently a different *product* than the OLTP source, not just a bigger instance.

```d2
direction: right
model: "By data model\nrelational · document · key-value\nwide-column · graph · search · vector" {
  width: 380
  height: 110
  style.fill: "#e3f2fd"
}
work: "By workload\nOLTP row stores · OLAP columnar" {
  width: 300
  height: 110
  style.fill: "#fff3e0"
}
```

**Fig. 1.** Two orthogonal classifications; a product answers both at once (MongoDB: document model, OLTP-ish workload; ClickHouse: columnar model, OLAP workload).

> [!warning] Categories describe engines' centers of gravity, not fences
> PostgreSQL hosts JSONB documents, full-text search, and vectors; Redis persists to disk; MongoDB has transactions. "Category X cannot do Y" answers lose points — the precise claim is about the design center: which model and workload the engine is *optimized* around, and what it costs to push it elsewhere (e.g. document stores joining slowly, row stores scanning analytics slowly). Cite the mechanism, not the marketing.

Where the store-family split is drilled: [[What is the difference between SQL and NoSQL data stores]] and [[What is an example of a relational database and a non relational database]]; the model behind the relational side: [[How would you explain the relational data model and Codd rules basics]].

> [!tip] Interview answer
> I sort on two axes. Model: relational, document, key-value, wide-column, graph, search, plus vector and time-series — with a representative each: PostgreSQL, MongoDB, Redis, Cassandra, Neo4j, Elasticsearch. Workload: OLTP row stores for short transactions versus OLAP columnar engines like ClickHouse for scans and aggregates. Products sit on both axes at once, so I name the axis before the category.
