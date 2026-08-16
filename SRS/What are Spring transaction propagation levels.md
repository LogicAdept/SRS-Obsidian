<!--
reps: 0
priority: 0
-->
#Java/Spring/Transactions #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по Spring (2026). Не сверен с официальной документацией Spring. Не считать ответом для ревью.

**REQUIRED vs REQUIRES_NEW vs NESTED?**

REQUIRED join-or-create (default). REQUIRES_NEW suspend and independent commit. NESTED savepoint. MANDATORY/NEVER/NOT_SUPPORTED/SUPPORTS as names suggest. Inner REQUIRES_NEW only works across a proxy.
