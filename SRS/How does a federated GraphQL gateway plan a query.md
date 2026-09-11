<!--
reps: 0
priority: 0
-->
#API/GraphQL #SRS

> [!abstract] Short answer
> A federated gateway receives the composed **supergraph** (built once from all subgraphs' SDL), and for each incoming query it **plans**: parse and validate against the supergraph, then compute which subgraph resolves which field — building a query plan that traverses subgraphs via `_entities` when a field's owning subgraph differs from the one that holds the entity. At runtime the router executes the plan: sequential fetch rounds where dependencies exist, parallel where they don't, joining entity representations through `@key` fields.

## The plan: from selection tree to fetch rounds

Planning inputs are static: the supergraph's field-to-subgraph ownership map plus each entity's keys. The planner walks the query's selection tree; every field belongs to exactly one subgraph (composition guarantees that), so the plan is a partition into **fetches**. Cross-subgraph edges need **join keys**: when the products subgraph returns a `Product`, and reviews extends `Product`, the router ships a representation — `{__typename: "Product", upc: "..."}` — into the reviews subgraph's `_entities` resolver; the reviews subgraph resolves its own fields from that key ([[What is the difference between GraphQL federation and schema stitching]]).

```graphql
# query: { product(upc: "1") { name reviews { body author { name } } } }
# plan (conceptually):
#   fetch 1 (products): product(upc) { name  __typename  upc }
#   fetch 2 (reviews):  _entities([{__typename:"Product", upc}]) { reviews { body  author { id } } }
#   fetch 3 (accounts): _entities([{__typename:"User", id}]) { name }
# fetches 2 and 3 depend on fetch 1's keys; fetch 3 depends on fetch 2's author id.
```

**Listing 1.** The dependency chain is data-driven: each round's inputs are the previous round's key fields — which is why planners hoist key fields (`upc`, `id`) into earlier fetches even when the client never selected them ([[What is the typename meta field in GraphQL]]).

```d2
direction: down
Q: "client query" { width: 170; height: 50 }
P: "planner: field ->\nsubgraph ownership" { width: 280; height: 65 }
F1: "round 1: products" { width: 220; height: 55 }
F2: "round 2: reviews\n(_entities by upc)" { width: 260; height: 60 }
F3: "round 3: accounts\n(_entities by author id)" { width: 270; height: 60 }
Q -> P
P -> F1
F1 -> F2: "representations"
F2 -> F3: "representations"
```

**Fig. 1.** Ownership partitions the query into fetch rounds; representations (type + key) are the join keys between rounds.

> [!warning] The gateway owns correctness-critical semantics — plan accordingly
> First: **N+1 crossed the architecture** — each `_entities` round can batch by key, but per-entity fan-out across subgraphs is the federation-flavored N+1; routers batch representations, and subgraphs must handle them with batched loaders ([[What is the N plus 1 problem in GraphQL]]). Second: **errors and partial results compound** — a failed subgraph fetch nulls paths per nullability and surfaces in the envelope with subgraph-derived entries; clients see the gateway's merged view, and non-null discipline across subgraphs matters more than in monoliths ([[What does the GraphQL errors array contain]]). Third: **planning is caching-friendly but composition-sensitive** — plans are computed per query shape and cached; a new subgraph deployment that changes ownership or keys requires recomposition and router reload, and an invalid composition fails closed at build time ([[How do you version a GraphQL schema]]). Fourth: the router is on the hot path of every request — its timeout, retry, and circuit-breaking policy per subgraph is real SRE surface ([[Why is rate limiting harder in GraphQL than REST]]).

Java angle: Spring for GraphQL ships federation subgraph support (entity resolvers via `@SchemaMapping` plus `@BatchMapping` for `_entities`), while the router role is typically an Apollo Router/GraphQL Java gateway deployment — the split mirrors ownership: subgraphs stay plain Spring services ([[How would you explain Spring for GraphQL]]).

> [!tip] Interview answer
> The gateway validates against the composed supergraph, then plans: it partitions the query by which subgraph owns each field, emits fetch rounds, and joins entities across rounds by representations — typename plus key fields — fed to `_entities`. Key fields get hoisted into plans even if unselected. The hard parts: batched entity fan-out, merged error/partial semantics, and composition-sensitive plan caching.

