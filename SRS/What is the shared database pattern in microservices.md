<!--
reps: 0
priority: 0
-->
#Patterns/Architecture/Microservices #Databases #SRS

# What is the shared database pattern in microservices

> [!abstract] Short answer
> The shared database pattern — several microservices reading and writing one database — is the anti-pattern counterpart of database-per-service. It maximizes coupling: schema changes ripple to every service, one database is a scaling and failure bottleneck, and ACID transactions across the shared tables tempt services into logic they should not own. Richardson catalogs it because real systems drift into it and someone must name the cost.

## Why it exists: the shortcuts it offers are real

The pattern survives because it solves the problems microservices create — cheaply and dangerously. Cross-service invariants: with all tables in one database, "order total must not exceed credit limit" is one local ACID transaction ([[What is a saga and how would you explain one with a real-world example]] is what replacing it costs). Cross-service queries: a JOIN replaces API composition entirely. Zero new infrastructure. For a system being extracted from a monolith, the shared database is even a legitimate way-station — the point is to treat it as debt, not a destination.

```d2
direction: right
s1: "Order service" {style.fill: "#e8f5e9"}
s2: "Customer service" {style.fill: "#e8f5e9"}
s3: "Reporting service" {style.fill: "#e8f5e9"}
db: "Shared database
ORDERS, CUSTOMERS, CREDIT" {shape: cylinder; style.fill: "#ef9a9a"}
s1 -> db: own + foreign tables
s2 -> db: own + foreign tables
s3 -> db: reads everything
```

**Fig. 1.** Three services, one database: every service's schema change is every service's problem.

## The coupling taxes, itemized

Schema coupling: the Order service's column rename breaks the Customer service's query — a deploy-time coordination problem that defeats independent releases. Runtime coupling: all services contend for the same connections, locks and capacity; one service's unindexed scan degrades every other's latency, and the database becomes the scaling ceiling for the whole system. Logic coupling: business invariants end up enforced by whichever service touches the tables, so ownership of rules blurs — the definition of a distributed big ball of mud. Testing and blast radius couple too: a schema migration must be rehearsed against every consumer. The escape path is database-per-service plus the integration patterns that replace the free JOINs and transactions: APIs and events for access ([[How would you explain the database per service pattern]]), API composition or read models for queries ([[What is the API composition pattern in microservices]]), sagas and outbox for cross-service state changes ([[How would you explain the transactional outbox pattern]]). The ownership rule this pattern violates is aggregate-level ownership - [[How do aggregates shape data ownership between services]].

> [!tip] Interview answer
> Shared database means several services read and write one schema. It buys cheap cross-service transactions and joins, at the cost of everything microservices are for: schema changes break all consumers, the database is a scaling and failure bottleneck, and business logic leaks into whoever touches the tables. I treat it as a migration way-station — extract data ownership per service, then replace free JOINs with APIs, events and read models.
