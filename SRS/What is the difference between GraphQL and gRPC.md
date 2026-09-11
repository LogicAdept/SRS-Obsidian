<!--
reps: 0
priority: 0
-->
#API/GraphQL #SRS

> [!abstract] Short answer
> gRPC is an **RPC transport protocol**: service methods with binary Protobuf messages over HTTP/2, code-generated typed stubs, no client-specified shape — the server's method signature is the contract. GraphQL is a **query language**: clients compose selections against a schema and the response mirrors the selection. gRPC optimizes machine-to-machine call efficiency; GraphQL optimizes client-driven data shaping for diverse UIs. They are often deployed together rather than instead of each other.

## The real comparison axes

**Contract and codegen**: both are strongly typed and generate client code, but Protobuf types describe *messages* for fixed methods, while GraphQL schema types describe *fields a client may select* — flexibility lives on different sides ([[What is the difference between schema-first and code-first GraphQL]]). **Shape on the wire**: gRPC returns whole messages per method (over-fetching by method design, mitigated by field masks — which are ad hoc and untyped), GraphQL returns exact selections and rejects unknown fields before execution ([[What is over-fetching and under-fetching compared with REST]]). **Transport**: gRPC owns a full duplex HTTP/2 protocol with streaming as a first-class concept (client-, server-, bi-di streams); GraphQL rides ordinary HTTP for query/mutation and needs a separate long-lived transport (WebSocket/SSE) for subscriptions ([[How do GraphQL subscriptions work over WebSockets]]). **Serialization**: Protobuf's compact binary with schema evolution rules versus JSON (usually) with envelope semantics and text size costs ([[What does the GraphQL errors array contain]]).

```graphql
# same capability, different idioms:
# gRPC:  rpc GetUser(GetUserRequest) returns (User)        <- one fixed shape per method
# GraphQL: { user(id: "1") { name orders(limit: 5) { total } } }   <- client composes the shape
```

**Listing 1.** The method-based vs selection-based split: gRPC's contract is behavior-per-method; GraphQL's is field-level composition.

```d2
direction: right
G: "gRPC" { width: 110; height: 50 }
G1: "HTTP/2 + Protobuf\nbinary, streaming" { width: 240; height: 65 }
G2: "service methods\nstubs, low latency" { width: 220; height: 60 }
Q: "GraphQL" { width: 110; height: 50 }
Q1: "schema + selection set\nJSON over HTTP" { width: 250; height: 65 }
Q2: "client-shaped payloads" { width: 240; height: 55 }
G -> G1
G -> G2
Q -> Q1
Q -> Q2
```

**Fig. 1.** gRPC moves efficiency (binary, streaming, stubs); GraphQL moves flexibility (selections, aggregation) — different optimization targets, not a ranking.

> [!warning] Two folklore corrections
> First: "gRPC is faster" is only half-true — raw serialization and multiplexing favor gRPC, but a GraphQL layer over gRPC backends costs one hop, and for human-facing UIs the bottleneck is usually rendering and round trips, not wire format. The standard pattern is **gRPC between services, GraphQL at the edge** for web/mobile clients — the two compose ([[When should you not use GraphQL]]). Second: "gRPC is impossible for browsers" is outdated — gRPC-Web exists but with proxying and missing trailers support; it is workable yet still not as native as JSON, which keeps GraphQL the default browser contract ([[What is the difference between GraphQL and REST]]).

Choose gRPC for internal service meshes, high-throughput point-to-point calls, polyglot teams needing strict contracts and streams. Choose GraphQL for client-facing aggregation over heterogeneous sources where view shapes churn. Choose plain REST when HTTP-native caching and public simplicity dominate ([[What is the difference between GraphQL and REST]]).

> [!tip] Interview answer
> gRPC is RPC over HTTP/2 with Protobuf: fixed method signatures, binary streaming, generated stubs — built for efficient machine-to-machine calls. GraphQL is a schema plus client-composed selections resolved per field — built for diverse clients shaping their own payloads. gRPC for internal calls and streams, GraphQL at the edge for UI aggregation; field masks versus selection sets is the cleanest one-line contrast.

