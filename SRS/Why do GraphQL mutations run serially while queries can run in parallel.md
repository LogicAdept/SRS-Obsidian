<!--
reps: 0
priority: 0
-->
#API/GraphQL #SRS

> [!abstract] Short answer
> Because mutations have side effects and queries (usually) do not. The spec says root mutation fields "must be executed serially, in the order they appear in the document", so clients can rely on `createX` finishing before `notifyX` starts — without that rule, two side-effecting fields in one operation could interleave arbitrarily across threads. Query root fields are "expected to run in parallel" since independent reads race harmlessly. The distinction applies to **root fields only**; nested field execution follows the same rules for both.

## What serial actually guarantees — and what it does not

The guarantee: for one mutation operation, root field resolvers start and complete in document order (for async resolvers, the engine awaits each before starting the next). The demo output shows the contract directly: two aliased root fields produced `RUN createPost ...` then `RUN deletePost ...`, never interleaved ([[What is the difference between a GraphQL query a mutation and a subscription]]).

```java
// graphql-java 26.1:
// mutation M($in: PostInput!) { c: createPost(input: $in) { id title } d: deletePost(id: "p1") }
// console:
// RUN createPost title=Hello tags=[api]
// RUN deletePost id=p1
// {"data":{"c":{"id":"p42","title":"Hello"},"d":true}}
```

**Listing 1.** Verified on graphql-java 26.1: document order held even though neither resolver shares state with the other — the engine, not the programmer, enforces ordering.

```d2
direction: down
Q1: "query: fieldA" { width: 200; height: 55 }
Q2: "query: fieldB" { width: 200; height: 55 }
M1: "mutation: createX" { width: 220; height: 55 }
M2: "mutation: notifyX" { width: 220; height: 55 }
Par: "may run in parallel" { shape: oval; width: 210; height: 50 }
Ser: "strict sequence" { shape: oval; width: 180; height: 50 }
Q1 -> Par
Q2 -> Par
M1 -> Ser
M2 -> Ser
```

**Fig. 1.** Same grammar, different root execution: reads may race, writes are chained in document order.

> [!warning] Serial is not atomic, not isolated, and stops at the root
> The three standard over-reads. First: **no transaction** — if `createX` succeeds and `notifyX` fails, the mutation returns partial data plus errors; multi-step consistency needs the backend, not the GraphQL engine ([[What does the GraphQL errors array contain]]). Second: **no cross-client isolation** — another user's mutation can commit between your two root fields; "serial" scopes to this operation only ([[What are the two fundamental relational data integrity types]]). Third: **nested selections still fan out** — `createX { comments { author } }` resolves children per object and may parallelize internally; the ordering promise covers root fields, and servers may also serialize nested mutation fields but are not required to ([[How does the GraphQL execution engine resolve a query]]).

Why queries get the opposite treatment: parallel reads are the performance story of GraphQL — one request fanning out over independent resolvers — and the spec's careful wording ("expected to", a server choice) lets engines bound concurrency, pin execution to a thread pool, or serialize everything if they must ([[What is the N plus 1 problem in GraphQL]]). Batching frameworks rely on this: DataLoader collects keys **per level** — which only works because siblings genuinely run concurrently, and because mutation roots do not, per-request loaders stay safe across side-effecting operations ([[How does DataLoader batch GraphQL resolver calls]]).

Design consequence worth saying out loud: chain dependent writes **within one mutation resolver** (one root field that does both steps) rather than listing two root fields and relying on their order — the second is serialized but still two separately-failing operations with no shared transaction.

> [!tip] Interview answer
> Mutations run their root fields serially in document order because they carry side effects; queries may run theirs in parallel because independent reads do not race. The serial rule is per operation, stops at the root, and provides ordering — not atomicity, isolation, or a transaction. Nested selections of both kinds execute by the ordinary tree-walk rules. For dependent writes, put the steps in one resolver instead of trusting field order.

