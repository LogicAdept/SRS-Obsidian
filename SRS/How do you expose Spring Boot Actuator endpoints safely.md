<!--
reps: 0
priority: 0
-->
#Java/Spring/Boot/Actuator #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по Spring (2026). Не сверен с официальной документацией Spring. Не считать ответом для ревью.

**Which Actuator endpoints in production?**

health (liveness/readiness for k8s), info, prometheus/metrics. Do not expose env, heapdump, logfile, beans, mappings publicly. management.endpoints.web.exposure.include=... and a separate management port. Secure with Spring Security. Custom HealthIndicator for DB/broker. show-details only internally.
