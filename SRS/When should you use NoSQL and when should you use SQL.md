<!--
reps: 0
priority: 0
-->
#Databases/NoSQL #Databases/Relational #SystemDesign/Tradeoffs #SRS

# When should you use NoSQL and when should you use SQL

> [!abstract] Short answer
> Choose SQL (relational) when data is relational, queries are ad-hoc, and multi-row transactional consistency matters — the default until a concrete reason appears. Choose NoSQL when a specific engine property beats those defaults: horizontal write scaling through sharding (wide-column stores), flexible schemas for heterogeneous documents (document stores), or specialized access patterns (key-value lookups, full-text, time series). The honest answer picks per workload, not per fashion.

## What SQL buys by default

A relational database gives you ACID transactions across any rows ([[What are the ACID properties of database transactions]]), a declarative query language with a planner (join anything with anything — [[What is a database index and why does it speed up queries]]), and constraints that keep the schema true. For the classic business system — orders, users, money, reports — this is exactly right, and decades of tooling (ORMs, BI, replication) assume it. The costs are vertical-first scaling and a schema you must migrate. That is the base case: the burden of proof is on changing away from it.

## The concrete reasons to go NoSQL

Each NoSQL family earns its place by giving up something for something. Key-value stores (Redis) give sub-millisecond lookups by giving up queries — right for sessions, caches, rate counters ([[How would you explain distributed caching and cache hierarchies at a high level]]). Document stores (MongoDB) give a flexible, aggregate-shaped schema by giving up joins — right when one document is exactly one read, wrong when entities interrelate deeply. Wide-column stores (Cassandra) give linear write scaling via sharded, replicated partitions by giving up ad-hoc queries and multi-row transactions — right for event/time-series ingestion keyed by design. Deciding factors to state out loud: access pattern known at design time? (key-value/wide-column: yes; SQL: no). Schema owned by code and heterogeneous? (document). Cross-entity transactions? (SQL). Write volume beyond one vertical node? (sharding-native engines). [[How do NoSQL databases scale compared with SQL databases]] details the scaling mechanics, [[How would you explain tradeoffs among relational document and other database types]] the data-model side, and polyglot designs often mix both — SQL as system of record, NoSQL for specialized paths.

```text
decision axis          SQL        document    key-value   wide-column
schema                 rigid      flexible    none        partition-keyed
transactions           multi-row  doc-level   single-key  partition-level
ad-hoc queries         yes        some        get/put     by-key only
write scale-out        limited    moderate    good        linear-ish
```

**Listing 1.** The engine families against the axes that actually decide the choice.

> [!warning] "We might need to scale" is not a workload
> NoSQL chosen before the access pattern is known locks you into by-key queries and app-side joins while removing transactions you still need. Pick engines for concrete requirements — measured write volume, known key access, document shape — not for a scale you have not reached.

> [!tip] Interview answer
> SQL is my default: relational integrity, ad-hoc queries, transactions. I reach for NoSQL when a specific property wins: Redis for sub-ms key-value paths, MongoDB for aggregate-shaped heterogeneous documents, Cassandra for linear write scaling on known access patterns. Polyglot mixes are normal — SQL as system of record plus specialized stores.
