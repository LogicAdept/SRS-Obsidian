<!--
reps: 0
priority: 0
-->
#API/GraphQL #SRS

> [!abstract] Short answer
> REST is an **architectural style** — resources addressed by URLs, uniform HTTP verbs, statelessness, hypermedia; GraphQL is a **query language and runtime** — one endpoint, a typed schema, and client-specified selections executed by resolvers. They solve the same problem (clients talking to backends) with different contracts: REST fixes response shapes per resource and reuses HTTP semantics; GraphQL fixes a type system and moves shape, aggregation, and versioning pressure from the URL space into the schema.

## Where the contracts actually differ

The precise, non-folklore comparison: **shape** — REST returns endpoint-defined payloads, GraphQL returns exactly the selection set ([[What is over-fetching and under-fetching compared with REST]]); **endpoint model** — many resource URLs versus one endpoint carrying the operation in the body; **typing** — REST's typing is conventional (OpenAPI describes it after the fact), GraphQL's schema is machine-checked before execution; **caching** — REST inherits HTTP caching for free (URL-keyed, verb-invalidating), GraphQL's single endpoint defeats URL-keyed caching and needs client-level caches ([[Why is HTTP caching harder with GraphQL than REST]]); **evolution** — REST evolves by adding endpoints and resource representations, GraphQL by additive schema changes with deprecation ([[How do you version a GraphQL schema]]).

```graphql
# one endpoint, two views of the same data:
# view A: { user(id: "1") { name } }
# view B: { user(id: "1") { name orders { total } } }
# the server code path differs only in which resolvers the selection triggers
```

**Listing 1.** The endpoint does not encode the view; the operation does — the defining structural difference from URL-oriented APIs.

```d2
direction: right
Rest: "REST" { width: 130; height: 50 }
R1: "resources + verbs" { width: 220; height: 55 }
R2: "HTTP cache friendly" { width: 230; height: 55 }
G: "GraphQL" { width: 130; height: 50 }
G1: "schema + selection set" { width: 250; height: 55 }
G2: "typed validation, one endpoint" { width: 290; height: 55 }
Rest -> R1
Rest -> R2
G -> G1
G -> G2
```

**Fig. 1.** Each model optimizes a different axis: REST leans on HTTP's uniform interface; GraphQL leans on a schema the client can program against.

> [!warning] Two folklore claims need correction every interview
> First: "GraphQL kills versioning" — it **moves** versioning into schema discipline: additive changes are cheap, but field removals, argument narrowing, and union expansions are still breaking, so real APIs still coordinate releases ([[Which GraphQL schema changes are breaking]]). Second: "GraphQL replaces REST" — they coexist deliberately: REST/HTTP semantics remain the standard for public, cache-heavy, resource-oriented APIs and for inter-service traffic where uniformity matters; GraphQL wins where clients are diverse (web, mobile, partners) and views aggregate many sources. Choosing is a workload decision, not a faith statement ([[When should you not use GraphQL]]).

Operational deltas matter too: monitoring shifts from URL metrics to operation-level metrics (hashes, names, field usage); authorization shifts from per-route middleware to field/type-aware enforcement; and error semantics move into the envelope ([[Why does GraphQL often return HTTP 200 when a field errors]], [[How do you authenticate and authorize a GraphQL request]]). A senior answer prices these shifts honestly instead of repeating "one endpoint, no over-fetching".

> [!tip] Interview answer
> REST is a style: URL-addressed resources, uniform verbs, HTTP-native caching and status semantics, shapes fixed per endpoint. GraphQL is a typed query language: one endpoint, a schema validated before execution, client-chosen selections resolved per field. GraphQL wins on shape flexibility and aggregation for diverse clients; REST wins on HTTP reuse, caching, and simplicity. Versioning is not eliminated but relocated into schema evolution discipline.

