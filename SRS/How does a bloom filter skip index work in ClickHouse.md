<!--
reps: 0
priority: 0
-->
#Databases/OLAP/ClickHouse #Databases/Indexes #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по ClickHouse (2026). Не сверен с официальной документацией ClickHouse. Не считать ответом для ревью.

**When do you add bloom_filter?**

Probabilistic 'value maybe in this granule group'. Good for user_id / UUID equality when it is NOT the ORDER BY prefix. False positives → extra granule reads, never false negatives for skip. Useless if the column is randomly scattered so almost every granule hits. Tune false-positive rate; still verify rows.
