<!--
reps: 0
priority: 0
-->
#API/GraphQL #SRS

> [!abstract] Short answer
> **Over-fetching** means the server sends more data than the client needs; **under-fetching** means it sends less, forcing extra round trips. Both are structural in classic REST: endpoints return fixed shapes, so one view needs data from several endpoints (under-fetching — the N+1-of-the-frontend) or gets superset payloads (over-fetching). GraphQL attacks both by letting the client state the exact shape: the response contains exactly the selected fields — no more, no less — from one endpoint.

## The mechanism behind the claim

In REST the response shape is fixed per resource per endpoint: a `/users/{id}` view returns whatever the server author chose. Different screens need different slices, so either the payload grows (over-fetching: a mobile list view receiving full user profiles) or the client makes several calls and stitches them (under-fetching: `/user`, then `/user/orders`, then `/orders/{id}/items`). GraphQL replaces endpoint-shaped responses with a single operation whose selection set *is* the response shape — unselected fields are never even resolved ([[How does the GraphQL execution engine resolve a query]]).

```java
// graphql-java 26.1: same source object, two different selections.
// { hero { id name } }              -> {"data":{"hero":{"id":"1000","name":"Luke Skywalker"}}}
// { hero { id } }                   -> the homePlanet component was never resolved at all
```

**Listing 1.** Verified on graphql-java 26.1: dropping a field from the selection dropped it from execution — the client shapes the payload per view ([[What is GraphQL introspection]]).

```d2
direction: down
R: "REST view" { width: 170; height: 50 }
E1: "GET /user" { width: 160; height: 50 }
E2: "GET /user/orders" { width: 190; height: 50 }
Ov: "payload superset\n(over-fetching)" { width: 240; height: 60 }
Un: "several round trips\n(under-fetching)" { width: 240; height: 60 }
G: "GraphQL: one operation,\nselection = response shape" { width: 300; height: 70 }
R -> E1
R -> E2
E1 -> Ov
E2 -> Un
G -> R: "replaces"
```

**Fig. 1.** REST's fixed shapes force one of the two failures per view; a selection-set API makes the client's need explicit per request.

> [!warning] "Exactly the selected fields" is a wire claim, not a cost claim
> Three honesty checks for interviews. First: preventing over-fetching on the **wire** does not make resolvers cheap — every selected field runs code, and nested selections per parent reproduce the N+1 pattern server-side unless batched ([[What is the N plus 1 problem in GraphQL]]). Second: under-fetching often reappears as *arguments*: without well-designed filter/limit arguments, clients either over-select and filter client-side (over-fetching returns through the back door) or issue one operation per slice ([[How do you paginate a GraphQL list]]). Third: REST is not condemned to fixed shapes — sparse fieldsets (`?fields=`), compound documents, and well-designed nested resources address both problems; the real difference is that GraphQL makes the shape contract **systematic and typed** rather than per-endpoint convention ([[What is the difference between GraphQL and REST]]).

Why interviews ask this: the pair over/under-fetching is the standard *rationale* for adopting GraphQL — so the senior-level answer names the counterweight: server-side cost control. Selection flexibility shifts payload-shaping responsibility to clients; the server must still bound work with depth/complexity limits, persisted queries, and batching, or the wire savings become CPU liabilities ([[What is query complexity analysis in GraphQL]]).

> [!tip] Interview answer
> Over-fetching is getting more than a view needs; under-fetching is needing several round trips to assemble one view — both fall out of REST's fixed per-endpoint shapes. GraphQL lets the client declare the exact shape in the selection set, so unrequested fields are not even resolved, in one request. The caveats: resolver cost follows selections, N+1 moves server-side, and REST mitigations exist — GraphQL's win is a typed, uniform shape contract.

