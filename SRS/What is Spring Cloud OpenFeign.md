<!--
reps: 0
priority: 0
-->
#Java/Spring/Cloud #SRS

# What is Spring Cloud OpenFeign?

> [!abstract] Short answer
> **Spring Cloud OpenFeign** is a **declarative HTTP client**: you write an **interface**, annotate it with `@FeignClient` and Spring MVC (or Feign / JAX-RS) mappings, and the runtime supplies the call. The starter is `spring-cloud-starter-openfeign`. Turn clients on with `@EnableFeignClients`. Spring Cloud wires the same `HttpMessageConverters` as Spring Web, plus **LoadBalancer** (logical service name), optional **CircuitBreaker**, and Eureka when those are on the classpath. It is **not** Spring MVC itself and **not** `RestClient` — that is a separate Framework client you can also load-balance.

## Interface becomes a client

`@FeignClient("stores")` names a LoadBalancer client. The string is a **service id** unless you set `url` to a concrete host. Discovery (for example Eureka) or `SimpleDiscoveryClient` supplies instances. Each named client gets its own child context (`FeignClientsConfiguration`: encoder, decoder, `Contract`). Override with `@FeignClient(configuration = …)` or `contextId`. The bean name is the interface’s fully qualified name unless you set `qualifiers` ([[How do you achieve server-side load balancing with Spring Cloud]], [[What is Spring Cloud]]).

```java
@SpringBootApplication
@EnableFeignClients
public class Application {

	public static void main(String[] args) {
		SpringApplication.run(Application.class, args);
	}
}

@FeignClient("stores")
public interface StoreClient {

	@GetMapping("/stores")
	List<Store> getStores();

	@PostMapping(value = "/stores/{storeId}", consumes = "application/json")
	Store update(@PathVariable("storeId") Long storeId, Store store);
}
```

**Listing 1.** Conceptual. MVC mappings on a Feign interface; `"stores"` is the load-balanced name.

On `@Configuration` classes, `@EnableFeignClients` must name packages or `clients=…`. Do not declare Feign clients inside `FactoryBean` types (they force a context refresh too early). As of OpenFeign **4.x**, `@FeignClient` attributes resolve **eagerly** (AOT); set `spring.cloud.openfeign.lazy-attributes-resolution=true` when you need lazy resolution (Spring Cloud Contract tests).

```d2
direction: down
iface: "@FeignClient(\"stores\")\nStoreClient" {
  width: 240
  height: 50
  style.fill: "#e3f2fd"
}
lb: "Spring Cloud LoadBalancer" {
  width: 220
  height: 40
  style.fill: "#fff3e0"
}
cb: "CircuitBreaker\n(optional)" {
  width: 200
  height: 40
  style.fill: "#fce4ec"
}
http: "stores instances" {
  width: 180
  height: 40
  style.fill: "#e8f5e9"
}
iface -> lb
iface -> cb
lb -> http
```

**Fig. 1.** Feign is the declaration; LoadBalancer picks an instance; CircuitBreaker wraps methods only when enabled.

## Timeouts, retries, circuit breaker

Two timeouts: **connect** (avoid blocking on a hung handshake / connect) and **read** (after the connection exists). Circuit breaking is **not** on by default: classpath **and** `spring.cloud.openfeign.circuitbreaker.enabled=true`. Then every method is wrapped. Fallbacks: `@FeignClient(fallback = …)` or `fallbackFactory`; the fallback type must be a **Spring bean**. Feign clients are marked `@Primary` so injection still works when fallback beans share the interface — set `primary=false` if that fights your context ([[How would you explain Circuit Breaker]]).

> [!warning] Spring Cloud disables Feign retries by default
> A `Retryer.NEVER_RETRY` bean is registered. That is **not** vanilla OpenFeign, which retries some I/O and `RetryableException`s. If you expect retries, you must replace the `Retryer`. Timeouts still apply either way.

> [!warning] `@EnableFeignClients` on `@Configuration` without a scan
> Clients in other packages are silent. Pass `basePackages` or `clients`. Multi-module builds have the same trap.

> [!tip] Interview answer
> OpenFeign is an annotated interface that becomes a load-balanced HTTP client, using MVC mappings and Web converters. Enable it with `@EnableFeignClients`. Circuit breakers and retries are extra: CB via `spring.cloud.openfeign.circuitbreaker.enabled`, retries off unless you provide a `Retryer`. `RestClient` is Framework’s fluent client, not a Feign synonym.
