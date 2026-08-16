<!--
reps: 0
priority: 0
-->
#Java/Language #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Liveness vs Readiness vs Startup probe.**

Liveness — жив ли? Нет → перезапуск. Readiness — готов к трафику? Нет → убирается из LB. Startup — для медленного старта: пока не пройдёт, остальные не проверяются. Spring Boot Actuator: /actuator/health/liveness, /actuator/health/readiness.
