<!--
reps: 0
priority: 0
-->
#Databases/NoSQL #SRS

# What categories of NoSQL databases exist

> [!abstract] Short answer
> **Four classic families — key-value, document, wide-column, graph — plus search and the newer vector/time-series specializations.** Each family exists because one access pattern was optimized to the exclusion of the relational model's generality: latency, nested shapes, write throughput, relationship traversal, relevance ranking, similarity search.

## The families with their design centers

**Key-value** (Redis, DynamoDB-style stores): opaque typed values behind keys; single-key operations; Redis is honestly a *data-structure server* — strings, hashes, lists, sets, sorted sets, streams — which makes it the latency layer for caches, counters, queues, rate limiters. **Document** (MongoDB, Couchbase): JSON-like documents whose nested shape travels with the data; reads and writes address whole documents (or paths inside them), schema is flexible per document with optional validation rules; the center of gravity is content-shaped records — product pages, user profiles, events. **Wide-column** (Cassandra, ScyllaDB, HBase): sparse row-column matrices partitioned by key across nodes; the design goal is sustained write throughput and linear horizontal scale, with queries shaped by the partition key. **Graph** (Neo4j): nodes and edges stored as first-class citizens so multi-hop traversals ("friends of friends who bought X") do not degrade into join explosions. **Search** (Elasticsearch, OpenSearch): inverted indexes over tokenized text with relevance scoring and aggregations. Newer specializations complete the map: **vector** stores (pgvector, dedicated ANN engines) for embedding similarity, **time-series** engines for append-heavy timestamped data with retention.

```d2
direction: right
kv: "Key-value — Redis\nlatency by key" {
  width: 230
  height: 80
  style.fill: "#e3f2fd"
}
doc: "Document — MongoDB\nnested content" {
  width: 230
  height: 80
  style.fill: "#fff3e0"
}
wc: "Wide-column — Cassandra\nwrite throughput" {
  width: 250
  height: 80
  style.fill: "#e8f5e9"
}
gr: "Graph — Neo4j\nmulti-hop traversal" {
  width: 230
  height: 80
  style.fill: "#ffebee"
}
se: "Search / Vector / TS\nrelevance · similarity · time" {
  width: 270
  height: 80
  style.fill: "#eeeeee"
}
```

**Fig. 1.** One family per access pattern: the category question is really "which single operation must be fast, and what shape is the data".

> [!warning] The categories are design centers, and products cross lines
> PostgreSQL covers document-shaped data (JSONB), search (full-text), and vectors (pgvector); Redis persists and Cassandra supports secondary indexes — so reciting "category X cannot do Y" is the weak answer. The strong form names the trade: what the engine optimizes for at its core, and what you pay to use it off-center (e.g. graph traversals in a relational engine are recursive CTEs and joins — correct, but not optimized). The same caveat applies to the store-family split in [[What is the difference between SQL and NoSQL data stores]].

Pairing with the concrete examples: [[What is an example of a relational database and a non relational database]]; the scaling contrast that motivates two of the families: [[How do NoSQL databases scale compared with SQL databases]]; enforcing integrity without relational keys: [[How do you add constraints in a NoSQL database]].

> [!tip] Interview answer
> Four classic NoSQL families: key-value like Redis for in-memory latency by key; document like MongoDB for nested JSON-shaped records; wide-column like Cassandra for huge write volumes and key-range scans; graph like Neo4j for multi-hop traversals. Around them: search engines with inverted indexes, and newer vector and time-series specializations. Each category is an access pattern made into an engine.
