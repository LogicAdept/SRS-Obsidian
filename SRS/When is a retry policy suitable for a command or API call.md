<!--
reps: 0
priority: 0
-->
#DistributedSystems/Communication #SystemDesign/Reliability #SRS

# When is a retry policy suitable for a command or API call

> [!abstract] Short answer
> Retrying is suitable when the failure is transient (timeouts, connection resets, 503/429) AND the operation is idempotent or carries an idempotency key, with exponential backoff, jitter, a retry cap or budget, and respect for Retry-After. Retrying is wrong for non-idempotent commands without deduplication, for permanent errors (validation failures, 4xx), and when retries only amplify an overloaded dependency.

## The four conditions

A retry is safe and useful when four things hold together. Transience: the error class is one that a second attempt plausibly survives — connection resets, timeouts, HTTP 503/429; Azure's retry guidance frames these as transient faults with the same diagnosis. Idempotency: the operation must tolerate re-execution — GETs and PUTs with a fixed resource id are idempotent by semantics; POST-created orders are not, unless the client sends an idempotency key that the server deduplicates (Stripe's pattern: store the first response under the key, replay it on retry). Backoff and jitter: wait exponentially longer between attempts with randomization, so a fleet of failed callers does not arrive in lockstep — Azure treats exponential backoff with jitter as the default strategy. A bound: a maximum attempt count or a retry budget, plus honoring the server's Retry-After header on 429/503. If any condition fails — permanent error, non-idempotent command, unbounded hammering — the right behavior is fail fast to the caller or fall back, not retry. [[How do you handle a two second network outage]] shows the drill in action; [[What is idempotency in HTTP and in messaging]] grounds the idempotency half.

```text
retryable : timeout, conn reset, 503, 429 (+ Retry-After honored)
            AND idempotent (GET/PUT) OR idempotency-key attached
not retryable: 400/401/403/404 (permanent), business-rule failure,
            non-idempotent POST without a key
shape     : attempts <= 3, backoff 100ms * 2^n + jitter, total budget cap
```

**Listing 1.** The retry gate: error class, idempotency, shape.

## Where the policy lives

The policy must be consistent across layers — a retrying HTTP client inside a retrying framework inside a retrying queue consumer multiplies attempts silently (3x3x3 = 27 executions), so the effective retry count is set once and propagated ( Resilience4j's Retry with maxAttempts, default 3, and waitDuration, default 500 ms, composes into the caller stack explicitly). For messaging, the equivalent is redelivery policy: at-least-once delivery makes consumer retries automatic — the consumer's obligation is idempotent processing or deduplication ([[How do you implement retries in RabbitMQ]] for the concrete mechanics), with poison messages routed to dead-lettering after the budget rather than redelivered forever. Commands that cannot be made idempotent get a different design: a workflow/saga that tracks execution state and resumes rather than re-executes. The circuit breaker wraps the whole thing so that when the dependency is truly down, retries stop and fail fast ([[How would you explain Circuit Breaker]]); the protection side of that contract is [[How do you protect a slower downstream service from overload]].

> [!warning] Retrying validation errors is a design smell
> A 400 or a business-rule rejection will fail identically forever — retrying it burns budget and hides the bug. Classify errors before retrying: transient gets backoff, permanent gets an alert and a fix, ambiguous gets an idempotency key.

> [!tip] Interview answer
> Retry when the failure is transient and the effect is safe to repeat: idempotent calls or idempotency-keyed commands, exponential backoff with jitter, an attempt cap or budget, honoring Retry-After. Never retry permanent errors or non-idempotent commands; in messaging, consumer redelivery implies the same idempotency obligation — and one retry policy per call path, not one per layer.
