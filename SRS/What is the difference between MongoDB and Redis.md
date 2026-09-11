<!--
reps: 0
priority: 0
-->
#Databases/NoSQL/MongoDB #Databases/NoSQL/Redis #SRS

# What is the difference between MongoDB and Redis

> [!abstract] Short answer
> **MongoDB is a persistent document store: JSON-like documents in collections, queried by field, with secondary indexes and schema validation. Redis is an in-memory data-structure server: typed values (hashes, lists, sets, sorted sets, streams) behind keys, optimized for single-digit-millisecond operations, with optional persistence.** One is where records live; the other is where hot state moves fast.

## The axes that separate them

**Data model.** MongoDB: documents (nested objects/arrays) inside collections — the unit is a record whose shape can be validated (validators with $jsonSchema) and indexed on inner fields. Redis: named *data structures* — the value behind a key is a string, hash, list, set, sorted set, stream, etc., and the command set is per-type; there is no query language, only key access plus structure-specific operations (ZPOPMIN, XRANGE). **Memory and persistence.** Redis keeps the working set in RAM (with RDB snapshots and AOF logs for durability — datasets must largely fit in memory); MongoDB memory-maps/caches pages and treats disk as home, so datasets exceed RAM freely at the cost of IO. **Query and indexing.** MongoDB: field predicates, ranges, sorting, covered queries via B-tree-ish secondary indexes; Redis: O(1)/O(log N) structure operations and no secondary indexes — lookups are by key or by structure members. **Durability and transactions.** MongoDB: single-document atomicity by default, multi-document ACID transactions since 4.0, replica sets with automatic failover. Redis: single-command atomicity, MULTI/EXEC or Lua for multi-step atomicity, replication and (in managed/cluster form) failover; classic deployments accept losing the last write window depending on persistence settings.

```d2
direction: right
mongo: "MongoDB — document DB\nrecords on disk · field queries\nindexes · validation · ACID txns" {
  width: 330
  height: 110
  style.fill: "#e3f2fd"
}
redis: "Redis — structure server\nRAM-first · key access · typed ops\ncache · queues · counters" {
  width: 330
  height: 110
  style.fill: "#fff3e0"
}
mongo -> redis: "hot state & coordination\nlive here, records stay there"
```

**Fig. 1.** In a typical stack they are complements, not competitors: MongoDB as the system of record, Redis as the hot layer in front of it.

> [!warning] The answers that fail interviews: "Redis is faster" and "Redis is only a cache"
> Redis is faster *at its design point* — small, hot, key-addressable structures in RAM; a 40 GB working set changes the economics (RAM cost, persistence lag), and MongoDB answers field queries Redis cannot express at all. And Redis is a full data-structure server — streams back event pipelines, sorted sets back leaderboards and rate limiters — not merely a cache front. The correct comparison names the workload per store, per the category map in [[What categories of NoSQL databases exist]].

Related drills: [[How do NoSQL databases scale compared with SQL databases]] for the scaling frame, [[How do you add constraints in a NoSQL database]] for the validation contrast between the two, and [[What is an example of a relational database and a non relational database]] for the family-level pair.

> [!tip] Interview answer
> MongoDB is a document database: JSON-like records in collections, field queries with secondary indexes, optional schema validation, ACID transactions — the system of record. Redis is an in-memory data-structure server: typed structures behind keys, per-structure commands, sub-millisecond ops, persistence as snapshot/AOF — the hot layer for caching, queues, counters, leaderboards. They complement each other rather than compete.
