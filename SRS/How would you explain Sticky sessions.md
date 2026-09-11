<!--
reps: 0
priority: 0
-->
#SystemDesign #SRS

# How would you explain Sticky sessions

> [!abstract] Short answer
> Sticky sessions (session affinity) make a load balancer route all requests from one client to the same backend instance, so server-local session state keeps working without a shared store. Affinity is usually achieved by a cookie the LB injects (NGINX `sticky cookie`, AWS ALB's load balancer-generated cookie) or by hashing a client attribute (IP hash). It is a compatibility tool, not an architecture: it breaks even load on scale-out and failover, so the modern default is stateless services with externalized sessions.

## How affinity is implemented

Cookie-based affinity: on the first response the balancer attaches a cookie identifying the chosen backend; subsequent requests carrying that cookie are routed to the same target — NGINX documents `sticky cookie` (the LB learns the upstream from a cookie it injects) alongside `hash` and `ip_hash` directives; AWS ALB offers load balancer-generated (duration-based) and application-controlled (the app sets a specific cookie) duration cookies; Azure Application Gateway implements the same as cookie-based affinity. IP hash hashes the client address to a backend deterministically — no cookie, but breaks behind proxies that rewrite client IPs and redistributes wholesale when the backend set changes. All affinity schemes share a failure property: the pinned backend dying forces its clients onto another instance, and their server-local sessions are gone — login state, carts, half-filled forms vanish unless the session lived elsewhere.

```d2
direction: down
client: {shape: person; width: 120; height: 60}
lb: {
  label: "load balancer\nsticky cookie: route to backend-2"
  width: 240
  height: 80
}
b1: {label: "backend-1\nsession: none"; width: 150; height: 70}
b2: {
  label: "backend-2\nHTTP session (server-local)"
  width: 170
  height: 70
}
client -> lb: "all requests (cookie)"
lb -> b2: "always"
```

**Fig. 1.** Affinity pins one client to one backend holding its session.

## When it is right and when it is a trap

Sticky sessions are the pragmatic answer for a legacy application that keeps sessions in server memory and cannot be refactored quickly — it buys horizontal instance scale (mostly) without a session store. The traps are load skew (a pinned long-lived user accumulates memory on one instance; the balancer cannot rebalance mid-session), degraded failover (instances are not interchangeable), and a false sense of statelessness — scaling events or zone failures still lose sessions. The architectural answer is to externalize state: serialize sessions into Redis (shared, survives instance death — [[How do you handle Redis connection failures in Spring]] covers its failure handling), or go token-based (JWT) so no server holds state and any instance serves any request — the stateless-service ideal in [[What is the difference between a stateful service and a stateless service]]. Spring's session management mechanics ([[How do you configure session management in Spring Security]]) and cluster-wide cache invalidation ([[How do you invalidate Spring Cache in a cluster]]) are the concrete migration steps. Health checks and draining ([[How would you explain Health checks]], [[How would you explain Connection draining]]) determine how affinity behaves when backends leave rotation.

> [!warning] Affinity converts one backend's death into many users' logout
> Pinning users to instance-local sessions means every backend failure or deploy evicts those users' state mid-flight. If sessions cannot be externalized, at least plan draining and replication — otherwise availability of the instance becomes availability of everyone it pinned.

> [!tip] Interview answer
> Sticky sessions pin a client to one backend via an injected cookie or IP hash, preserving server-local session state. I treat it as a migration tool for legacy stateful apps; the target design externalizes sessions to Redis or goes JWT-stateless, because affinity skews load, breaks even on failover, and makes deploys lossy for pinned users.
