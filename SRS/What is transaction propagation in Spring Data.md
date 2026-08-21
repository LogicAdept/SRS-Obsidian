<!--
reps: 0
priority: 0
-->
#Java/Spring/Data/JPA #Java/Spring/Transactions/Propagation #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Propagation-уровни транзакций.**

REQUIRED (default) — присоединяется или создаёт. REQUIRES_NEW — всегда новая, приостанавливает текущую. NESTED — savepoint. SUPPORTS, MANDATORY, NOT_SUPPORTED, NEVER.

**Какие propagation знаешь?**

REQUIRED (default) — использует существующую транзакцию или создаёт новую. REQUIRES_NEW — приостанавливает текущую и создаёт новую. Полезно для аудита: должно записаться даже если основная транзакция упала. На стажёре этих двух хватит, остальные (NESTED, MANDATORY, SUPPORTS, NEVER, NOT_SUPPORTED) знать как имена.

**Propagation-уровни транзакций.**

REQUIRED (default) — присоединяется или создаёт. REQUIRES_NEW — всегда новая. NESTED — savepoint. SUPPORTS, MANDATORY, NOT_SUPPORTED, NEVER.
