<!--
reps: 0
priority: 0
-->
#Databases/Relational #Databases/NoSQL #SRS

# What is an example of a relational database and a non relational database

> [!abstract] Short answer
> **Canonical pair: PostgreSQL (relational) versus MongoDB (non-relational, document store).** PostgreSQL keeps data as rows over a declared schema, enforces keys and constraints, and joins tables with SQL; MongoDB keeps JSON-like documents in collections, where related data can be embedded in one document and shape varies per document.

## What the example is supposed to demonstrate

The drill is recognition of the store *families* through a concrete product. **PostgreSQL, relational:** an `orders` table references a `customers` table by foreign key; order lines live in their own table and join on demand; the schema (columns, types, constraints) is declared up front and enforced on every write; multi-row ACID transactions are native; the query language is SQL. **MongoDB, non-relational:** an order is one JSON document — customer snapshot, items, totals — stored in a collection; fields can appear in some documents and not others; the DBMS validates structure only if you define schema validation rules; cross-document joins are secondary (lookups) rather than the primary access path.

A second pair reinforces the axis: **Redis** (non-relational, key-value) — data as typed values (strings, hashes, lists, sets, streams) behind keys, in-memory latency for caching, queues, and rate limiters; against **MySQL** (relational) — the classic row-store with InnoDB's ACID transactions. Same drill: where the model puts related data (a hash value vs a joined row) and what the engine guarantees around it.

```d2
direction: right
pg: "PostgreSQL — relational\nrows over declared schema\nFKs · joins · SQL · ACID" {
  width: 320
  height: 110
  style.fill: "#e3f2fd"
}
mongo: "MongoDB — document\nJSON documents in collections\nembed or lookup · flexible fields" {
  width: 320
  height: 110
  style.fill: "#fff3e0"
}
redis: "Redis — key-value\ntyped values behind keys\nin-memory latency" {
  width: 290
  height: 110
  style.fill: "#e8f5e9"
}
```

**Fig. 1.** One relational and two non-relational representatives: the differences to name are schema enforcement, where related data lives, and the primary access path.

> [!warning] "Non-relational" names the model, not a quality grade — and the gap keeps narrowing
> MongoDB added multi-document transactions and schema validation; PostgreSQL hosts JSONB documents that query like documents. Naming "MongoDB" as non-relational is correct, but the follow-up that earns points is *why*: its primary model is documents, not keyed tuples over one schema. Avoid ranking answers ("NoSQL is faster / relational is safer") — speed depends on access pattern, and safety on the guarantees you actually configure, per [[What is the difference between SQL and NoSQL data stores]].

The categorical frame: [[What database categories or types do you know]]; the scaling contrast: [[How do NoSQL databases scale compared with SQL databases]]; constraints on the non-relational side: [[How do you add constraints in a NoSQL database]].

> [!tip] Interview answer
> PostgreSQL is the standard relational example: rows over a declared schema, foreign keys and joins, SQL, native ACID. MongoDB is the standard non-relational one: JSON-like documents in collections, flexible per-document fields, related data embedded or looked up. Redis works as a second non-relational example — typed values behind in-memory keys. The contrast to articulate is schema enforcement and where related data lives.
