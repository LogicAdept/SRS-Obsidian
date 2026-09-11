<!--
reps: 0
priority: 0
-->
#Databases/Relational #Databases/NoSQL #SRS

# What is the difference between SQL and NoSQL data stores

> [!abstract] Short answer
> **"SQL" names stores built on the relational model — declared schema, keyed tuples, joins, ACID transactions, one query language. "NoSQL" names stores organized around other models — documents, key-value, wide-column, graph — that trade the relational guarantees for scale-out, flexible schema, and model-shaped access.** The honest comparison is per model and per guarantee, because the NoSQL side is a family, not a thing.

## The four axes that actually differ

**Data model.** Relational: normalized relations, identity by key, relations composed by joins. Document: nested JSON in collections, related data embedded or looked up. Key-value: opaque typed values behind keys. Wide-column: sparse row-column matrices partitioned by key. **Schema.** SQL engines enforce declared schema on every write (columns, types, constraints). Most NoSQL stores impose structure at write time only where you configure it — MongoDB's optional schema validation, Redis's per-type commands — so shape changes are code-side, not migrations. **Guarantees.** Relational engines default to full multi-row ACID; NoSQL typically guarantees atomicity per item/document and tunable consistency, with multi-item transactions as an add-on (MongoDB's), because they replicate and partition aggressively — the scaling contrast is its own drill in [[How do NoSQL databases scale compared with SQL databases]]. **Access and scaling.** SQL: one language, joins over any predicate, historically scale-up (partitioning and sharding exist but are heavier). NoSQL: access shaped by the model and partition key — get by key, range scans, document queries — designed for horizontal scale and high write throughput.

```d2
direction: right
sql: "SQL / relational\nDeclared schema · ACID · joins\nScale: up (+ sharding)" {
  width: 300
  height: 110
  style.fill: "#e3f2fd"
}
nosql: "NoSQL families\nDocument · KV · wide-column · graph\nFlexible schema · item atomicity\nScale: out (partition-key shaped)" {
  width: 340
  height: 130
  style.fill: "#fff3e0"
}
sql -> nosql: "same problems,\ndifferent trade curve"
```

**Fig. 1.** One line, one family: the relational side trades flexibility for uniform guarantees; the NoSQL side trades uniform guarantees for model-shaped performance and horizontal scale.

> [!warning] The comparison is not SQL-vs-"one NoSQL", and the border is porous
> Each NoSQL family answers a different question — Redis for latency, Cassandra for write volume, MongoDB for nested documents — so "NoSQL is better for scale" is a category error; a given store is. Meanwhile PostgreSQL does JSONB, full-text, and vectors, and MongoDB does transactions: the border is porous in both directions. The decision-worthy statement names the workload: access pattern, consistency requirement, write volume, and growth curve — then picks the model whose center of gravity matches, per [[What database categories or types do you know]] and the concrete-pair drill in [[What is an example of a relational database and a non relational database]].

Constraints discipline on the NoSQL side: [[How do you add constraints in a NoSQL database]]; the workload split: [[When should you use OLTP versus OLAP]].

> [!tip] Interview answer
> SQL stores are relational: declared schema, keyed tuples, joins, full ACID, one language. NoSQL is a family — document, key-value, wide-column, graph — with flexible schema, per-item atomicity and tunable consistency, and access plus scaling shaped by the partition key. The real decision is per workload: consistency and ad-hoc queries push relational; massive write volume, key access, or nested documents push a specific NoSQL model.
