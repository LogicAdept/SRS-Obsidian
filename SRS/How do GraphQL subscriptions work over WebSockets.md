<!--
reps: 0
priority: 0
-->
#API/GraphQL #SRS

> [!abstract] Short answer
> A subscription is a **long-lived operation**: the client opens a WebSocket (or SSE), sends the operation once, and the server's root resolver returns a **source event stream** (a reactive Publisher); every event is executed through the normal selection set and pushed to the client as a complete GraphQL response. The WebSocket protocol layers on top: the client sends standard GraphQL messages (`subscribe`, `complete`), the server answers with `next`/`error`/`complete` frames — connection setup, acks, and resubscription are protocol, not language.

## The lifecycle over the socket

The mechanism has three layers. **Transport**: a WebSocket connection, optionally with the `graphql-transport-ws` subprotocol, which defines message types and the handshake (`connection_init` / `connection_ack`). **Operation**: one `subscribe` message carries the document and variables — like any GraphQL operation, validated against the schema first. **Execution**: the server resolves the subscription root field, whose resolver returns a Publisher; the engine subscribes to it, and for each event re-runs the selection set — each event's payload looks exactly like a query response, errors included per event ([[What is the difference between a GraphQL query a mutation and a subscription]]).

```java
// graphql-java 26.1: execute() on a subscription operation returns a result whose
// data is a Publisher of ExecutionResults — the engine maps events through the selection set.
// console:  subscribe field resolver ran, symbol=AAPL
// events=[{"data":{"ticker":{"price":101}}}, {"data":{"ticker":{"price":103}}}]
// the server transport (WebSocket handler) then serializes each event as a "next" frame.
```

**Listing 1.** Verified on graphql-java 26.1: one subscribe call, one source stream, two events — each independently shaped by the client's selection.

```d2
direction: down
C: "client: WebSocket open\nconnection_init" { width: 300; height: 65 }
S: "server: connection_ack" { width: 240; height: 55 }
Op: "subscribe message\ndocument + variables" { width: 290; height: 65 }
Pub: "root resolver ->\nsource event stream" { width: 290; height: 65 }
E1: "next: event 1 as full response" { width: 300; height: 60 }
E2: "next: event 2 ..." { width: 200; height: 50 }
C -> S: "handshake"
C -> Op
Op -> Pub
Pub -> E1 -> E2
```

**Fig. 1.** Protocol handshake, then one subscription operation; each stream event is executed and pushed as an ordinary GraphQL response frame.

> [!warning] Statefulness is the architecture decision, not the protocol
> First: **connections are state** — horizontal scaling needs sticky sessions or a pub/sub backbone (Redis, Kafka) so any node can serve any client's stream; the event source must live outside the node that holds the socket ([[What is GraphQL execution context]]). Second: **backpressure and slow consumers** are real: reactive-streams gives flow control per subscriber, but a server pushing to thousands of sockets must bound queues, drop or replay deliberately, and close dead connections — the protocol will not do it for you ([[Why is rate limiting harder in GraphQL than REST]]). Third: **resubscription is the client's job** after reconnects — mutations that happened while offline are not replayed unless you design event sourcing/replay into the stream or fall back to a query on reconnect ([[What is global object identification in GraphQL]]). Fourth: subscriptions authenticate at connection time and re-check at each operation — long-lived sockets outlive tokens ([[How do you authenticate and authorize a GraphQL request]]).

When to reach for them: genuinely push-shaped data (presence, collaborative state, live tickers). For "refresh when something changes", SSE plus a refetch — or plain polling — is often the cheaper, more cache-friendly design ([[When should you not use GraphQL]]).

> [!tip] Interview answer
> Subscriptions ride a WebSocket with a GraphQL subprotocol: handshake, then a subscribe message carrying the operation. The server's root resolver returns a source event stream (Publisher); the engine executes the selection set per event and pushes full GraphQL responses as next frames, closing with complete or error. Scaling means stateful connections plus a shared pub/sub, backpressure by design, and re-auth on long-lived sockets.

