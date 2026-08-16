<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Boot #DevOps/Tools/Kubernetes #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по Spring (2026). Не сверен с официальной документацией Spring. Не считать ответом для ревью.

**Liveness vs readiness in Actuator?**

management.endpoint.health.probes.enabled=true → /health/liveness (process up) vs /health/readiness (can take traffic: DB, etc.). Don't use the same probe for both. Restart on failed liveness; remove from LB on failed readiness.
