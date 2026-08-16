<!--
reps: 0
priority: 0
-->
#Databases/ClickHouse #Databases/SQL #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по ClickHouse (2026). Не сверен с официальной документацией ClickHouse. Не считать ответом для ревью.

**What is ASOF JOIN?**

Time-series: for each left row, take the latest right row with timestamp ≤ left timestamp (as-of). Quotes vs trades. Requires ordered keys. Different from equality JOIN. Interview flavor for market data / IoT.
