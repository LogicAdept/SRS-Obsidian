<!--
reps: 0
priority: 0
-->
#Patterns/Architecture/Microservices/Deployment #SRS

# How would you explain multiple services per host deployment

> [!abstract] Short answer
> Multiple-services-per-host packs several service instances (often different services) onto one shared host: utilization is high and the operational footprint small, but isolation is weak — the services contend for the same CPU, memory, ports and runtime, and one misbehaving service degrades its neighbors. Richardson's ladder puts it at the low-isolation, high-utilization end.

## The mechanics and the sharing costs

One host runs a stack of service processes. The gains are real: fewer hosts to provision and patch, dense utilization, and a simple story for small fleets (one big VM, several processes, one supervisor). The costs all come from the sharing. Resource contention: services without enforced CPU/memory ceilings bleed into each other — a memory leak in one service OOMs whichever neighbor the kernel picks; CPU saturation in one inflates everyone's latency. Port and dependency management: fixed ports must be allocated per service on the host; conflicting runtime or library versions are a manual packing puzzle. Security: all services share the host's filesystem and user context unless extra partitioning is added. Failure isolation: a crash is contained per process, but resource failures propagate. Monitoring per service requires per-process discipline ([[What is the application metrics pattern in microservices]] explains the tagging workload this creates).

```d2
direction: down
host: "One host" {style.fill: "#eceff1"}
s1: "orders
2 GB / 1 cpu" {style.fill: "#e8f5e9"}
s2: "inventory
leaking..." {style.fill: "#ef9a9a"}
s3: "search
starved" {style.fill: "#fff3e0"}
host -> s1
host -> s2
host -> s3
note: "No enforced ceilings: leak in inventory
takes search and orders down" {style.fill: "#ffebee"}
s2 -> note
```

**Fig. 1.** Dense packing without resource ceilings: one service's failure mode becomes every service's outage.

## The modern position of the pattern

As a deliberate architecture, multiple-services-per-host is mostly a transitional or small-scale choice: the standard answer to its weaknesses is the container — service-per-container keeps the density while adding per-process resource ceilings, filesystem isolation and image-level dependency pinning ([[What is the service per container pattern]] is the direct successor; the JVM variant of the same idea is multiple application instances in one process, Richardson's "multiple service instances per process" — same contention trade, even denser). The pattern stays reasonable for: internal tools with tiny footprints, single-team systems where the host is effectively owned by one team (which removes the security and contention blast radius between owners), and environments where container platforms are not yet available. Where it is used, per-service cgroups or equivalent resource controls and per-service log separation are the minimum hygiene ([[How would you explain single service per host deployment]] is the high-isolation opposite end of the same ladder).

> [!warning] Density hides coupling, until the night it doesn't
> The pattern's apparent simplicity — everything on one box — is operational coupling: any change that affects the host (OS patch, runtime upgrade, security hardening) affects every service at once, and any service's capacity growth needs a conversation with every neighbor. If two services share a host because "it was convenient", they share its failure modes too.

> [!tip] Interview answer
> Multiple-services-per-host trades isolation for density: fewer hosts to manage, great utilization, but services contend for CPU, memory, ports and runtimes — one leaking service can starve its neighbors and patching the host is a fleet-wide event. I see it as a small-fleet or transitional rung; containers give the same density with enforced ceilings, which is why service-per-container replaced it.
