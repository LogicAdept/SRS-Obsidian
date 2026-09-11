<!--
reps: 0
priority: 0
-->
#SystemDesign/Architecture #DataAndState/State #SRS

# What is the difference between a stateful service and a stateless service

> [!abstract] Short answer
> A stateless service keeps no client state between requests: every request carries everything needed to serve it (credentials, parameters), and any instance can handle any request — sessions live in a token or an external store. A stateful service holds per-client or per-session state in memory (or pinned local storage) across requests, so subsequent requests must reach the same instance. Statelessness is what makes horizontal scaling trivial; statefulness buys locality and protocol continuity at the cost of routing constraints.

## The mechanical difference and its consequences

A stateless request handler is a pure function of (request, shared data): given the same input and the same database, any replica produces the same result. Nothing in the instance remembers the client — no HTTP session map, no warm per-user cache that is required for correctness, no pinned file handles that matter. The consequences: a load balancer may round-robin freely; instances can be added, drained or crashed mid-conversation with no user-visible loss (the drain drill of [[How would you explain Connection draining]] becomes safe); autoscaling is honest ([[How would you explain common principles for scaling software systems]]). A stateful service inverts this: its memory is part of the system's correctness. HTTP sessions, WebSocket/game/long-poll session objects, in-memory caches that must not vanish, locally buffered writes — all require session affinity ([[How would you explain Sticky sessions]]) and make instance death a user-visible event. The state still exists somewhere in stateless designs — it moved out: signed tokens carry it per request, Redis or a database holds it shared ([[How do you use Redis as a Spring CacheManager]]-style externalization), queues hold work-in-flight.

```text
stateless: any instance -> any request
           scale = add replica; failure = reroute (no loss)
           state lives in: JWT/cookies, Redis, DB, queues
stateful:  this instance -> this client (affinity required)
           scale = rebalance sessions; failure = state loss
           state lives in: instance memory / local disk
```

**Listing 1.** The routing and failure consequences of where state lives.

## Choosing and the middle ground

Prefer stateless for anything HTTP-shaped and horizontally scaled — it is the default posture of microservices and the precondition for honest autoscaling and zero-downtime deploys. Statefulness is legitimate where the state IS the service: long-lived streaming connections, leader-based coordination, in-process caches as performance (not correctness) layers, game/real-time servers — designs that accept affinity and plan for state migration or loss. Two clarifications sharpen interviews: first, "stateless" does not mean "no data" — it means no per-client data that lives and dies with the instance; a stateless service still reads and writes shared stores constantly. Second, caches complicate the purity: an in-memory cache is state, but permissible statelessness-tolerating state — its loss degrades latency ([[What difficulties arise when working with caching]]), not correctness. Where true state must survive instance death, externalize (Redis sessions, queue-backed work) or replicate deliberately ([[How would you explain database replication strategies]] at application level). [[How would you explain Sticky sessions]] covers the routing workaround; [[How do you invalidate Spring Cache in a cluster]] the shared-cache migration path.

> [!warning] Local state is a silent scaling ceiling
> A service that stores sessions or per-user state in instance memory scales fine until the first rebalance or deploy — then users are logged out mid-flow and the team discovers the architecture. Externalize state before scaling, not after the first incident.

> [!tip] Interview answer
> Stateless services hold no per-client state between requests — any replica serves any request, so scaling, draining and failover are safe; state lives in tokens or external stores. Stateful services pin clients to instances holding their state, requiring affinity and planned failure handling. I default to stateless and pay for state only where the state is the product.
