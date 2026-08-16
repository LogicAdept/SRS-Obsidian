<!--
reps: 0
priority: 0
-->
#Patterns/Architecture/Microservices/ExternalAPI #API/Gateway #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по Spring (2026). Не сверен с официальной документацией Spring. Не считать ответом для ревью.

**Spring Cloud Gateway as the gateway?**

Single entry: routing, auth, rate limit, TLS termination. In Spring: Cloud Gateway (WebFlux). Alternative: Ingress/API gateway products. Don't put business logic in the gateway.
