<!--
reps: 0
priority: 0
-->
#Patterns/Architecture/Microservices/Deployment #SRS

# What is the service deployment platform pattern

> [!abstract] Short answer
> Service deployment platform: use automated infrastructure - Kubernetes, Docker Swarm, a PaaS like Cloud Foundry or AWS Elastic Beanstalk, or a serverless platform - that abstracts deployed services as named, load-balanced, highly available sets of instances. The pattern says: do not hand-manage hosts and processes; give the platform the service image and the desired instance count, and let it place, restart, discover and scale instances for you.

## Mechanism: the service abstraction

The platform's contract is a service abstraction: you register a named service backed by an image and a replica count; the platform runs that many instances across the cluster, load-balances traffic over the healthy ones, restarts failed ones, and exposes the name as the stable address. The concrete examples: Docker orchestration frameworks - Kubernetes and Swarm mode; serverless platforms - AWS Lambda; PaaS - Cloud Foundry and Elastic Beanstalk. All four deliver the same abstraction at different rigidity levels. What you hand over versus what you keep is the pattern's essence: you keep the service artifact and its configuration; the platform owns placement, health management, discovery and scaling. Two pieces of the related-patterns note are interview gold: deployment platforms typically provide a service registry and server-side discovery as built-ins, and internally they may implement a service using containers or VMs - Kubernetes is explicitly container-based, while the platform choice hides that from the service's perspective ([[How does service discovery work in Kubernetes]] shows the discovery built-in; [[How would you explain server side service discovery]] is the general pattern behind it).

```d2
direction: right
dev: "Developer
image + desired replicas" {style.fill: "#e8f5e9"}
plat: "Deployment platform
Kubernetes / Swarm / PaaS" {style.fill: "#fff3e0"}
i1: "instance 1" {style.fill: "#e8f5e9"}
i2: "instance 2" {style.fill: "#e8f5e9"}
i3: "instance 3 (crashed, restarting)" {style.fill: "#ffcdd2"}
lb: "named service
load-balanced VIP/DNS" {style.fill: "#ffe0b2"}
dev -> plat: declare
plat -> i1
plat -> i2
plat -> i3
i1 -> lb
i2 -> lb
lb -> dev: stable address
```

**Fig. 1.** The developer declares an image and a replica count; the platform maintains the named, load-balanced service through instance crashes and rescheduling.

## Why it matters and what it hides

Without a platform, every team re-solves the same problems: writing init scripts, wiring load balancers, health-checking processes, scaling by hand. With one, deployment converges on a declarative contract and the operational mechanics are shared and tested. The platform also standardizes the deployment patterns beneath - it decides that services run per-container or per-VM, implements single- or multiple-instances-per-host scheduling, and integrates health checks so rolling updates only shift traffic to instances that pass readiness ([[What is the health check API pattern]] is the service-side half of that contract). The cost side is the flip of the benefit: running a Kubernetes cluster well is itself an engineering discipline, and platform APIs creep into service manifests and configurations - migration between platforms is a refactor, not a checkbox. That is why serverless is a platform flavor and why the interview answer should place all of the deployment patterns (per-VM, per-container, multiple-per-host, serverless) as choices beneath this one abstraction.

> [!warning] A platform is not an ops department substitute
> The trap is treating the platform as magic: it restarts crashed containers, but it cannot fix an unready endpoint, a missing health check, a memory leak that OOM-kills pods in a loop, or an application that ignores SIGTERM and drops in-flight requests on every rolling deploy. Platform adoption still demands readiness probes, graceful shutdown and resource requests that match reality. Second trap: cluster sprawl - every team running its own bespoke Kubernetes with its own add-ons rebuilds the operational silo the platform was meant to remove.

> [!tip] Interview answer
> A service deployment platform - Kubernetes, Swarm, Cloud Foundry, Lambda - gives every service the same abstraction: declare an image and replica count, get a named, load-balanced, self-healing set of instances with discovery built in. It standardizes placement, health management and scaling that teams would otherwise hand-roll. I still owe the platform readiness probes, graceful shutdown and honest resource settings - it automates operations, it does not replace them.
