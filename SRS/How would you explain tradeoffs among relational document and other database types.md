<!--
reps: 0
priority: 0
-->
#Databases/Relational #Databases/NoSQL #SystemDesign/Tradeoffs #SRS

# How would you explain tradeoffs among relational document and other database types

> [!abstract] Short answer
> The tradeoff axis is data model versus guarantees versus access shape: relational rows give normalization, joins and strong transactions; document stores give aggregate-shaped, schema-flexible records with doc-level atomicity and no joins; key-value gives raw speed for get/put; wide-column gives write-throughput at partition scale; graph gives relationship traversal. The choice is which shape matches your reads, writes and consistency needs — not a ranking.

## Relational versus document

A relational database models every entity as a row in a normalized table and every relationship as a join ([[What is a database index and why does it speed up queries]] covers the read mechanics): maximal integrity, ad-hoc queries, multi-row ACID. A document store (MongoDB) models one aggregate as one JSON-like document: an order with its lines is a single unit read and written atomically, fields can vary per document, and the shape follows the application object — which removes impedance mismatch for aggregate-shaped domains. The tradeoffs mirror that: document reads are one fetch (no joins), but "join-like" questions across documents move to the application, duplicates creep in across documents, and cross-document transactions are recent or limited; relational joins cost at read time but keep every fact in one place. Schema is the second axis: relational enforces centrally via migrations, documents push schema into the writer's discipline — flexible and dangerous at once. [[When should you use NoSQL and when should you use SQL]] frames this as the decision; [[How do NoSQL databases scale compared with SQL databases]] the scaling side.

## The other families in one glance

Key-value stores (Redis) collapse everything to opaque get/put — fastest possible, no queries. Wide-column stores (Cassandra, Bigtable-style) store rows partitioned by key with sparse column families — designed for massive write throughput over known key access, weak elsewhere. Graph databases store first-class edges — traversal queries (friends-of-friends) that would be recursive joins elsewhere. Full-text engines (Elasticsearch) invert content into term indexes — search-shaped reads. Time-series engines specialize in timestamp-partitioned ingestion with TTL retention. [[What is BASE as a consistency model]] adds the guarantee axis that often decides within these families: many of them trade strict consistency for availability and latency, which the relational family refuses by default.

```text
family        strength                  you give up
relational    joins, ACID, ad-hoc SQL   horizontal write scale
document      aggregate reads, schema   cross-doc joins/transactions
key-value     sub-ms get/put            anything but key access
wide-column   write scale-out           ad-hoc queries
graph         relationship traversal    bulk-scan throughput
```

**Listing 1.** The family tradeoffs on one line each.

> [!warning] The join does not disappear — it moves
> A document model that embeds references duplicates data the relational schema would have joined at read time. The work is still done, now by application code maintaining copies. Count that cost, not just the missing JOIN clause.

> [!tip] Interview answer
> Relational trades read-time joins for integrity and ad-hoc queries; document trades cross-record joins for aggregate-shaped atomic reads and flexible schema; key-value trades everything for speed; wide-column trades queries for write scale; graph trades scans for traversal. I pick by matching read/write shape and consistency needs, and the join never vanishes — it just changes place.
