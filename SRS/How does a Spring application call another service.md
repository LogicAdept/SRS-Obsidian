<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebMvc #Java/Spring/Framework/WebFlux #SRS

# How does a Spring application call another service?

> [!abstract] Short answer
> **Same process:** inject the other bean (constructor DI) — do not `new` it. **Another process over HTTP:** use a Framework **REST client**. Prefer **`RestClient`** (sync, fluent, thread-safe after `build()`/`create()`) or an **HTTP Service** interface (`@HttpExchange` + `HttpServiceProxyFactory`). Use **`WebClient`** when the call must stay **non-blocking**. **`RestTemplate`** is **deprecated in Framework 7.0** in favor of `RestClient`. Declarative Feign lives in **Spring Cloud**, not the Framework core.

## Same JVM versus another host

A `@Service` in *this* context is just another bean. The container already knows how to call it: wire it as a constructor argument ([[How do you use dependency injection in practice]]). That is **not** a network hop.

Calling a **remote** HTTP API is a different problem. The Framework’s *REST Clients* chapter lists four choices:

| Choice | Role |
| --- | --- |
| **`RestClient`** | Synchronous fluent client (the default for imperative apps) |
| **`WebClient`** | Non-blocking, reactive; streaming and high concurrency |
| **`RestTemplate`** | Old template API — **deprecated**, migrate to `RestClient` |
| **HTTP Service client** | Java interface with `@HttpExchange` / `@GetExchange`; proxy over one of the three above |

```d2
YourApp: {
  OrderService
  RestClient
  OrderService -> RestClient: retrieve()
}
Remote: "remote HTTP API"
YourApp.RestClient -> Remote: GET /orders/{id}
```

**Fig. 1.** A singleton bean holds a shared `RestClient` and issues HTTP; the remote service is not a Spring bean in *this* context.

## `RestClient` (typical imperative path)

Create once (often a `@Bean`), set `baseUrl` and converters on the builder, then inject that instance. After creation it is **safe on multiple threads**. Each call is a chain: HTTP method → `uri(...)` → optional headers/body → **`retrieve()`** → a **terminal** conversion (`body(Class)`, `toEntity(Class)`, `toBodilessEntity()`). `retrieve()` alone does **nothing**.

```java
@Service
public class OrderGateway {

	private final RestClient restClient;

	public OrderGateway(RestClient restClient) {
		this.restClient = restClient;
	}

	public OrderDto find(long id) {
		return restClient.get()
				.uri("/orders/{id}", id)
				.retrieve()
				.body(OrderDto.class);
	}
}
```

**Listing 1.** Inject a configured `RestClient` and convert JSON with `retrieve().body(...)`. Put the host on the builder’s `baseUrl`, not in every call.

Status **4xx/5xx** raise an exception by default (same family as `RestClientException`). Register status handlers when you need a different policy.

## HTTP Service interface (typed remote API)

Declare the contract once. `HttpServiceProxyFactory` (with `RestClientAdapter` or `WebClientAdapter`) builds a proxy you inject like any other bean. Boot can declare **HTTP Service groups** and customize them with `HttpServiceGroupConfigurer` (properties, OAuth, Cloud load balancing).

```java
public interface OrderApi {

	@GetExchange("/orders/{id}")
	OrderDto getOrder(@PathVariable long id);
}
```

**Listing 2.** `@GetExchange` on an interface; the proxy performs the HTTP. A server `@Controller` can implement the **same** interface.

## `WebClient` when you must not block

`WebClient` (Framework **5.0**) speaks `Mono`/`Flux`, default transport Reactor Netty, back pressure and streaming. Use it from WebFlux, or from MVC when you return reactive types from the controller. Do **not** `.block()` on an event-loop thread ([[What is WebClient]]; [[What is the difference between RestTemplate WebClient and RestClient]]).

## Cloud Feign is optional

**OpenFeign** (`@FeignClient`) is a **Spring Cloud** declarative client with load-balancer integration. It is not required to call HTTP from a Framework app; `RestClient` / HTTP Service covers the same job in-process. See [[What is Spring Cloud OpenFeign]] when the interview is Cloud-specific.

> [!warning] `RestTemplate` is on the way out
> Framework **7.0** deprecates `RestTemplate` in favor of `RestClient` (removal in a **future** version). New code should not add `RestTemplate`. For async/streaming, use `WebClient`, not a blocking template on a reactive stack.

> [!tip] Interview answer
> Same app: inject the other `@Service`. Remote HTTP: `RestClient` (or an `@HttpExchange` proxy) for blocking apps; `WebClient` for reactive. `RestTemplate` is deprecated as of 7.0. Do not confuse in-process DI with a network client.
