<!--
reps: 0
priority: 0
-->
#Patterns/Architecture/Microservices/Deployment #SRS

# How would you explain single service per host deployment

> [!abstract] Short answer
> Single-service-per-host deploys one service instance per host (VM or bare server): isolation is strong — the instance owns the host's resources, no noisy neighbors — but resource utilization is low and the fleet of hosts becomes large to patch and manage. Richardson's deployment-pattern ladder places it between multiple-services-per-host and service-per-container/VM.

## The mechanics and the real trade

One host runs one service instance: the instance can use the whole machine's memory and CPU, and its resource ceiling is visible and predictable — capacity planning per service is straightforward. Dependencies are host-global (language runtime, native libraries), which is both the pattern's simplicity and its limit: two services needing conflicting runtimes need separate hosts, and upgrading the host's stack is a fleet-wide task. From the operations side, the cost is arithmetic: N services times R replicas equals N times R hosts to provision, patch, monitor and pay for — plus dead capacity whenever a service underuses its dedicated machine. Richardson's forces table makes the comparison concrete against [[How would you explain multiple services per host deployment]] (better utilization, worse isolation) and [[What is the service per container pattern]] (isolation without the fleet overhead).

```d2
direction: right
h1: "Host 1
orders #1" {style.fill: "#e8f5e9"}
h2: "Host 2
orders #2" {style.fill: "#e8f5e9"}
h3: "Host 3
inventory #1" {style.fill: "#eceff1"}
h4: "Host 4
idle capacity" {style.fill: "#ef9a9a"}
cap: "Cost: 4 hosts for 3 instances" {style.fill: "#fff3e0"}
h1 -> cap
h3 -> cap
h4 -> cap
```

**Fig. 1.** Strong isolation has a price in host count: underused machines are the pattern's signature waste.

## Where it still earns its keep

The pattern remains reasonable when: a service is resource-hungry and its performance profile demands dedicated hardware (JVM heaps, database-adjacent services); compliance or licensing requires hard host boundaries; or the organization's tooling maturity is low — one instance per host is the easiest deployment story to reason about, with logs, metrics and process supervision host-local and unambiguous. The modern successor that keeps the isolation semantics without the host-count cost is service-per-container: the container isolates dependencies and resource ceilings while the host runs many containers — which is why Richardson frames single-service-per-host mostly as the step on the ladder toward containerized deployment ([[What is the externalized configuration pattern for microservices]] and the chassis make those instances environment-agnostic, which is what makes host elasticity possible).

> [!warning] "One instance per host" still needs the instance management layer
> The pattern solves placement, not lifecycle: who restarts the instance after a crash, how new versions roll out, how health gates routing ([[What is the health check API pattern]]), how configuration reaches the new host. Without an orchestrator or deployment platform answering those, the pattern degrades into hand-managed pets — a fleet of them.

> [!tip] Interview answer
> Single-service-per-host gives one service instance the whole host: predictable resources, no noisy neighbors, dead-simple operations story — at the cost of poor utilization and a large fleet to patch. I treat it as the classic rung before containers: right for resource-hungry or compliance-bound services, otherwise service-per-container delivers the same isolation with shared hosts.
