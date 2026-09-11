<!--
reps: 0
priority: 0
-->
#Patterns/Architecture/Microservices/ServiceDiscovery #SRS

# How would you explain self registration with a service registry

> [!abstract] Short answer
> Self registration is the style where a service instance registers itself with the service registry: on startup it writes its location and metadata, while running it keeps the entry alive with heartbeats, and on clean shutdown it deregisters. The instance owns the registry interaction — the contrast is third-party registration, where the deployment platform registers on the instance's behalf ([[How would you explain the service registry pattern]] defines the registry both feed).

## The lifecycle the instance implements

Four steps are the instance's responsibility. Register on boot: after the app is ready to serve, it puts its entry into the registry — logical service name, host, port, and metadata (zone, version, health URL). Heartbeat while alive: the client renews the entry periodically (Eureka's default renewal every 30 seconds); the registry expires entries whose renewals stop — the lease is the liveness backstop. Deregister on shutdown: a clean stop removes the entry so traffic stops flowing immediately instead of waiting for lease expiry. React to health: a self-degrading instance flips its status to DOWN or OUT_OF_SERVICE so the registry stops routing to it even before death ([[What is the health check API pattern]] supplies the deep health signal the entry points to). Netflix Eureka is Richardson's canonical example — its Java client wraps exactly this loop; Spring Cloud packages it ([[What is Spring Cloud]]).

```d2
direction: right
app: "Service instance" {style.fill: "#e8f5e9"}
reg: "Registry" {shape: cylinder; style.fill: "#fff3e0"}
c: "Consumers
lookup 'orders'" {style.fill: "#eceff1"}
app -> reg: 1. register on boot
app -> reg: 2. heartbeat every 30s
app -> reg: 3. deregister on shutdown
c -> reg: 4. lookup
```

**Fig. 1.** The instance runs the whole registry conversation itself; consumers read whatever the instance has kept alive.

## What the style buys — and what it costs

Benefits: no extra infrastructure component — the instance is the only actor, so plain-VM deployments work with nothing but the client library; registration timing can be precise (the instance registers only when it is genuinely ready to serve, which a platform registrar may approximate); and shutdown deregistration is immediate. Costs: every language and framework in the fleet needs a registry client (the polyglot tax, shared with client-side discovery [[How would you explain client side service discovery]]); the instance holds registry credentials — a compromise of the instance is a compromise of the registry's namespace; and app-level bugs leak into topology — a version that forgets to deregister, or double-registers after a restart, pollutes the list until leases expire. These costs are exactly what third-party registration removes ([[What is the third-party registration pattern in microservices]]): the registrar centralizes the logic, kills the credential sprawl, and cannot forget to deregister — at the price of one more platform component whose own availability becomes load-bearing. The usual decision rule: self registration where no platform component is positioned to own instance lifecycle; third-party wherever an orchestrator already knows when instances start and die.

> [!warning] The crash path is the style's blind spot
> Everything the instance does is voluntary — and a SIGKILL does none of it. A crashed instance's entry stays in the registry until the lease expires, so consumers keep choosing a corpse for up to a full lease window. Self registration therefore only works with TTL-based eviction as the backstop, short enough for your recovery goals, and with consumer-side timeouts and retries ([[How would you explain Circuit Breaker]]) for the window it exists.

> [!tip] Interview answer
> Self registration means the instance manages its own registry entry: register when ready to serve, heartbeat to renew the lease, deregister on clean shutdown, and report degraded health through its status. It needs no extra infrastructure and gets registration timing right, but every language needs the client, instances hold registry credentials, and a crashed instance leaves a stale entry until the lease expires — which is why TTL eviction plus consumer-side resilience are mandatory, and why platform-based third-party registration often replaces it.
