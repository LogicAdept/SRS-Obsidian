<!--
reps: 0
priority: 0
-->
#Patterns/Architecture/CQRS #SRS

# What is CQRS

> [!abstract] Short answer
> CQRS — Command Query Responsibility Segregation — splits a component's interface into two models: commands that change state and return nothing, and queries that return data and change nothing. Richardson's microservices.io and Fowler both present it as an architectural pattern: write side keeps the transactional domain model, read side keeps flat, query-optimized models, and the two are connected by events whenever they use separate databases.

## The core contract: separate verbs, separate models

The ground rule comes from CQS ([[What is CQS and how does it relate to CQRS]]): a method is either a command with a side effect or a query returning data — never both. CQRS scales that principle from one method to the whole architecture. The write side accepts commands ([[What is a command in CQRS]]) through command handlers ([[What is a command handler in CQRS]]), enforces invariants, and publishes domain events. The read side receives queries and answers from models shaped exactly like the answers — denormalized views built by projections ([[What is a projection in CQRS and event sourcing]]). Neither model pretends to serve the other: the write model is normalized for invariants, the read model is denormalized for speed.

```d2
direction: right
client: "Client" {style.fill: "#eceff1"}
cmd: "Command
(change state)" {style.fill: "#fff3e0"}
qry: "Query
(read state)" {style.fill: "#e3f2fd"}
write: "Write model
domain + invariants" {style.fill: "#e8f5e9"}
read: "Read models
projections" {style.fill: "#f3e5f5"}
ev: "events" {shape: cylinder; style.fill: "#fffde7"}
client -> cmd
client -> qry
cmd -> write
write -> ev
ev -> read
qry -> read
```

**Fig. 1.** One client, two paths: commands mutate the write model; queries are served from event-fed read models.

## Levels of adoption

CQRS is a spectrum, not a binary. Level 1: same database, different objects — command services and query services share one store but use different code paths and DTOs; this already removes accidental coupling. Level 2: separate schemas or databases — write DB optimized for transactions, read DB optimized for queries, synchronized by events; now the read side can use any storage (search index, document store, cache) and can scale independently. Level 3: full event sourcing on the write side, projections rebuildable from history. Richardson stresses that separate databases is where the real benefits (independent scaling, polyglot storage, query-specific views) and the real costs (eventual consistency, duplicate logic) appear.

> [!warning] CQRS is not event sourcing and not a default
> You can do CQRS without event sourcing and event sourcing without CQRS; they compose but are separate decisions ([[Which kinds of projects benefit most from CQRS]] lists where the payoff is real). Once the read model is event-fed, its data is eventually consistent — the UI must tolerate read-your-writes gaps ([[What is eventual consistency]]), and every event consumer needs idempotent handling ([[What is idempotency in HTTP and in messaging]]). Teams that adopt full CQRS for CRUD-heavy domains pay double the model count for zero benefit.

> [!tip] Interview answer
> CQRS separates the interface of a service into commands that change state and return nothing, and queries that return data and change nothing. The write side keeps a transactional domain model; the read side gets denormalized, query-shaped models fed by events — often a separate database. It pays off when reads and writes have genuinely different shapes or scaling needs (search, reporting, high read volume) and costs extra moving parts — eventual consistency, idempotent projections — so I don't apply it to plain CRUD.
