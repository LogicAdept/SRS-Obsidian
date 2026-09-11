<!--
reps: 0
priority: 0
-->
#Patterns/Architecture/Microservices/ExternalAPI #API/Gateway #SRS

# What is the API gateway pattern in microservices

> [!abstract] Short answer
> The API gateway is the single entry point all clients hit instead of calling services directly: it routes each request to the owning service and often enforces the cross-cutting edge concerns once — authentication, rate limiting, TLS termination, response shaping. Richardson positions it as the microservices equivalent of the Facade pattern; behind it, services may change address, split or merge without client releases.

## The mechanism: route table plus edge policy

The gateway holds a route table — external path prefix to internal service — and forwards, adding or enforcing policy on the way through: token verification and identity propagation ([[How do you secure microservices with Spring Security]] covers the app-level twin; the gateway enforces the perimeter), rate limits and quotas per client, TLS termination, request/response shaping, and edge caching. Composition is optional: gateways commonly do light fan-out for simple views ([[What is the API composition pattern in microservices]] names the pattern; [[How would you explain the backends for frontends pattern]] splits experience logic out of the gateway when shaping per client gets rich). Routing is also the migration seam: shifting a prefix to a new service is the strangler fig's cutover move ([[What is the strangler fig pattern and when do you use it]]).

```d2
direction: down
c: "Clients" {style.fill: "#eceff1"}
gw: "API gateway
routes + auth + rate limit + TLS" {style.fill: "#fff3e0"}
o: "Order service" {style.fill: "#e8f5e9"}
u: "User service" {style.fill: "#e8f5e9"}
r: "Report service" {style.fill: "#e8f5e9"}
c -> gw
gw -> o: /orders/*
gw -> u: /users/*
gw -> r: /reports/*
```

**Fig. 1.** One door in front of the fleet: clients know the gateway; only the gateway knows the current topology.

```java
String path = ex.getRequestURI().getPath();
String token = ex.getRequestHeaders().getFirst("Authorization");
if (token == null) {                       // cross-cutting concern enforced once, at the edge
    send(ex, 401, "{"error":"unauthorized"}");
    return;
}
String backend = routes.entrySet().stream()
        .filter(e -> path.startsWith(e.getKey()))
        .map(Map.Entry::getValue).findFirst().orElse(null);
if (backend == null) { ex.sendResponseHeaders(404, -1); ex.close(); return; }
// forward with policy headers, relay the response
```

**Listing 1.** Verified on JDK 21 (G07_ApiGatewayHttp in empirics): a request without a token is rejected `401` at the gateway, `/orders/7` reaches its backend and returns the service's JSON with `X-Gateway` added, and unknown paths 404 — the client only ever sees the gateway (out/G07_ApiGatewayHttp.txt).

## Costs: the gateway is critical shared infrastructure

Everything depends on it, so its availability and latency budget are the system's: it must scale horizontally, have its own health checks, and fail safe (a routing-only fallback policy for degraded states). It can grow into a monolith of its own — Richardson's warning — when teams start adding experience-specific shaping, per-client business rules or orchestration logic; the discipline is: gateway = generic edge policy, BFF = per-experience backend, services = business logic. Change management matters too: route table changes are production changes and need review; and clients' view of the API is now coupled to the gateway's contract versioning ([[What changes are breaking for a REST API]] governs what can change without breaking them).

> [!warning] Direct service access does not disappear — it must be governed
> Even with a gateway, services remain reachable on the internal network; the gateway only protects the edge. Insider traffic, other services and workloads bypass it by design — which is why zero-trust setups add a mesh for east-west policy ([[How would you explain the service mesh pattern]]) and treat the gateway as the north-south edge, not the whole security story.

> [!tip] Interview answer
> The API gateway is the single entry point in front of the services: it routes by path to the owning service and enforces edge concerns once — auth, rate limiting, TLS — so clients never need to know the topology and services can move freely behind it. I keep it thin: routing and generic policy only; per-experience shaping belongs in BFFs and business logic in services. Its cost is being critical shared infrastructure — scale it, monitor it, and treat route changes as production changes.
