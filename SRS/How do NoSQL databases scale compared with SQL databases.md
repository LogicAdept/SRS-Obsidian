<!--
reps: 0
priority: 0
-->
#Databases/NoSQL #Databases/Relational #SystemDesign/Scalability #SRS

# How do NoSQL databases scale compared with SQL databases

> [!abstract] Short answer
> Most NoSQL engines are built sharding-first: data is partitioned by key across nodes, each node serves only its partition, so capacity and throughput grow nearly linearly by adding nodes — at the cost of by-key access and weak or narrow transactions. Classic SQL scales vertically (bigger machine), then read-replicas, then sharding as an afterthought — powerful but operationally heavy, because cross-node joins and transactions are the hard part.

## The scaling paths

A relational system grows in stages. First vertical: more CPU/RAM/NVMe on one node — easy, no application change, but a ceiling and a cost curve. Second read-out: replicas offload reads ([[How would you explain database replication strategies]]) while one primary still owns writes. Third is sharding — splitting rows by key across primaries — which works ([[How would you explain horizontal database sharding]]) but moves JOINs, uniqueness and transactions across nodes, so ORMs lose guarantees and cross-shard queries fan out. NoSQL engines start at that third stage by design: Mongo partitions documents over shards ([[What is the difference between a stateful service and a stateless service]]-style statelessness makes node churn cheap), Cassandra/DynamoDB distribute a hash ring with partition keys, Redis clusters slot ranges. Because each partition is served by one node with its own local index, throughput adds up linearly — and because queries are by-partition-key, no coordinator must join anything.

```text
SQL:     vertical -> read replicas -> manual sharding (joins/txns hurt)
NoSQL:   hash/range partitions by key from day one
         each node = one partition set, local indexes only
         scale = add node, remap a slice of key space
cost:    queries must carry the partition key; no global joins
```

**Listing 1.** The two growth curves in one view.

## What the scaling model costs

Linear scale-out is bought with constraints, and knowing them is the point of the comparison. Access must be key-shaped: a query without the partition key fans out to every node (scatter-gather), so data models are designed around known queries. Transactions narrow: ACID holds within a partition or document, while cross-partition operations need 2PC or sagas ([[What is the difference between atomicity and consistency]] frames the guarantee levels; [[How does an aggregate persist and publish events without a distributed transaction]] shows the escape hatch). Consistency becomes tunable — quorum reads and writes trade freshness against latency ([[How would you explain consistency in distributed systems and data stores]]). Relational engines keep the opposite bargain: strong guarantees and arbitrary queries, with scale-out pushed to read replicas and, increasingly, built-in declarative sharding extensions. [[When should you use NoSQL and when should you use SQL]] turns this mechanics comparison into the decision.

> [!warning] Scatter-gather is the tax for forgetting the partition key
> A "find all X regardless of shard" query on a sharded engine hits every node and serializes on the slowest one. If most queries cannot name the partition key, the sharding-first engine is the wrong engine, whatever its throughput benchmarks say.

> [!tip] Interview answer
> SQL scales vertically then by replicas, and sharding is possible but heavy because joins and transactions cross nodes. NoSQL engines are sharding-native: partition by key, local indexes, near-linear node scaling — paid for by by-key access, narrow transactions and tunable consistency. So the comparison is really about which constraints your workload can live with.
