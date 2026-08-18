<!--
reps: 0
priority: 0
-->
#API/GraphQL #API/GRPC #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Compilation comparison of three styles:

REST: resource URLs, JSON, HTTP cache-friendly; public APIs and simple CRUD.

GraphQL: client-specified fields, typically one endpoint; over/under-fetching vs REST; N+1 and HTTP caching as costs; fits complex frontends / BFF.

gRPC: HTTP/2 plus Protobuf, binary, generated stubs, unary and streaming; dumps pick it for internal service-to-service, latency budgets, polyglot typing. Downsides listed: not browser-native without gRPC-Web/proxy; harder to debug binary; schema field-number discipline.

Hybrid named often: REST at the edge, gRPC inside, GraphQL as a client-facing facade.

> [!warning] Unverified traps from the dump
> - Dump claim: they are complementary, not one winner; gRPC for internals, GraphQL for flexible clients.
