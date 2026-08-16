<!--
reps: 0
priority: 0
-->
#Java/Language #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**CI vs CD.**

CI — автосборка+тесты при push. CD — Delivery (ручной деплой) или Deployment (автодеплой). Pipeline: checkout → build → test → docker build → push registry → deploy staging → (approval) → prod.
