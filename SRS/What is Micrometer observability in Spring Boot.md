<!--
reps: 0
priority: 0
-->
#Java/Spring/Boot/Actuator #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по Spring (2026). Не сверен с официальной документацией Spring. Не считать ответом для ревью.

**Logs vs metrics vs traces?**

Boot 3 Observability: Micrometer Observation + tracing (Brave/OTel) + metrics. Same observation can log, time, and span. Distributed tracing: traceId in logs, Zipkin/Tempo. Not a replacement for logs; correlates them. Actuator /prometheus for scrape.
