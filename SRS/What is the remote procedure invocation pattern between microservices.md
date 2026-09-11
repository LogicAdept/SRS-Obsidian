<!--
reps: 0
priority: 0
-->
#Patterns/Architecture/Microservices/CommunicationStyles #DistributedSystems/Communication #API/RPC #SRS

# What is the remote procedure invocation pattern between microservices

> [!abstract] Short answer
> Remote procedure invocation (RPI) is the synchronous communication style for microservices: a service calls another service's API and blocks for the response — REST over HTTP the common default, gRPC for high-throughput internal calls. Richardson lists it as one of the two main inter-service communication styles; the caller's error handling (timeouts, retries, circuit breaking) is part of the pattern's price.

## Mechanics of the synchronous contract

The caller composes a request to a concrete endpoint — resolved via discovery or a logical name — and waits. The protocol semantics do the heavy lifting: REST gives resource-oriented semantics, status codes and caching ([[What is the relationship between HTTP and REST]] for the foundation; [[What is the API gateway pattern in microservices]] for the edge); gRPC gives schema-typed RPC over HTTP/2 with deadlines and streaming ([[What is the difference between REST and gRPC]] for the trade-off). What makes it RPI rather than messaging: the caller's control flow continues only when the answer arrives, so failure handling is in-process — connect/timeout exceptions map to retry or fail-fast decisions.

```java
// caller-side deadline: the synchronous contract means the caller owns failure handling
try {
    HttpResponse<String> ok = client.send(HttpRequest.newBuilder(
            URI.create("http://127.0.0.1:18103/charge?amount=10")).build(),
            HttpResponse.BodyHandlers.ofString());
    System.out.println("order service: /charge -> HTTP " + ok.statusCode());
} catch (HttpTimeoutException e) {
    // the remote side is slow: caller decides - retry / compensat / fail
}
```

**Listing 1.** Verified on JDK 21 (G08_RpiHttp in empirics): a fast charge returns `HTTP 200 ok`; against a deliberately slow endpoint, the 300ms request timeout fires `HttpTimeoutException` in the caller while the server eventually completes into the void (out/G08_RpiHttp.txt).

## The costs that shape every RPI design

Availability coupling: the caller cannot proceed without the callee — a chain of five RPI hops multiplies unavailability and latency; deep synchronous chains are the signature of a distributed monolith. The standard mitigations are budgets (per-call timeouts below the caller's own deadline), retries with backoff on idempotent operations only ([[What is idempotency in HTTP and in messaging]]), circuit breakers to stop stampeding a dying downstream ([[How would you explain Circuit Breaker]]), and caching where semantics allow. Temporal coupling is structural: if the use case can tolerate "accepted, process later", the messaging style with async delivery is usually the better fit ([[Which interaction styles do you know in microservices]] contrasts the styles; [[How would you orchestrate communication between multiple services]] covers the coordination layer above RPI).

> [!warning] A timeout is a third answer, not a failure
> When an RPI call times out, the caller does not know whether the operation happened — the request may still have succeeded after the caller gave up. Treating timeout as "didn't happen" and blindly retrying a non-idempotent POST double-executes it. Every RPI design must classify operations by idempotency and design the retry policy per class, not per framework default.

> [!tip] Interview answer
> RPI is the synchronous style: call another service's API and wait — REST or gRPC. It's simple, natural for request/response and lets protocols do the semantics, but it couples my availability to the callee's, so every call needs a timeout budget, idempotency-aware retries and circuit breaking. I use RPI when the caller genuinely needs the answer now, and reach for messaging when "accepted, processed later" is enough.
