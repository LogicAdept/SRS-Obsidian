<!--
reps: 0
priority: 0
-->
#Java/Spring/Cloud/CircuitBreaker #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Circuit Breaker.**

Защита от каскадных сбоев. CLOSED → OPEN (блокирует) → HALF_OPEN (тестовые запросы). Resilience4j + Spring Boot стартер. Конфигурация: failureRateThreshold, waitDurationInOpenState. Fallback: дефолтное значение или кэш.

**Circuit Breaker.**

Защита от каскадных сбоев. CLOSED → OPEN → HALF_OPEN. Resilience4j. fallback-ответ при недоступности downstream.

**Resilience4j in Spring interviews?**

CLOSED/OPEN/HALF_OPEN. Spring Cloud CircuitBreaker + Resilience4j (not Hystrix). Fallback, slow-call threshold, ignore business exceptions, metrics.
