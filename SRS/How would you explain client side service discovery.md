<!--
reps: 0
priority: 0
-->
#Patterns/Architecture/Microservices/ServiceDiscovery #SystemDesign/Microservices #DistributedSystems #SRS

# How would you explain client side service discovery

> [!abstract] Short answer
> In client-side service discovery, the calling service queries a service registry itself, picks one healthy instance (client-side load balancing), and calls it directly — no intermediate load balancer hop. The registry (Eureka, Consul, etcd) holds the live instance list, populated by self-registration or third-party registration. The alternative is server-side discovery, where the client calls a stable endpoint (DNS/LB/gateway) that resolves instances for it.

## The mechanics: registry, lookup, client-side balancing

Three moving parts. Registration: an instance of, say, the pricing service starts and registers its address, port and health metadata in the registry — self-registration on startup plus deregistration/heartbeat on shutdown and death (the registry evicts instances that stop heartbeating; a failed health check must also mark the instance unavailable — the same liveness logic as [[How would you explain Health checks]]). Lookup: the consumer asks the registry for the service's instances (or subscribes and caches the list locally, polling or watching for changes — network round trips per call would recreate the bottleneck discovery exists to remove). Client-side load balancing: the consumer's client library (Netflix Ribbon, Spring Cloud LoadBalancer, gRPC's client LB) picks an instance by its own policy — round-robin, least-loaded, zone-aware — and calls it directly. Microservices.io's writeup frames the benefit exactly: this removes the extra network hop of a central LB and makes per-client balancing policies (zone preference, retries on another instance) natural; the costs are client coupling (every language needs a registry client) and registry availability becoming critical — mitigated by client-side caching so consumers ride out registry blips.

```d2
direction: right
registry: {
  label: "service registry (Eureka/Consul)\npricing: ip1, ip2, ip3"
  width: 250
  height: 80
}
consumer: {label: "consumer\nclient-side LB (Ribbon)"; width: 200; height: 70}
p1: {label: "pricing-1"; width: 110; height: 50}
p2: {label: "pricing-2"; width: 110; height: 50}
consumer -> registry: "lookup / watch (cached locally)"
registry -> consumer: "instance list"
consumer -> p1: "direct call (chosen by LB policy)"
p2 -> registry: "register + heartbeat"
```

**Fig. 1.** The consumer resolves and balances itself against the registry's list.

## Client-side versus server-side, and the platform shift

Server-side discovery inverts the flow: the client calls one stable address — a load balancer, API gateway, or DNS — which resolves instances (via the same registry) and forwards; the client stays dumb, but every request pays the extra hop and the LB is shared infrastructure to scale and own. Kubernetes pushes a third model into the platform: services get cluster DNS and kube-proxy routes to pods — server-side discovery as infrastructure, invisible to application code, which is why modern stacks often need no Eureka at all. The choice criteria: client-side wins on latency (no hop), smart per-client policies and avoiding a scaling bottleneck; it costs library coupling across languages and more client complexity. Server-side wins on simplicity and heterogeneity; it costs the hop and central infrastructure. Either way the registry pattern underlies it — [[How would you explain Health checks]] and [[How would you explain Connection draining]] determine when instances enter and leave the registry's list, and the resilience wrappers ([[How would you explain Circuit Breaker]]-style clients) decide what happens when a chosen instance misbehaves. [[What is the difference between a stateful service and a stateless service]] is the precondition: discovery only works because instances are interchangeable.

> [!warning] Discovery without health semantics routes to corpses
> A registry list is only as good as its eviction: an instance that crashed without deregistering stays in the list until heartbeats lapse, and clients keep choosing it. Registry TTLs, heartbeats and health-gated registration are load-bearing — a stale list is worse than no discovery because it fails selectively.

> [!tip] Interview answer
> Client-side discovery has the consumer query a registry (Eureka/Consul), cache the instance list, and load-balance in its own client library — no extra hop, and per-client policies like zone preference. Server-side discovery hides this behind an LB/gateway or k8s DNS at the cost of the hop. Either way, registration, heartbeats and health gating keep the list honest.
