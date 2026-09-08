<!--
reps: 0
priority: 0
-->
#Java/Spring/Cloud #SRS

# How do you achieve server-side load balancing with Spring Cloud?

> [!abstract] Short answer
> **Spring Cloud LoadBalancer is client-side.** The caller (or the **gateway**) picks an instance from discovery. The Spring Cloud **edge** answer for “one entry, many instances” is **Spring Cloud Gateway** with a `lb://serviceId` URI (needs `spring-cloud-starter-loadbalancer` on the gateway classpath). That is load balancing **in front of** the service, not Ribbon and not Netflix Zuul. Service-to-service calls use the same LoadBalancer from the **client** (`@LoadBalanced` `RestClient` / `WebClient`, or OpenFeign). A Kubernetes **Service** is cluster DNS/LB **outside** the train.

## Edge vs caller

Gateway resolves `lb://catalog` with `LoadBalancerClient` / the reactive load-balancer filter and replaces the URI with a host and port. Discovery-based routes (`spring.cloud.gateway.discovery.locator.enabled=true` plus a `DiscoveryClient`) default to `'lb://'+serviceId`. From a browser that looks like **server-side** routing; inside Gateway it is still the **LoadBalancer client** ([[What is Spring Cloud Gateway]], [[What is Spring Cloud]]).

Callers that are **not** a gateway annotate a `RestClient.Builder` or `WebClient.Builder` with `@LoadBalanced` and call a **logical** hostname (`http://stores/...`). OpenFeign’s `@FeignClient("stores")` builds a LoadBalancer client for that name ([[What is Spring Cloud OpenFeign]]). Default algorithm is **round-robin** (`RoundRobinLoadBalancer`); switch per client with `@LoadBalancerClient` (for example `RandomLoadBalancer`).

```yaml
spring:
  cloud:
    gateway:
      routes:
        - id: catalog
          uri: lb://catalog-service
          predicates:
            - Path=/catalog/**
```

**Listing 1.** Conceptual. Gateway route; `lb://` is the load-balancer filter, not a literal host.

```java
@Configuration
public class StoreClients {

	@Bean
	@LoadBalanced
	RestClient.Builder loadBalancedRestClientBuilder() {
		return RestClient.builder();
	}
}
```

**Listing 2.** Conceptual. Client-side LoadBalancer on `RestClient`; URI host is a **service id**.

```d2
direction: down
ui: "Browser / mobile" {
  width: 180
  height: 40
  style.fill: "#fff3e0"
}
gw: "Gateway\nlb://catalog-service" {
  width: 220
  height: 50
  style.fill: "#e3f2fd"
}
svc: "catalog instances\nA · B · C" {
  width: 220
  height: 50
  style.fill: "#e8f5e9"
}
peer: "Other Boot app\n@LoadBalanced RestClient" {
  width: 240
  height: 50
  style.fill: "#fce4ec"
}
ui -> gw
gw -> svc
peer -> svc
```

**Fig. 1.** Gateway is the edge picker; peer services pick themselves. Both use LoadBalancer + discovery.

Ribbon is **not** the current Commons implementation. Health-check suppliers, retries, and circuit breakers are **separate** knobs (LoadBalancer health-check / retry, Spring Cloud CircuitBreaker) — not one Zuul pipeline.

> [!warning] Do not put `@LoadBalanced` on Gateway’s proxy client
> Gateway MVC owns an internal `RestClient` for proxying. Annotating that (or a custom `@LoadBalanced RestClient.Builder` in the **same** gateway context) can resolve the target **before** `lb://` runs and fail with `Service Instance cannot be null`. Use `lb://` / `lb()` on **routes**; use `@LoadBalanced` only on clients **your** code calls.

> [!warning] Zuul is not the 2025 train answer
> Older Netflix wording called Zuul a JVM router / server-side load balancer. Current Cloud routing is **Gateway**. Netflix remains **on the train**; that does not mean Zuul 1 is how you load-balance today.

> [!tip] Interview answer
> Say “client-side LoadBalancer, Gateway at the edge with `lb://`.” Zuul and Ribbon are history. Kubernetes Service is infrastructure LB, not a Spring Cloud starter. Round-robin is the default picker; circuit breaking is a different project.
