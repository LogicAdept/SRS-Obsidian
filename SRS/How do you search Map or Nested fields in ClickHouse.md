<!--
reps: 0
priority: 0
-->
#Databases/OLAP/ClickHouse #Databases/Indexes #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по ClickHouse (2026). Не сверен с официальной документацией ClickHouse. Не считать ответом для ревью.

**How do you index Map keys/values?**

mapContains / map values; text and bloom skip indexes can target mapKeys/mapValues. Nested exploded via ARRAY JOIN then filter. Don't LIKE the whole JSON String if you can use JSON/Map types + skip/text indexes on the extracted field.
