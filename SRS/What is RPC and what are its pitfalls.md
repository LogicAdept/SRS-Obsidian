<!--
reps: 0
priority: 0
-->
#API/RPC #SRS

# What is RPC and what are its pitfalls

> [!abstract] Short answer
> RPC (Remote Procedure Call) is the pattern of invoking code on another machine as if calling a local function: a client stub packs the call (marshalling), a transport moves it, a server stub unpacks and dispatches, and the reply travels back. Its central pitfall is exactly the hiding: a network call is not a function call — it can time out with the outcome unknown, fail halfway, or succeed slowly, and code written as if otherwise breaks.

## The machinery

An RPC stack has five moving parts. The interface definition (IDL — a .proto, CORBA IDL, or RMI's implied interface) fixes method signatures across languages. The client stub (proxy) presents the local-looking method and turns arguments into bytes (marshalling) tagged with method identity. The transport (HTTP/2, TCP, historically proprietary) delivers the request; the server skeleton unpacks, locates the implementation, invokes it, and marshals the response back; exceptions or status codes carry failures. gRPC is the modern embodiment; JSON-RPC is the minimal one ([[What is the difference between RPC and gRPC]]); Java RMI was the JVM-native variant ([[What is the remote procedure invocation pattern between microservices]] for the microservice-pattern view). The illusion is the product — and the trouble: argument semantics differ from value semantics (passing a large object graph by value, lazy fields that explode into N+1 fetches across the wire).

```d2
c: caller
cs: client stub (proxy)
net: transport
ss: server skeleton
impl: implementation
c -> cs: local-looking call(args)
cs -> net: marshal -> bytes + method id
net -> ss: request
ss -> impl: unpack, dispatch
impl -> ss: result or error
ss -> net -> cs: reply
cs -> c: return value
(or exception/status)
```

**Fig. 1.** The five-part path a "local" call actually takes; the caller sees only the first and last hop.

## The pitfalls, named precisely

First, the outcome problem: a timeout does not tell you whether the server executed — a retry may double-charge, so every RPC needs an idempotence or dedup story at the application level ([[What is idempotency in HTTP and in messaging]]; [[What is the Idempotency-Key header used for in HTTP APIs]]). Second, partial failure: the call succeeded on the server but the reply was lost, or downstream dependencies of the server failed — distributed state now disagrees ([[How do you handle a two second network outage]] for the operational handling). Third, latency and capacity: a "function call" that takes 50ms and consumes server threads changes algorithmic thinking — chatty object-oriented APIs over RPC (fine-grained getters) collapse under round-trip costs, which is why interfaces must be coarse-grained. Fourth, coupling: shared stubs version-compile clients to servers; renaming a method breaks wire compatibility, so interface evolution needs explicit contract discipline ([[What changes are breaking for a REST API]] — same problem, REST at least forces the boundary into documents). The classic critique (Waldo et al., "A note on distributed computing") stands: local and remote calls differ in kind — failure modes, latency, memory — and pretending otherwise produces systems that work in the lab and fail in production.

```text
caller:        result = getOrder(7)         <- looks local
client stub:   marshal -> {method:"GetOrder", args:[7]} -> bytes
transport:     frames to the remote machine
server skeleton: unmarshal -> dispatch to implementation
reply:         bytes -> stub -> result (or error)
failure reality: timeout = outcome UNKNOWN -> retry needs idempotence
```

**Listing 1.** What "local-looking" hides: marshal, transport, dispatch — and an outcome the caller must design for (conceptual).

> [!warning] Local call syntax hides remote semantics — until it cannot
> No amount of stub polish makes a network call atomic, instant, or reliably-once. Treat every RPC as a message exchange with unknown delivery outcome: design for timeouts, retries with idempotence, and explicit failure states, and the "local call" framing becomes syntax sugar, not architecture.

> [!tip] Interview answer
> RPC lets code invoke a remote service through a local-looking method: a client stub marshals arguments over a transport, a server skeleton dispatches to the implementation. The pitfalls come from the hidden network: timeouts leave the outcome unknown so retries need idempotence, partial failures leave inconsistent state, chatty interfaces drown in round-trips, and shared interface definitions couple versions. gRPC modernizes the machinery — the discipline it demands has not changed since Waldo's critique.
