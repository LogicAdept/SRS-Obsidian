<!--
reps: 0
priority: 0
-->
#DevOps/CICD #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**CI/CD pipeline.**

checkout → build → test → docker build → push registry → deploy staging → (approval) → prod. В Яндексе: Arcadia CI + Nanny для деплоя.
