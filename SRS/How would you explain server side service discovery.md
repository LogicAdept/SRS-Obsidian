<!--
reps: 0
priority: 0
-->
#Patterns/Architecture/Microservices/ServiceDiscovery #SRS

# How would you explain server side service discovery

> [!abstract] Short answer
> In server-side service discovery the client calls one stable endpoint — a load balancer or router — and the platform resolves the logical service name to a live instance behind the scenes: lookup happens in the infrastructure, not in the client. The client needs no registry library and no balancing logic; the platform gains a choke point for policy and observability.

## The mechanics: one hop that hides everything

The consumer addresses the service by a fixed name (a load balancer's address, a DNS name, Kubernetes Service IP). The intermediary consults the registry — or the platform's own state — selects a healthy instance and forwards the request. All clients look identical regardless of language or vendor: no discovery SDK, no balancing policy to deploy, no caching discipline to implement. The intermediary is also the natural place for per-service policy: TLS termination, rate limits, metrics per backend, canary weights. Kubernetes' Service abstraction is the textbook instance — a virtual IP with kube-proxy or CNI doing the selection; classic cloud load balancers plus DNS are the same pattern; a service mesh's ingress is its evolution ([[How would you explain the service registry pattern]] underlies the resolution; [[What is the API gateway pattern in microservices]] sits a layer above, at the north-south edge).

```d2
direction: right
c: "Client
calls a stable name" {style.fill: "#eceff1"}
lb: "Load balancer / platform
lookup + select + forward" {style.fill: "#e3f2fd"}
reg: "Registry / platform state" {shape: cylinder; style.fill: "#fff3e0"}
i1: "orders #1" {style.fill: "#e8f5e9"}
i2: "orders #2" {style.fill: "#e8f5e9"}
c -> lb: 1. call 'orders'
lb -> reg: 2. resolve
lb -> i1: 3. forward
```

**Fig. 1.** The platform does the discovery hop: the client's contract is one stable endpoint.

## The trade versus client-side discovery

Advantages: zero client logic — the entire fleet, including uncooperative or legacy clients, gets uniform discovery and balancing; one place to evolve policy (per-instance health gating, zone-aware routing, gradual rollouts) without touching any client; and a single observable hop with per-backend metrics. Costs: the load balancer is now on the critical path of every call — it must scale horizontally, be redundantly deployed and add one network hop of latency; and per-request, per-client policies (sticky by user, caller-aware canary avoidance) are harder when the platform cannot see the request's business context. The mesh synthesizes the debate: sidecar proxies give every instance server-style discovery while keeping the "smart" logic declarative in a control plane ([[What is the Sidecar pattern]]; [[How would you explain the service mesh pattern]]). Richardson's guidance cuts across implementations: use server-side discovery as the default when a platform provides it (container orchestrators do), reach for client-side libraries when you need request-context-aware selection and cannot add proxy hops.

> [!warning] The balancing hop must not become a single point of failure or a hidden monolith
> The intermediary forwards every request, so its failure is everyone's failure — redundant deployment and health-checked scaling are prerequisites, not enhancements. And platform routers that grow routing logic per client ("special-case mobile here") accumulate exactly the coupling the pattern removed; policy belongs in declarative, versioned configuration — or in a BFF, not in the balancer's code.

> [!tip] Interview answer
> Server-side discovery hides the registry behind one stable endpoint: the client calls a load balancer or platform name, the platform resolves a healthy instance and forwards — clients need no libraries, every language behaves identically, and policy like canary weights or per-backend metrics lands in one place. I pay one extra hop and a redundantly deployed intermediary. On Kubernetes this is the default — Service and DNS are this pattern — and the mesh generalizes it per-instance.
