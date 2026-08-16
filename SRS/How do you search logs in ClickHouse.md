<!--
reps: 0
priority: 0
-->
#Databases/ClickHouse #Databases/Indexes #SystemDesign/Performance #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по ClickHouse (2026). Не сверен с официальной документацией ClickHouse. Не считать ответом для ревью.

**How would you design log search?**

ORDER BY (service, ts) or (toDate(ts), service) matching filters. PARTITION BY month. Skip/text index on message. Query: time range first (partition + PK prefix), then hasToken/LIKE. MV for frequent GROUP BY. EXPLAIN indexes=1 to see granules skipped. Avoid SELECT * on fat Nested/JSON columns.
