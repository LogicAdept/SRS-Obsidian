<!--
reps: 0
priority: 0
-->
#Java/Spring/Transactions/Propagation #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Propagation.**

REQUIRED (default) — присоединяется/создаёт. REQUIRES_NEW — всегда новая, приостанавливает текущую (аудит/логирование). NESTED — savepoint внутри текущей. SUPPORTS — присоединяется если есть, нет — без. MANDATORY — требует существующей. NOT_SUPPORTED — приостанавливает. NEVER — если есть → исключение.

**Propagation.**

REQUIRED (default), REQUIRES_NEW, NESTED, SUPPORTS, MANDATORY, NOT_SUPPORTED, NEVER.
