<!--
reps: 0
priority: 0
-->
#Databases/SQL #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**NULL в SQL — почему NULL = NULL это UNKNOWN?**

NULL — отсутствие значения, не ноль. NULL = NULL → UNKNOWN (не true и не false). Для проверки: IS NULL / IS NOT NULL. COALESCE(a, b) — первый не-NULL. Ловушка: WHERE status != 'active' НЕ вернёт строки с NULL-статусом.

**NULL grouping in Postgres?**

All NULLs one group. UNIQUE allows multiple NULLs. Partial unique WHERE col IS NOT NULL if you need uniqueness only when present.
