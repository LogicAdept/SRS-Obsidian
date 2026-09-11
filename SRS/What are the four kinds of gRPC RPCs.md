<!--
reps: 0
priority: 0
-->
#API/GRPC #SRS

# What are the four kinds of gRPC RPCs

> [!abstract] Short answer
> A gRPC method is declared with its cardinality in the .proto: unary (one request, one response), server streaming (one request, a response stream), client streaming (a request stream, one response), and bidirectional streaming (both sides stream independently on one HTTP/2 stream). The kind is part of the contract — it decides the interaction topology, backpressure, and how deadlines behave.

## The four shapes and their jobs

Unary is the request/response classic — GetOrder(id) -> Order — the shape all of REST knows. Server streaming answers one request with a sequence: a metrics feed, a large export in chunks, live price updates; the client gets a Stream (Java: StreamObserver on the response side) and can cancel mid-stream, which propagates as cancellation to the server. Client streaming inverts it: an upload of many chunks answered by one summary — a batch importer acknowledging with counts. Bidirectional runs two independent streams on one HTTP/2 stream — chat, multiplayer sync, watch-and-push — either side writes whenever it has data; the protocol does not couple the sequences (application logic does). In Java all of this is StreamObserver callbacks: server methods receive a request (unary/server-streaming) or a response StreamObserver (client/bidi), and io.grpc.stub annotations generate the bases from the .proto. Deadlines and cancellation apply to every kind — the client's context deadline propagates, and abandoning a stream must actually stop the server's work ([[What is gRPC and when is it useful]] for why streaming shapes matter; [[What is the difference between RPC and gRPC]] for where this capability sits historically).

```d2
u: unary {
  a: request ->
  b: <- response
}
ss: server streaming {
  a: request ->
  b: <- resp, resp, resp...
}
cs: client streaming {
  a: req, req, req... ->
  b: <- response
}
bi: bidirectional {
  a: req... -> (independent)
  b: <- resp... (independent)
}
one: all four ride ONE
HTTP/2 stream each {
  shape: text
}
```

**Fig. 1.** Cardinality is the contract: 1-1, 1-N, N-1, N-N — all on multiplexed HTTP/2 streams with propagating deadlines.

## Choosing kinds and their costs

The kind you pick becomes an API commitment: switching a unary endpoint to streaming later is a breaking change, so model by need, not by coolness. Server streaming fits read-side fan-out (tail a job, subscribe to a topic slice); client streaming fits write-side batching (telemetry, logs); bidi fits session-shaped exchanges — and carries session complexity: ordering guarantees you must define, per-message acknowledgment you must design, and backpressure via flow control you must respect (the HTTP/2 window is transport-level; application-level overload still needs your design). Error semantics differ subtly per kind: a unary fails once; a server stream can deliver many messages then fail — clients must treat mid-stream status trailers as terminal for the whole call ([[What is the difference between REST and gRPC]] for the style comparison; [[What are webhooks and how do you implement them reliably]] — server streaming and webhooks solve overlapping push problems with opposite initiation).

```proto
service JobService {
  // unary: submit, get verdict
  rpc Submit (JobSpec) returns (JobHandle);
  // server streaming: tail progress
  rpc Watch (JobHandle) returns (stream Progress);
  // client streaming: upload chunks, one verdict
  rpc Upload (stream Chunk) returns (Ack);
  // bidirectional: independent both ways
  rpc Session (stream Event) returns (stream Event);
}
```

**Listing 1.** Cardinality is declared per method in the .proto; the comment names the interaction each kind serves (conceptual, per grpc.io core concepts).

> [!warning] A stream is not a queue
> A dropped connection ends the stream: no replay, no acknowledgment ledger, no redelivery — that is your application layer (or a real broker). Teams reaching for bidirectional streams to "do messaging" re-implement Kafka badly; keep streams for live interaction, not durable delivery.

> [!tip] Interview answer
> Four kinds, declared per method: unary — request, response; server streaming — one request, many responses, good for feeds and exports; client streaming — many requests, one summary, good for uploads and batching; bidirectional — two independent streams for session-shaped work like chat. All ride one HTTP/2 stream with propagating deadlines and cancellation. The kind is part of the contract, so I model it by interaction need, and I remember streams are not durable messaging.
