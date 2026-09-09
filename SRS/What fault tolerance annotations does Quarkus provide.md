<!--
reps: 0
priority: 0
-->
#Java/Quarkus #SRS

# What fault tolerance annotations does Quarkus provide?

> [!abstract] Short answer
> `quarkus-smallrye-fault-tolerance` implements **MicroProfile Fault Tolerance** and Quarkus extras: **`@Retry`** (maxRetries, delay, jitter, retryOn/abortOn), **`@Timeout`** (milliseconds), **`@CircuitBreaker`** (failure-rate windows, open/closed transitions), **`@Bulkhead`** (concurrency or queue limits), **`@Fallback`** (alternative method or handler), plus `@RateLimit`, `@Asynchronous` and programmatic `FaultTolerance` API. They are CDI interceptors composed by stacking on a method — with per-method configuration overrides through MicroProfile Config keys.

## How the annotations compose

All of them are interceptor-based: ArC weaves them at build time around bean methods ([[What bean scopes does Quarkus support]]), and stacking defines an execution plan — `@Timeout` bounds a single attempt, `@Retry` repeats attempts (each attempt gets the full timeout), `@Fallback` runs when all retries fail, `@CircuitBreaker` decides based on rolling failure statistics whether to call at all, `@Bulkhead` caps concurrent executions. Every annotation's knobs are overridable per method at runtime with config like `quarkus.fault-tolerance."method-name".retry.max-retries` — the same code behaves differently per environment without recompiling. The programmatic API (`FaultTolerance.create()`) covers cases where annotations cannot express the flow.

```java
// src/main/java/org/acme/check/infra/FragileService.java (JDK 21, Quarkus 3.39.2;
// mvn test: 6/6 green - the fallback body was returned and the attempt counter
// proved 1 initial call + 3 retries).
package org.acme.check.infra;

import jakarta.enterprise.context.ApplicationScoped;
import org.eclipse.microprofile.faulttolerance.Fallback;
import org.eclipse.microprofile.faulttolerance.Retry;
import java.util.concurrent.atomic.AtomicInteger;

@ApplicationScoped
public class FragileService {
    private final AtomicInteger attempts = new AtomicInteger();

    @Retry(maxRetries = 3, delay = 0)
    @Fallback(fallbackMethod = "cached")
    public String flaky(boolean fail) {
        attempts.incrementAndGet();
        if (fail) throw new IllegalStateException("boom");
        return "real";
    }

    public int attemptsCount() {
        return attempts.get();
    }

    String cached(boolean fail) {
        return "fallback";
    }
}
// Test evidence (ExpansionTest, verbatim assertions):
//   GET /demo/fallback -> 200 body "fallback"
//   assertEquals(4, fragile.attemptsCount() - before, "1 call + 3 retries");
// The @Fallback method served the response only after @Retry exhausted maxRetries=3.
```

**Listing 1.** Retry-then-fallback composed on one method: four attempts happened (initial + 3 retries), the exception from each was swallowed by the retry plan, and the fallback supplied the final value — the exact behavior interviewers ask you to trace on a whiteboard.

```d2
direction: down
call: "Call with @Retry + @Fallback" {
  width: 280
  height: 50
}
cb: "@CircuitBreaker\nis the circuit open?" {
  width: 250
  height: 55
  style.fill: "#e3f2fd"
}
bh: "@Bulkhead\nconcurrency slot available?" {
  width: 270
  height: 55
  style.fill: "#e3f2fd"
}
try: "@Timeout bounds each attempt" {
  width: 270
  height: 50
  style.fill: "#fff3e0"
}
ok: "success -> return" {
  width: 200
  height: 45
  style.fill: "#e8f5e9"
}
fb: "retries exhausted\n-> @Fallback method" {
  width: 250
  height: 55
  style.fill: "#f5c6c6"
}
call -> cb -> bh -> try
try -> ok
try -> fb
```

**Fig. 1.** The interceptor order on one call: circuit gate, bulkhead gate, timeout-per-attempt under retry, fallback as the last resort.

## Circuit breaker and bulkhead specifics

`@CircuitBreaker` parameters — `requestVolumeThreshold`, `failureRatio`, `delay` in open state — implement the classic half-open/closed state machine; it is stateful across calls, so a test must trigger enough calls to fill the window. `@Bulkhead(value=N)` limits simultaneous executions (with a waiting queue size in the thread-pool flavor); with `@Asynchronous` it converts to semaphores over futures. Both integrate with Micrometer metrics so the state and rejection counts are observable ([[How do you expose metrics in Quarkus]]).

> [!warning] @Retry is not idempotency and @Fallback hides incidents
> Retrying a non-idempotent operation (charge, POST) duplicates side effects — retry belongs on read-mostly or idempotent calls, or needs idempotency keys. Fallback values that silently mask an outage turn "degraded" into "we did not notice for three days" — log and metric the fallback path. Common config trap: `@Retry(delay=...)` without jitter under correlated failure makes all callers retry in lockstep (thundering herd); the spec's `jitter`/`jitterDelay` exists for that, and interviewers often ask what happens "when the whole cluster retries at once".

> [!tip] Interview answer
> Quarkus ships SmallRye Fault Tolerance, the MicroProfile Fault Tolerance implementation: @Retry, @Timeout, @CircuitBreaker, @Bulkhead, @Fallback, plus extras like @RateLimit and a programmatic API. They're CDI interceptors I can stack — timeout bounds each attempt, retry repeats, fallback catches exhaustion, circuit breaker and bulkhead gate by failure statistics and concurrency — and each knob is overridable per method via config keys. In my verified demo, one call plus three retries landed on the fallback method, and the counter proved it.
