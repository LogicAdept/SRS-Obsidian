<!--
reps: 0
priority: 0
-->
#Java/Spring/Cloud #SRS

# What is Spring Cloud?

> [!abstract] Short answer
> **Spring Cloud** is a **set of libraries** (a **release train** of versioned projects) on top of **Spring Boot** for **common distributed-system patterns**: versioned configuration, service registration and discovery, routing, service-to-service calls, load balancing, circuit breakers, and distributed messaging. It is **not** a short-lived batch framework and **not** “integration with external systems” as a one-line identity. You stand up those patterns locally, on bare metal, or on a platform such as Cloud Foundry.

## What the train is

The Spring Cloud **train** (example: **2025.0**, Boot **3.5.x**) bundles compatible project versions: Config, Gateway, OpenFeign, LoadBalancer / Commons, CircuitBreaker, Stream, Bus, Contract, Kubernetes, Consul, Netflix, Vault, Function, Task, and others. You pick the starters you need; Cloud is not one JAR ([[What is Spring Cloud Config]], [[What is Spring Cloud Gateway]], [[What is Spring Cloud OpenFeign]]).

Official feature list for typical use cases (with an extensibility hook for the rest):

- Distributed / versioned configuration
- Service registration and discovery
- Routing
- Service-to-service calls
- Load balancing
- Circuit breakers
- Distributed messaging

```d2
direction: down
boot: "Spring Boot application" {
  width: 220
  height: 45
  style.fill: "#e8f5e9"
}
cloud: "Spring Cloud train\nConfig · discovery · Gateway · Feign · CB · Stream" {
  width: 340
  height: 55
  style.fill: "#e3f2fd"
}
dist: "Distributed runtime\nlaptop · datacenter · Cloud Foundry / k8s" {
  width: 320
  height: 50
  style.fill: "#fff3e0"
}
boot -> cloud
cloud -> dist
```

**Fig. 1.** Cloud adds distributed patterns on Boot; the same app is meant to run in more than one environment.

Spring Cloud **Commons** / **Context** supply shared pieces (abstractions, refresh scope, bootstrap-era environment). Concrete discovery can be Consul, Kubernetes, Netflix, Zookeeper — the train still **includes** `spring-cloud-netflix`; treat interview “Netflix OSS is dead” as a product-history question, not as “the train dropped Netflix” ([[How do you achieve server-side load balancing with Spring Cloud]], [[What is Spring Cloud Stream used for with RabbitMQ]]).

```xml
<dependency>
	<groupId>org.springframework.cloud</groupId>
	<artifactId>spring-cloud-starter-gateway</artifactId>
</dependency>
```

**Listing 1.** Conceptual. One Cloud starter; BOM / train manages the version.

> [!warning] Not Spring Batch and not “finite data”
> Cloud is **not** a short-lived job runner. **Spring Cloud Task** / **Stream** are train members for finite or messaging workloads; they do not define the whole project. “Integrates with external systems” is true of half the JVM — too vague for an identity.

> [!tip] Interview answer
> Spring Cloud is a Boot-aligned release train for distributed patterns: config, discovery, routing, client calls, load balancing, circuit breaking, messaging. Gateway, Config, OpenFeign, CircuitBreaker, and Stream are the names that still show up; it is a toolbox, not a single runtime.
