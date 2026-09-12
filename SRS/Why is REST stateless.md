<!--
reps: 0
priority: 0
-->
#API/REST #SRS

# Why is REST stateless

> [!abstract] Short answer
> Statelessness means every request must carry all context needed to process it — identity, intent, negotiation — so the server keeps no client session between requests. The payoff is system-level: any node can serve any request, which gives horizontal scaling, fault tolerance, and monitoring visibility; the cost is repeated context and moving session state to the client.

## What the server is allowed to forget

The constraint (dissertation §5.1.3) says session state lives on the client. Servers may still hold resource state (the order's status) and caches; what they may not do is remember "this conversation" — the thing that would make request N+1 depend on request N having landed on the same node. Mechanically, self-contained requests are what make the rest work: a load balancer may route each call to any replica; a gateway can interpret, cache, or reject a message by looking at it alone; a crashed node is recovered by reissuing the request, not by re-binding a session ([[What is the difference between a stateful service and a stateless service]] for the general pattern; [[What is the relationship between HTTP and REST]] for where HTTP fits). In practice the client's carried context is usually a credential — bearer token or signed JWT — plus negotiation headers, which is exactly why token auth replaced classic server sessions in REST APIs ([[What is an HTTP session]] contrast; [[Why do you disable CSRF for a JWT REST API]] as a downstream consequence).

```d2
c1: client
n1: replica A
n2: replica B
lb: LB (stateless routing)
c1 -> lb: req1 + token
lb -> n2: served by B
c1 -> lb: req2 + token
lb -> n1: served by A
(no affinity needed)
note: no session on A or B —
all context rides the request {
  shape: text
}
```

**Fig. 1.** Because context rides in each request, the balancer may route every call to any replica; no node remembers the conversation.

## The trade-offs to name out loud

Costs: context repeats on every call (token bytes, per-request auth verification), and the client becomes responsible for holding conversational state — which pushed state into JWTs, cookies for browser flows, and resumable-request designs for long flows. Some flows genuinely need server-side state (OAuth flows, shopping carts); those become explicit resources or dedicated state stores rather than invisible session memory. There is also a monitoring benefit interviewers like: statelessness plus uniform interface gives visibility — an intermediary sees the whole interaction in one message, so tracing and auditing do not require correlating sessions ([[What is caching used for]] interacts: responses stay reusable only while the carried context is not personal).

```text
-> replica A:  GET /orders/7
   Authorization: Bearer eyJhbGci...    <- identity rides the request
   Accept: application/json

-> replica B:  GET /orders/42
   Authorization: Bearer eyJhbGci...    <- repeated context, no session lookup
   Accept: application/json
```

**Listing 1.** Two requests land on different replicas; each carries full context, so neither node needs the conversation history (conceptual).

> [!warning] Sticky sessions are the anti-pattern, not a mitigation
> Load balancers offer session affinity as a crutch for stateful apps; relying on it forfeits the scaling and fault-tolerance properties and creates hot spots when a node dies mid-conversation. If you need affinity, you have not made your requests self-contained yet.

> [!tip] Interview answer
> Statelessness keeps session state on the client: each request is self-contained, so any replica can serve any call. That buys horizontal scaling, transparent failover, and visibility for proxies and tracers. The price is repeated context — usually a bearer token or JWT — and moving conversation state client-side. Server-side memory is still fine for resource state and caches; what is forbidden is remembering the client conversation between requests.
