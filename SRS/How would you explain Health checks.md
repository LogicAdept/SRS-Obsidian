<!--
reps: 0
priority: 0
-->
#Java/Language #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Health checks.**

Active: балансер периодически проверяет backend (HTTP GET /health, TCP connect). Passive: считает ошибки от реальных запросов. Комбинация — best practice.
