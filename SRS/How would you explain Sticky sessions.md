<!--
reps: 0
priority: 0
-->
#SystemDesign #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Sticky sessions.**

Привязка клиента к конкретному backend. По cookie, IP, header. Проблема: неравномерная нагрузка при скейлинге. Решение: shared session storage (Redis) или stateless (JWT).
