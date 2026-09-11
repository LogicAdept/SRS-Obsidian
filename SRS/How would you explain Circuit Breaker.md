<!--
reps: 0
priority: 0
-->
#Java/Spring/Cloud/CircuitBreaker #Patterns/DistributedSystems #SRS

# How would you explain Circuit Breaker?

> [!abstract] Short answer
> A **circuit breaker** **stops calling** a failing dependency so errors **do not cascade**. In Resilience4j it is a **state machine**: **CLOSED** (calls go through, outcomes recorded), **OPEN** (calls rejected immediately with `CallNotPermittedException`), **HALF_OPEN** (a few **probe** calls). Spring Cloud **CircuitBreaker** is an **abstraction** (`CircuitBreakerFactory.create(id).run(supplier, fallback)`) with **Resilience4J** and **Spring Retry** implementations — **not** Hystrix. Fallback is the **Function** when the breaker trips.

## CLOSED → OPEN → HALF_OPEN

Resilience4j records successes and failures in a **sliding window** (count-based or time-based). It opens when **failure rate** or **slow-call rate** is **≥** the threshold — but only after **`minimumNumberOfCalls`** in the window. Default **`failureRateThreshold` is 50%**. Slow calls use **`slowCallDurationThreshold`** and **`slowCallRateThreshold`**. **OPEN** waits **`waitDurationInOpenState`** (default 60s), then **HALF_OPEN** allows **`permittedNumberOfCallsInHalfOpenState`** (default 10). Those probes decide CLOSED vs OPEN again. Special states: **DISABLED**, **FORCED_OPEN**, **METRICS_ONLY** ([[How does Resilience4j circuit breaker work with Spring]], [[How do you protect a slower downstream service from overload]]).

By default **every exception is a failure**. **`recordExceptions`** / **`ignoreExceptions`**: ignored types count as **neither** failure nor success (typical for **business** exceptions you do not want to trip the breaker).

The breaker is **thread-safe** for state and the window; it does **not** serialize the **call**. Many threads can be in-flight in CLOSED — use a **Bulkhead** to cap concurrency.

```d2
direction: right
closed: "CLOSED\nrecord outcomes" {
  width: 160
  height: 50
  style.fill: "#e8f5e9"
}
open: "OPEN\nCallNotPermittedException" {
  width: 200
  height: 50
  style.fill: "#fce4ec"
}
half: "HALF_OPEN\nprobe calls" {
  width: 160
  height: 50
  style.fill: "#fff3e0"
}
closed -> open: "failure or slow rate ≥ threshold"
open -> half: "waitDurationInOpenState"
half -> closed: "rates below threshold"
half -> open: "rates still high"
```

**Fig. 1.** Three normal states; OPEN fails fast so the dependency can recover.

## Spring Cloud API

Include a CircuitBreaker starter; a **`CircuitBreakerFactory`** (or **`ReactiveCircuitBreakerFactory`**) bean appears. `run` wraps a `Supplier` (or `Mono`/`Flux`) and an optional fallback `Function<Throwable, …>` ([[What is Spring Cloud Gateway]], [[What is Spring Cloud OpenFeign]]).

```java
@Service
public class CatalogClient {

	private final RestClient rest;
	private final CircuitBreakerFactory<?, ?> cbFactory;

	public String load() {
		return cbFactory.create("catalog").run(
				() -> rest.get().uri("http://catalog/items").retrieve().body(String.class),
				throwable -> "[]");
	}
}
```

**Listing 1.** Conceptual. Commons API; Resilience4J or Spring Retry is behind the factory.

> [!warning] Nine failures need not open the breaker
> If `minimumNumberOfCalls` is 10 (or the window is not full), **all** of the first nine calls can fail and the state stays **CLOSED**. Interview “N errors in a row → open” is a cartoon; Resilience4j uses **rates over a window**, plus a **minimum sample**.

> [!warning] OPEN is fail-fast, not a retry
> Callers get **`CallNotPermittedException`** (or your **fallback**). Retrying the same instance immediately **increases** load unless Retry is a **separate** decorator with a sensible policy.

> [!tip] Interview answer
> Circuit breaker: fail fast when a dependency is sick so the rest of the system survives. CLOSED records, OPEN rejects, HALF_OPEN probes. In Spring Cloud you wrap calls with `CircuitBreakerFactory`; Resilience4j is the usual implementation, Hystrix is not. Tune failure/slow-call rates and `minimumNumberOfCalls`, and give a cheap fallback.
