<!--
reps: 0
priority: 0
-->
#API/GraphQL #SRS

> [!abstract] Short answer
> GraphQL loses when the workload leans on what HTTP gives you for free, or when the schema would be a thin, unstable mirror of one source. Concretely: heavy public caching, simple resource-oriented CRUD, file-heavy or streaming transports, traffic from clients that cannot send rich requests, teams without schema-governance capacity, and single-client APIs with stable views are all cases where REST-style HTTP (or gRPC internally) is the better contract ([[What is the difference between GraphQL and REST]]).

## The decision drivers, one by one

**Caching and CDN economics**: URL-addressed resources with verb-based invalidation use HTTP caches, browsers, and CDNs natively; a single POST endpoint defeats that, so caching moves into client libraries or needs persisted queries plus custom layers — a real cost for cache-heavy public data ([[Why is HTTP caching harder with GraphQL than REST]]). **Rate limiting and abuse control**: per-endpoint limits are trivial in REST; per-operation cost analysis, depth limits, and complexity budgets are mandatory infrastructure in GraphQL ([[Why is rate limiting harder in GraphQL than REST]]). **Simple CRUD with stable shapes**: if every client needs the same fields of the same resources, the selection machinery buys nothing and charges tooling, validation, and N+1 vigilance ([[What is over-fetching and under-fetching compared with REST]]).

**Governance capacity**: a schema is a living contract — deprecation discipline, breaking-change detection, persisted-query management, and field-level auth need owners; without them GraphQL's flexibility turns into an unmaintainable graph ([[How do you version a GraphQL schema]]). **Query-cost asymmetry**: one request can express a dataset-sized traversal, so servers must bound work proactively; teams that cannot enforce limits should not expose arbitrary selections ([[What is query complexity analysis in GraphQL]]). **Operational tooling**: HTTP status metrics, standard auth middleware, and URL-based monitoring all assume the uniform interface; GraphQL shifts observability to operation hashes and field usage analytics — an investment ([[Why does GraphQL often return HTTP 200 when a field errors]]).

```d2
direction: down
W: "Workload profile" { width: 200; height: 55 }
C: "cache-heavy public data\n-> REST + CDN" { width: 300; height: 60 }
S: "internal high-throughput calls\n-> gRPC" { width: 300; height: 60 }
F: "diverse clients, churning views,\naggregated sources -> GraphQL" { width: 340; height: 70 }
W -> C
W -> S
W -> F
```

**Fig. 1.** The choice is workload-shaped: HTTP-native caching and uniformity favor REST; internal call efficiency favors gRPC; client-driven composition favors GraphQL.

```graphql
# A schema where GraphQL buys little: one stable view per resource, no shape churn.
type Query {
  product(id: ID!): Product
}
type Product {
  id: ID!
  title: String!
  price: Int!
}
```

**Listing 1.** When every client needs exactly these fields of exactly these types, the selection machinery has nothing to select — the same three fields ride fine in a plain REST response with HTTP caching attached.
> [!warning] "Not use GraphQL" does not mean "bad technology"
> Two traps in answering. First: the famous negatives — no HTTP caching, query cost, N+1 — are **managed** costs, not disqualifiers; mature stacks live with them daily. The honest disqualifiers are capacity and fit: no team to own schema governance, or genuinely stable single-client views. Second: do not argue against GraphQL because "queries can become expensive" while your REST API already accepts arbitrary query parameters that hammer the same database — the cost-control problem is universal; GraphQL merely concentrates it in one visible place ([[What is the N plus 1 problem in GraphQL]]). Interviews reward naming the *mechanism* behind each cost and the mitigation, not the scare-word.

Migration nuance worth mentioning: hybrid deployments are normal — REST for public resources and CDN coverage, GraphQL as the aggregation edge for first-party clients, gRPC internally; the "GraphQL instead of REST" framing is itself the trap ([[What is the difference between GraphQL and gRPC]]).

> [!tip] Interview answer
> Think in drivers: heavy HTTP caching or CDN distribution, simple stable CRUD, and uniform clients favor REST; internal high-throughput point-to-point calls favor gRPC; diverse clients with churning view requirements over aggregated sources favor GraphQL — and GraphQL demands schema governance: deprecation discipline, cost limits, field-level auth, operation analytics. Missing that capacity is the honest reason not to adopt it.

