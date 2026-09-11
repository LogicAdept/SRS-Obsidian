<!--
reps: 0
priority: 0
-->
#Patterns/Architecture/Microservices/Deployment #DevOps/Tools/Docker #DevOps/Containerisation #SRS

# What is the service per container pattern

> [!abstract] Short answer
> Service-per-container runs each service instance in its own container on a shared host: the container pins the service's dependencies and image, enforces CPU/memory ceilings and isolates the filesystem, while the host (or orchestrator) packs many containers for density. Richardson's catalog treats it as the modern default between host-sharing schemes and serverless deployment.

## What the container actually buys per service

Four concrete properties, per instance. Immutable artifact: the image contains the service plus its pinned runtime and libraries — the same bytes promoted across environments ([[What is the externalized configuration pattern for microservices]] keeps environment values out of the image). Resource isolation: CPU and memory limits are enforced by the platform, so a noisy neighbor degrades to its own ceiling instead of starving the host ([[How would you explain multiple services per host deployment]]'s core defect, fixed). Dependency isolation: conflicting runtime versions coexist on one host without packing puzzles. Fast, uniform operations: start/stop/replace is one command shape for every service, which is what orchestrators and autoscalers automate — and why this pattern is the substrate of Kubernetes-style platforms ([[What is the health check API pattern]] is how the platform learns which containers actually work; [[How would you explain the service registry pattern]] is how they get found).

```d2
direction: down
host: "Orchestrator host" {style.fill: "#eceff1"}
c1: "orders:2.4.1
limits: 1 cpu / 2 GB" {style.fill: "#e8f5e9"}
c2: "inventory:1.0.0
limits: 0.5 cpu / 1 GB" {style.fill: "#e8f5e9"}
c3: "search:5.2.0
limits: 2 cpu / 4 GB" {style.fill: "#e8f5e9"}
host -> c1
host -> c2
host -> c3
```

**Fig. 1.** Density with ceilings: pinned images, enforced limits, one lifecycle verb for every service.

## The trade-offs and the lifecycle discipline it demands

Costs: containers are processes with walls, not VMs — kernel is shared, isolation is weaker than hardware virtualization (security-sensitive neighbors may still need VM-per-service); the image layer adds a build pipeline obligation (rebuilds on every base-image CVE — a fleet-wide chore); and the platform itself (orchestrator, registry, ingress) is a new subsystem to operate. The operational pattern that makes it work: instances are cattle — replace, don't repair; every instance must therefore be stateless or have its state externalized (database, events), must be health-checkable, must log to stdout/stderr for collection ([[What is the log aggregation pattern in microservices]]), and must register or be registered for discovery. Richardson's ladder beyond this rung: service-per-VM when stronger isolation or licensing demands it, and serverless deployment when the service's load profile is bursty enough to justify handing scaling entirely to the platform ([[How would you explain single service per host deployment]] is the ladder's history; the chassis plus container is the canonical modern pairing).

> [!warning] A container is not a mini-VM
> Teams that treat containers as VMs get bitten twice: in security (shared kernel means container escapes are host escapes — the threat model is different) and in data (a container's writable layer is disposable by design — anything stored there is lost on replace). The architecture only works if every instance can be killed at any moment without data loss; that invariant must be designed, not assumed.

> [!tip] Interview answer
> Service-per-container gives each instance its own image — pinned dependencies, promoted unchanged across environments — plus enforced resource limits and filesystem isolation, while the host packs many containers for density. It works because instances are cattle: stateless or externalized state, health-checked, logging to stdout, registered for discovery. Costs are the image pipeline and the orchestrator platform; isolation is process-level, so security-critical neighbors may still want VMs.
