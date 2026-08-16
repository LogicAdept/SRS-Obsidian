<!--
reps: 0
priority: 0
-->
#Java/Spring/Cloud/CircuitBreaker #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по Spring (2026). Не сверен с официальной документацией Spring. Не считать ответом для ревью.

**How do you use Resilience4j in Spring Boot?**

starter: annotations @CircuitBreaker, @Retry, @Bulkhead, @TimeLimiter or CircuitBreakerRegistry. States CLOSED → OPEN → HALF_OPEN. Tune sliding window, failureRateThreshold, slowCall*, waitDurationInOpenState, ignore business exceptions. Hystrix is dead. Metrics via Actuator/Micrometer. Fallback must be cheap. Pair TimeLimiter so threads don't hang.
