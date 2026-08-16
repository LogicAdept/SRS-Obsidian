<!--
reps: 0
priority: 0
-->
#Java/Language #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Pagination: offset/limit vs cursor-based.**

offset/limit: GET /users?offset=20&limit=10. Простой, но медленный на больших данных (БД пропускает offset строк). cursor-based: GET /users?after=abc123&limit=10. Быстрый (индекс по
