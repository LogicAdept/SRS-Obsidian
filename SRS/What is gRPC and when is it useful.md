<!--
reps: 0
priority: 0
-->
#API/GRPC #SRS

# What is gRPC and when is it useful

> [!abstract] Short answer
> gRPC is an open-source, CNCF-hosted RPC framework built on HTTP/2 and Protocol Buffers: you define services and messages in .proto files, codegen produces typed clients and servers in any language, and calls ride multiplexed HTTP/2 streams with deadlines, metadata, and standardized status codes. It shines for internal, high-volume, polyglot service-to-service communication — especially with streaming — and fits poorly for browser-facing or cache-friendly public APIs.

## How a call works

You author the contract once: a .proto defining a service with rpc methods (four shapes — [[What are the four kinds of gRPC RPCs]]) and message types; protoc's plugins generate client stubs and server bases for Java, Go, Python, and more. At runtime a channel opens HTTP/2 connections to the server; each call is a stream: the client sends a request message (framed, protobuf-encoded), the server answers one or many, with trailers carrying the final status. Deadlines (the gRPC timeout model) travel with the call and propagate downstream — the server sees "the caller gives up in 200ms" and can cancel nested work; metadata carries auth tokens and tracing keys; the status model (OK, INVALID_ARGUMENT, NOT_FOUND, UNAVAILABLE, and a dozen more) standardizes failures across languages. The wire is binary protobuf — compact and fast, at the cost of human-readability ([[What is Protocol Buffers and why does gRPC use it]]; [[What is the difference between RPC and gRPC]] for the lineage).

```d2
cli: Java client (stub)
h2: HTTP/2 channel {
  s1: stream 1 (unary)
  s2: stream 2 (server streaming)
  s3: stream 3 (in flight)
}
srv: Go server (base)
cli -> h2: open channel
h2 -> srv: concurrent calls
multiplexed on one conn
srv -> h2: messages + trailers
(grpc-status)
h2 -> cli: deadline propagates:
cancel nested work
```

**Fig. 1.** One HTTP/2 channel carries concurrent typed calls; deadlines and statuses are first-class wire citizens.

## The fit and the misfit

Use gRPC when both ends are yours and the traffic is heavy or latency-sensitive: internal microservice meshes, polyglot backends, mobile-to-backend where bandwidth matters, and streaming topologies (live updates, uploads, bidirectional chat) that HTTP/1-style APIs handle awkwardly. Generated stubs become the shared contract — evolution rules and all ([[What is the remote procedure invocation pattern between microservices]]). Avoid it at the public edge: browsers lack raw HTTP/2-stream control, so gRPC-Web shimmed through a proxy is the browser story; no HTTP caching semantics apply to typed RPC calls ([[Why is HTTP caching harder with GraphQL than REST]] for a related shape of problem; [[What is the difference between REST and gRPC]] for the style trade); debugging needs grpcurl or reflection because payloads are binary. The common production shape is both: REST/OpenAPI at the public edge, gRPC inside ([[What is the API gateway pattern in microservices]] for the seam).

```proto
syntax = "proto3";

service OrderService {
  rpc GetOrder (OrderId) returns (Order);                  // unary
  rpc WatchOrders (OrderFilter) returns (stream Order);    // server streaming
  rpc UploadInvoices (stream Invoice) returns (Summary);   // client streaming
  rpc Chat (stream ChatMsg) returns (stream ChatMsg);      // bidirectional
}

message OrderId { int64 id = 1; }
message Order  { int64 id = 1; string status = 2; }
```

**Listing 1.** The .proto contract: one service declaring all four call kinds; protoc generates clients and servers from it (conceptual, per grpc.io core concepts).

> [!warning] A channel is connection-oriented — plan for load balancing
> gRPC multiplexes many calls over few long-lived HTTP/2 connections; naive layer-4 balancing pins a channel to one pod and concentrates load. Use client-side load balancing, or an L7 proxy that understands HTTP/2, or you will wonder why one replica is hot.

> [!tip] Interview answer
> gRPC is a CNCF RPC framework: contracts in .proto, codegen to typed clients and servers in any language, calls as protobuf over multiplexed HTTP/2 streams with propagating deadlines, metadata, and standard status codes. It fits internal high-volume polyglot traffic, especially streaming; it fits poorly at the browser edge (gRPC-Web) or where HTTP caching matters. The typical shape: gRPC inside, REST at the public edge.
