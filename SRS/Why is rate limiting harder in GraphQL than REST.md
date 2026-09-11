<!--
reps: 0
priority: 0
-->
#API/GraphQL #SRS

> [!abstract] Short answer
> REST limits **requests to a URL** — one endpoint, roughly one unit of work, so a counter per IP or token works. GraphQL packs **arbitrary work into one request**: a single document can traverse the entire graph, and two requests can differ by three orders of magnitude in server cost while looking identical at the transport. Rate limiting therefore moves from counting requests to **pricing operations** — depth limits, complexity scoring, and per-field or persisted-query quotas.

## From counters to cost models

The mechanism shift: in REST, URL granularity plus verb semantics make "N requests per minute" a usable unit; in GraphQL, request-count limits are trivially bypassed by bigger documents. Servers respond with layered controls. **Depth limiting** caps nesting (cheap, static) ([[How do you limit nested query depth in GraphQL]]). **Complexity analysis** prices each field — multiplying factors for list fields with `first`/`limit` arguments model fan-out — and rejects operations above budget, optionally returning a "cost" header so clients self-regulate ([[What is query complexity analysis in GraphQL]]). **Server-level guards**: timeouts, pagination bounds, and per-operation persisted-query allowlists shut down arbitrary document construction ([[What are persisted queries in GraphQL]]).

```java
// graphql-java 26.1 ships depth limiting out of the box:
GraphQL graphql = GraphQL.newGraphQL(schema)
        .instrumentation(new graphql.analysis.MaxQueryDepthInstrumentation(3))
        .build();
// { user { friends { name } } }                          -> ok
// { user { friends { friends { friends { name } } } } }  ->
// {"errors":[{"message":"maximum query depth exceeded 5 > 3",
//   "extensions":{"classification":"ExecutionAborted"}}]}
```

**Listing 1.** Verified on graphql-java 26.1: the engine aborted a depth-5 document against a limit of 3 before resolving any field — the GraphQL-native answer to "what does one request cost?".

```d2
direction: down
Rest: "REST: one URL = ~one unit" { width: 300; height: 60 }
Count: "count requests / IP / token" { width: 290; height: 60 }
G: "GraphQL: one request = ? units" { width: 290; height: 60 }
D: "depth limit" { width: 170; height: 50 }
Cx: "complexity budget" { width: 210; height: 50 }
Pq: "persisted queries" { width: 210; height: 50 }
Rest -> Count
G -> D
G -> Cx
G -> Pq
```

**Fig. 1.** REST's uniform interface gives rate limiting a natural unit; GraphQL must price the document itself with layered controls.

> [!warning] Counting requests is not just weak — it is wrong
> Two traps. First: **per-request counters actively discriminate against the pattern GraphQL encourages** — a client batching many views into one operation looks like one request, while a naive REST-style client looks like fifty; without cost-based accounting you punish exactly the aggregation you adopted GraphQL for ([[What is over-fetching and under-fetching compared with REST]]). Second: cost models are **estimates** — resolver cost varies with arguments and data (a `first: 100` on a hot path vs a cold one), so budgets need tuning, calibration against real field metrics, and a kill switch; and none of it replaces standard protections (auth before resolution, size limits on variables, timeouts) ([[How do you authenticate and authorize a GraphQL request]]).

Whitelisting via persisted queries is the hard ceiling: registered documents only, so cost is known at deploy time and unknown documents are rejected — common for first-party clients, impractical for open APIs, which must live with computed budgets ([[When should you not use GraphQL]]).

> [!tip] Interview answer
> REST limits per URL because one request is one unit; GraphQL lets any request express arbitrary traversal, so counting requests is meaningless. Practical limiting prices the operation: static depth limits, field-weighted complexity budgets returned to clients, timeouts and pagination bounds, and — strongest — persisted-query allowlists. GraphQL-native servers ship instrumentation for this, like MaxQueryDepth in graphql-java.

