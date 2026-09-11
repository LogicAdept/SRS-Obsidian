<!--
reps: 0
priority: 0
-->
#Patterns/Architecture/Microservices/ServiceBoundaries #Databases #SRS

# How would you explain the database per service pattern

> [!abstract] Short answer
> Database-per-service means each microservice's data is private: no other service connects to its database — not even reads. Every access goes through the service's API or its events. Richardson's core data pattern for microservices; it is what makes independent schema evolution, per-service storage choice and independent scaling possible, and what forces the integration patterns (API composition, sagas, outbox) that replace free JOINs and shared transactions.

## The mechanism: ownership as an architectural invariant

The rule is structural, not a guideline: the database (or schema, or logical namespace) is part of the service's implementation, like its classes. Consequences cascade. Schema freedom: the owning service changes tables, indexes and even storage engines freely — a rename is a private refactor, not a fleet coordination event ([[What is the shared database pattern in microservices]] itemizes the taxes being avoided). Storage fit: an order service can use PostgreSQL while search uses Elasticsearch and a graph service uses Neo4j. Scaling: hot services scale their own store; the fleet's bottleneck is not one shared instance. Consistency: each service keeps local ACID inside its boundary; invariants that span services stop being transactions and become sagas with compensations, and state changes become events for others ([[What is a saga and how would you explain one with a real-world example]]; [[How does an aggregate persist and publish events without a distributed transaction]]).

```d2
direction: right
o: "Order service" {style.fill: "#e8f5e9"}
od: "orders db" {shape: cylinder; style.fill: "#fffde7"}
c: "Customer service" {style.fill: "#e8f5e9"}
cd: "customers db" {shape: cylinder; style.fill: "#fffde7"}
o -> od: owner
c -> cd: owner
o -> c: API for customer data
o -> c: events for changes
note: "No cross-connections: o cannot query cd directly" {style.fill: "#ffebee"}
```

**Fig. 1.** Data is reachable only through its owner: APIs for queries, events for change propagation.

## The costs it imposes — the integration patterns it summons

Queries spanning services lose the JOIN: answer them with API composition, event-fed read models, or data replication into query-friendly stores ([[What is the API composition pattern in microservices]]; [[What is a projection in CQRS and event sourcing]]). Transactions spanning services lose 2PC: they become sagas, and "state change plus event published" needs the outbox to stay atomic ([[How would you explain the transactional outbox pattern]]; [[What is BASE as a consistency model]] names the consistency model that results). Reporting across the whole system needs a pipeline (CDC, transaction log tailing or events) into an analytics store ([[How would you explain transaction log tailing for integration]]). These are not incidental costs — they are the actual price of the ownership boundary, and they must be designed, not discovered. One legitimate relaxation exists inside a single deployable: if two "services" are always deployed and versioned together, Richardson's guidance is that they may share a database — they are, in truth, one service not yet split.

> [!warning] "Private database" is violated most often by reporting tools
> The pattern breaks from the side door: a BI tool or a colleague's script connects straight to the schema "just for reads". The read still couples the writer — schema changes now break the analyst's queries and pressure the owner to freeze the model. Analytics is a consumer like any other: feed it a replica, a CDC stream or a warehouse — not a direct connection to the owner's store.

> [!tip] Interview answer
> Database-per-service makes data private: only the owning service touches its store, everyone else goes through its API or consumes its events. I get free schema evolution, per-service storage choice and scaling, and honest ownership. The price is real: cross-service queries need composition or read models, cross-service consistency becomes sagas with an outbox, and reporting needs a CDC pipeline. I treat direct external connections — including BI reads — as violations of the boundary.
