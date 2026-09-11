<!--
reps: 0
priority: 0
-->
#Patterns/Architecture/Microservices/ServiceDiscovery #SRS

# How would you explain the service registry pattern

> [!abstract] Short answer
> The service registry is a database of available service instances: each entry maps a service's logical name to its network locations (host, port, metadata), is kept current by registration and heartbeats, and is consulted by clients or load balancers before every call. It is the DNS-plus-liveness backbone that makes microservice topology dynamic — instances appear, die and scale without manual address management.

## Mechanics: registration, liveness, lookup

Three moving parts define the pattern. Registration: an instance's location enters the registry — either by the instance itself ([[How would you explain self registration with a service registry]]) or by a deployment-platform registrar ([[What is the third-party registration pattern in microservices]]). Liveness: entries carry leases or heartbeats; a silent instance is expired and stops being returned — the registry must answer with live addresses, not historical ones. Lookup: a consumer queries by logical service name and picks an instance (client-side load balancing), or a server-side intermediary does it on the caller's behalf ([[How would you explain server side service discovery]] contrasts the two). Real registries add metadata (zone, version, tags) for topology-aware routing and gradual rollouts; they also must be highly available themselves — a registry outage must not take the whole system down, which is why clients cache entries and degrade to last-known-good ([[What is the health check API pattern]] feeds the registry the deep health signal beyond heartbeat liveness).

```d2
direction: down
i1: "orders @ 10.0.0.1:8081" {style.fill: "#e8f5e9"}
i2: "orders @ 10.0.0.2:8082" {style.fill: "#e8f5e9"}
reg: "Service registry
name -> live instances
lease + heartbeat" {shape: cylinder; style.fill: "#fff3e0"}
c: "Client
lookup 'orders'" {style.fill: "#eceff1"}
i1 -> reg: heartbeat
i2 -> reg: heartbeat (or silence)
c -> reg: lookup
reg -> c: live list
```

**Fig. 1.** The registry is the live map: instances keep their entries warm, clients resolve by name at call time.

## The property that decides registry design: consistency versus availability

The CAP tension is acute here, and mainstream choices split on it. Eureka (AP): prefer serving a possibly stale list over refusing to answer — clients keep calling; dead instances are weeded out by lease expiry; in extreme cases Eureka's self-preservation mode stops expiring entries to survive a network partition (trading accuracy for availability). Consul (CP-ish): stronger consistency for critical lookups, with health checks driving availability. ZooKeeper-based setups historically pushed consistency harder. The operational rule that matters more than the product choice: the registry is infrastructure with its own failure modes, so its consumers must be written against partial truth — cached registrations, bounded staleness, and the assumption that any resolved instance may be dead by the time it's called (hence per-call timeouts and breakers, [[How would you explain Circuit Breaker]]). In container platforms the registry often blurs into the platform itself: Kubernetes' Service abstraction is effectively registry plus server-side discovery plus DNS.

> [!warning] A registry is a cache of truth, not the truth
> Entries can be stale in both directions: a dead instance still listed (until lease expiry) and a live instance not yet visible (registration lag). Design consumers for it: do not treat lookup failure as service absence, do not treat lookup success as a guarantee, and always pair the registry with per-call resilience policy. The night the registry itself flaps, cached last-known-good lists are what keep the system serving.

> [!tip] Interview answer
> The service registry is the live map of instances: services register their locations (themselves or via their platform), keep entries warm with heartbeats or leases, and clients or load balancers resolve a logical name to live instances per call. The design crux is CAP — Eureka-style registries prefer stale-but-available lists, and consumers must handle partial truth with caching, timeouts and breakers. On Kubernetes, the platform's Service+DNS is this pattern built in.
