<!--
reps: 0
priority: 0
-->
#Java/Spring/Cloud #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по Spring (2026). Не сверен с официальной документацией Spring. Не считать ответом для ревью.

**What is OpenFeign?**

Declarative HTTP client: interface + @FeignClient + Spring MVC mapping. Encoder/decoder, load balancer integration. Boot 3: still used; RestClient is the in-process alternative. Circuit breaker: feign.circuitbreaker.enabled or Resilience4j annotations. Fallbacks must be beans. Timeouts and retries are interview follow-ups.
