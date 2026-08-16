<!--
reps: 0
priority: 0
-->
#Java/Language #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Liveness vs Readiness probe.**

Liveness: жив ли → перезапуск. Readiness: готов ли → убирается из балансировки. Spring Boot Actuator: /health/liveness, /health/readiness.

**Liveness vs Readiness probe.**

Liveness: жив ли? Нет → перезапуск. Readiness: готов к трафику? Нет → убирается из балансировки. Spring Boot Actuator: /health/liveness, /health/readiness.
