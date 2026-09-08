<!--
reps: 0
priority: 0
-->
#Java/Spring/Cloud/CircuitBreaker #SRS

# How does Resilience4j circuit breaker work with Spring?

> [!abstract] Short answer
> Two Spring stacks share the **same Resilience4j machine** (CLOSED / OPEN / HALF_OPEN, sliding window, `failureRateThreshold`). **Spring Cloud CircuitBreaker** is the **Commons API**: starters `spring-cloud-starter-circuitbreaker-resilience4j` (blocking) or `…-reactor-resilience4j` (reactive), then `CircuitBreakerFactory.create(id).run(…)`. Every run is also wrapped in a **TimeLimiter** unless you disable it. **`resilience4j-spring-boot3`** is the **annotation** path: `@CircuitBreaker`, `@Retry`, `@Bulkhead`, `@TimeLimiter` plus AOP (needs `spring-boot-starter-aop`). Hystrix is **not** a Cloud CircuitBreaker implementation.

## Cloud factory vs annotations

Cloud: a `Customizer<Resilience4JCircuitBreakerFactory>` (or the reactive factory) sets default **`CircuitBreakerConfig`** and **`TimeLimiterConfig`**. YAML under `resilience4j.circuitbreaker` / `resilience4j.timelimiter` **overrides** Java `Customizer` (instance → group → global). `create("backendA")` picks the `backendA` instance properties ([[How would you explain Circuit Breaker]], [[What is Spring Cloud]]).

If `resilience4j-bulkhead` is on the classpath, Cloud **wraps** calls with a Bulkhead; default is **`FixedThreadPoolBulkhead`** (`spring.cloud.circuitbreaker.resilience4j.enableSemaphoreDefaultBulkhead=true` switches to semaphore). Disable bulkhead with `spring.cloud.circuitbreaker.bulkhead.resilience4j.enabled=false`.

Annotation starter: same YAML instance names, methods annotated `@CircuitBreaker(name = "backendA", fallbackMethod = "fallback")`. Fallback methods live in the **same class**, same parameters **plus one exception type** (closest match wins, like catch). Annotation fallbacks run like **try/catch** — **independent of breaker state**, not only when OPEN.

```java
@Bean
public Customizer<Resilience4JCircuitBreakerFactory> defaultCb() {
	return factory -> factory.configureDefault(id -> new Resilience4JConfigBuilder(id)
			.timeLimiterConfig(TimeLimiterConfig.custom().timeoutDuration(Duration.ofSeconds(4)).build())
			.circuitBreakerConfig(CircuitBreakerConfig.ofDefaults())
			.build());
}
```

**Listing 1.** Conceptual. Cloud default: breaker + **TimeLimiter** on every `run`.

```java
@CircuitBreaker(name = "catalog", fallbackMethod = "empty")
public List<Item> load() { /* RestClient call */ }

private List<Item> empty(Throwable t) {
	return List.of();
}
```

**Listing 2.** Conceptual. `resilience4j-spring-boot3` AOP; fallback signature matches plus `Throwable`.

Default annotation **order** (outer → inner): **Retry ( CircuitBreaker ( RateLimiter ( TimeLimiter ( Bulkhead ( f ) ) ) ) )** — Retry is **outermost**. Change with `*AspectOrder` properties or drop annotations and chain decorators.

```d2
direction: down
api: "CircuitBreakerFactory.run\nor @CircuitBreaker" {
  width: 280
  height: 45
  style.fill: "#e3f2fd"
}
tl: "TimeLimiter\n(Cloud: on by default)" {
  width: 260
  height: 40
  style.fill: "#fff3e0"
}
cb: "Resilience4j CircuitBreaker\nwindow · rates · states" {
  width: 280
  height: 50
  style.fill: "#e8f5e9"
}
call: "downstream HTTP" {
  width: 200
  height: 40
  style.fill: "#fce4ec"
}
api -> tl
tl -> cb
cb -> call
```

**Fig. 1.** Cloud always time-limits unless `spring.cloud.circuitbreaker.resilience4j.disable-time-limiter=true`.

Metrics: `spring-boot-starter-actuator` + `resilience4j-micrometer` (Cloud auto-config; disable with `spring.cloud.circuitbreaker.resilience4j.micrometer.enabled=false`). Annotation stack publishes `/actuator/metrics` names such as `resilience4j.circuitbreaker.failure.rate`. **Health** mapping (CLOSED → UP, OPEN → **DOWN**, HALF_OPEN → UNKNOWN) is **off** by default — turning it on can mark the **whole app DOWN** when one backend is open ([[What is Spring Cloud Gateway]]).

> [!warning] TimeLimiter is not optional in Cloud unless you switch it off
> Cloud Resilience4j **enables TimeLimiter by default** (`TimeLimiterConfig.ofDefaults()` if you set nothing). A “hanging” HTTP call is cut by **timeout**, then recorded as a failure. That is why interview answers pair CB with TimeLimiter; it is already there on the Cloud starter.

> [!warning] Two starters, two programming models
> `@CircuitBreaker` from `io.github.resilience4j` does **not** appear just because you added `spring-cloud-starter-circuitbreaker-resilience4j`. Cloud wants **`CircuitBreakerFactory`**. Mixing both is possible but you then have **two** registries/aspects to reason about.

> [!tip] Interview answer
> Resilience4j is the library; Spring Cloud CircuitBreaker is the factory API plus TimeLimiter (and optional Bulkhead). The other Boot path is `resilience4j-spring-boot3` annotations and Actuator. Configure windows and thresholds in YAML. Ignore business exceptions so they do not open the circuit. Hystrix is gone from this stack; implementations are Resilience4J and Spring Retry.
