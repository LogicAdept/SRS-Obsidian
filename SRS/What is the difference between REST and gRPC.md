<!--
reps: 0
priority: 0
-->
#API/REST #API/GRPC #SRS

# What is the difference between REST and gRPC

> [!abstract] Short answer
> REST is an architectural style: resources, uniform HTTP methods, negotiable representations, and web infrastructure doing the heavy lifting. gRPC is an RPC framework: typed operations, protobuf messages, HTTP/2 multiplexing and streaming, and generated code. REST optimizes ecosystem properties — reachability, cacheability, client diversity; gRPC optimizes per-call properties — latency, payload size, typing, streaming.

## The head-to-head

Interface shape: REST names nouns and lets methods carry intent ([[What is a resource in a RESTful context]]); gRPC names verbs — service methods with typed request/response messages. Wire: typical REST is JSON over HTTP/1.1 — human-readable, tool-friendly, verbose; gRPC is protobuf over HTTP/2 — compact (a fraction of the JSON size for the same payload — [[What is Protocol Buffers and why does gRPC use it]]), typed by schema, multiplexed with native streaming in four call shapes ([[What are the four kinds of gRPC RPCs]]). Failure model: REST reports via HTTP status classes plus a body convention ([[Which HTTP status codes matter most in REST API design]]); gRPC reports a standardized status code on the call, independent of HTTP codes riding beneath. Caching: REST inherits HTTP caching for free where resources allow ([[How do you make REST API responses cacheable]]); gRPC calls are POST-shaped operations — application-level caching only ([[Why is HTTP caching harder with GraphQL than REST]] — a similar trade). Ecosystem: REST wins browsers, curl, gateways, and reachability; gRPC wins codegen, deadlines propagation, and polyglot type safety. Errors and evolution are disciplines in both ([[What changes are breaking for a REST API]] versus proto field-number rules).

```d2
t: REST vs gRPC
t.shape: {
  r1: resources + uniform methods
  g1: typed service methods
}
t.wire: {
  r2: JSON over HTTP/1.1
  g2: protobuf over HTTP/2
+ streaming
}
t.cache: {
  r3: HTTP caching native
  g3: app-level only
}
t.client: {
  r4: browsers, curl, any client
  g4: generated stubs, grpc-Web
for browsers
}
t.use: {
  both: REST at public edge,
gRPC inside the mesh
}
```

**Fig. 1.** The axes and the usual synthesis: both, per boundary, not either/or.

## Choosing the boundary

Public, browser- or partner-facing APIs stay REST: reachability without SDKs, cacheability at CDNs, debugging with curl, and an OpenAPI contract ([[What is OpenAPI and how does Swagger relate to it]]). Internal service-to-service meshes, mobile uplinks with constrained bandwidth, and streaming topologies take gRPC: generated stubs kill serialization drift, deadlines propagate through call chains, and streaming is native. The comparison is per boundary, not per company — most serious systems run both ([[What is gRPC and when is it useful]] for the deployment; [[What is the difference between an API and a web service]] for the boundary-obligation frame). Interview traps: "gRPC replaces REST" (they optimize different axes), "gRPC is always faster end-to-end" (marshalling wins the wire; the network and your query patterns dominate), and "REST cannot stream" (SSE and chunked responses exist — gRPC's four-shape streaming is just more general).

```text
read order #7

REST : GET /orders/7  Accept: application/json
       -> 200 {"id":7,"status":"NEW"}      (resource + representation)
       caching: ETag + Cache-Control on the wire

gRPC : stub.getOrder(OrderId{id:7})
       -> Order{id:7, status:"NEW"}        (typed method + message)
       caching: application-level only
```

**Listing 1.** The same read in both styles: URI and representation versus stub and message; HTTP caching rides only the first (conceptual).

> [!warning] "Faster" needs the measurement boundary
> gRPC wins bytes and CPU per call, but a chatty gRPC design loses to a well-shaped REST endpoint with caching. The wire format is rarely the bottleneck — round-trip count and data shape are; optimize those first in either style.

> [!tip] Interview answer
> REST is a style — resources, uniform methods, HTTP-native caching, any client; gRPC is a framework — typed methods, protobuf over HTTP/2, four streaming shapes, propagating deadlines, generated code. REST wins the public edge: reachability, debuggability, CDN caching. gRPC wins internal meshes: latency, typing, streaming. I run both — REST/OpenAPI outside, gRPC inside — and I do not pretend the wire format outranks call shaping in performance.
