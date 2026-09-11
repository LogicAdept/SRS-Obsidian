<!--
reps: 0
priority: 0
-->
#API/GraphQL #SRS

> [!abstract] Short answer
> Cap the nesting depth of incoming documents — usually with a server-side analyzer that counts the deepest field chain (fragments flattened, skip/include counted) and rejects operations above the limit before any resolver runs. graphql-java ships `MaxQueryDepthInstrumentation` for exactly this; typical production limits sit around 5–15 depending on schema depth, paired with complexity budgets since neither control covers the other's blind spot.

## How depth is counted and enforced

Depth is a static property of the document: the analyzer walks fields through fragment spreads and inline fragments, counting the longest chain from the root; meta fields and conditional fields count like any other. Enforcement lands before execution — the instrumentation wraps document parsing/validation, so rejected queries cost no resolver work ([[What is query complexity analysis in GraphQL]]).

```java
// graphql-java 26.1:
GraphQL graphql = GraphQL.newGraphQL(schema)
        .instrumentation(new graphql.analysis.MaxQueryDepthInstrumentation(3))
        .build();
// { user { friends { name } } }                         -> resolves normally
// { user { friends { friends { friends { name } } } } } ->
// {"errors":[{"message":"maximum query depth exceeded 5 > 3",
//   "extensions":{"classification":"ExecutionAborted"}}]}
```

**Listing 1.** Verified on graphql-java 26.1: the engine aborted a depth-5 chain against the limit 3, reporting both numbers — and nothing executed ([[How does the GraphQL execution engine resolve a query]]).

```d2
direction: down
Doc: "incoming document" { width: 220; height: 55 }
A: "static walk:\nlongest field chain" { width: 250; height: 60 }
V: "chain vs limit" { shape: oval; width: 170; height: 50 }
Ok: "continue validation/execution" { width: 300; height: 55 }
Rej: "abort:\nmaximum query depth exceeded" { width: 300; height: 60 }
Doc -> A -> V
V -> Ok: "within"
V -> Rej: "over"
```

**Fig. 1.** The whole control is pre-execution: measure the document's deepest chain, compare with the configured limit, abort cheaply when over.

> [!warning] Depth alone is gameable — and the limit is a business decision
> First: **wide beats deep** — a depth-3 document with three list levels of `first: 100` can dwarf a depth-10 scalar chain; depth limits must pair with complexity analysis and pagination caps ([[What is query complexity analysis in GraphQL]]). Second: fragments do not hide depth — the analyzer expands them, so "keep the document shallow by spreading fragments" fails ([[What is a GraphQL fragment]]). Third: a too-tight limit breaks legitimate features: schemas with honest 6-level hierarchies (order → items → product → category) need headroom; set the limit from the schema's real depth plus margin, not from fear — and version it as deliberately as any API change ([[How do you version a GraphQL schema]]).

Where the control lives operationally: instrumentation on the GraphQL object for raw graphql-java; gateway-level analyzers for federated graphs (so subgraphs never see over-deep documents); and for first-party clients, persisted queries make depth limits nearly moot — registered documents are known-shallow by construction ([[What are persisted queries in GraphQL]]). The remaining audience for runtime depth checks is arbitrary or third-party document construction — exactly the traffic worth gating ([[Why is rate limiting harder in GraphQL than REST]]).

> [!tip] Interview answer
> Depth limiting statically rejects documents whose longest field chain exceeds a configured maximum — graphql-java's MaxQueryDepthInstrumentation aborts before execution with "maximum query depth exceeded N > M". It blocks deep-recursion abuse cheaply, expands fragments, and must be paired with complexity analysis because wide documents can be as costly as deep ones. Set the limit from real schema depth plus margin.

