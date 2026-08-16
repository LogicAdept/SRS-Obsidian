<!--
reps: 0
priority: 0
-->
#Java/Spring/Cloud/Gateway #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по Spring (2026). Не сверен с официальной документацией Spring. Не считать ответом для ревью.

**Spring Cloud Gateway vs Zuul?**

Gateway: WebFlux, non-blocking, dynamic routes, filters (auth, rate limit, rewrite). Zuul 1: blocking servlet, legacy. Production 2026: Gateway (or Ingress/API gateway outside Spring). Don't run blocking I/O on Gateway's event loop. Pair with discovery or static URI.
