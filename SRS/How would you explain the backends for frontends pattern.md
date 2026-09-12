<!--
reps: 0
priority: 0
-->
#Patterns/Architecture/Microservices/ExternalAPI #Patterns/Architecture/UI #SRS

# How would you explain the backends for frontends pattern

> [!abstract] Short answer
> Backends for frontends (BFF) is an intermediate-tier pattern: for each user-facing experience — mobile app, web SPA, partner API — a separate, purpose-built backend sits between the clients and the fine-grained microservices, owning aggregation, translation and experience-specific concerns. Sam Newman introduced it after teams over-generalized a single API gateway into a kitchen sink.

## The problem it solves: one client, one shape does not fit

Behind an API gateway, the underlying services expose fine-grained resources. A mobile client needs few round trips and small payloads over a slow radio; a web SPA needs richer views; a partner needs stability and narrow fields. Making one backend serve all three produces either chatty, oversized responses for mobile or constant feature flags for the others. A BFF is owned by the team that owns the frontend it serves: it calls the relevant services, composes their responses ([[What is the API composition pattern in microservices]] is the underlying composition move), trims and reshapes payloads, and caches what that experience needs. The gateway stays thin — routing, TLS, authentication ([[What is the API gateway pattern in microservices]]); the BFFs carry experience logic.

```d2
direction: down
mobile: "Mobile app" {style.fill: "#e3f2fd"}
web: "Web SPA" {style.fill: "#e3f2fd"}
bff1: "Mobile BFF
small payloads, few calls" {style.fill: "#fff3e0"}
bff2: "Web BFF
rich views" {style.fill: "#fff3e0"}
orders: "Order service" {style.fill: "#e8f5e9"}
cust: "Customer service" {style.fill: "#e8f5e9"}
inv: "Inventory service" {style.fill: "#e8f5e9"}
mobile -> bff1
web -> bff2
bff1 -> orders
bff1 -> cust
bff2 -> orders
bff2 -> cust
bff2 -> inv
```

**Fig. 1.** One backend per experience; the underlying services are shared, the aggregation and shaping are not.

## Trade-offs and the failure mode

Benefits: each client gets an interface tuned to it; frontend teams deploy their BFF independently — Newman's original motivation was ownership, not traffic shape; mobile-specific optimizations (response trimming, request batching) stop leaking into other clients. Costs: more deployables and duplicated glue; a bad team split recreates a mini-monolith inside each BFF if it starts owning business rules. The known failure mode is BFF proliferation — one per screen or per release instead of one per experience — and business logic sneaking in: the BFF orchestrates calls and shapes data, it must not enforce invariants, which stay in the owning services ([[What is a saga and how would you explain one with a real-world example]] covers cross-service business processes). For read-heavy aggregation with many clients, a GraphQL gateway is a related evolution ([[What is GraphQL]] covers the query language).

> [!warning] A BFF is not a API-gateway replacement
> The gateway is infrastructure: cross-cutting, generic, no knowledge of experiences. The BFF is product code: full of knowledge of one experience. Fusing them — routing plus per-experience shaping in one component — couples every team's release to the edge component, which is exactly the bottleneck BFFs exist to remove.

> [!tip] Interview answer
> BFF means one backend per frontend experience — a mobile BFF, a web BFF — owned by the frontend team, sitting between the clients and the microservices. It aggregates and reshapes service responses for that experience's needs and deploys independently. The gateway stays a thin cross-cutting router; the BFF holds experience logic, not business invariants.
