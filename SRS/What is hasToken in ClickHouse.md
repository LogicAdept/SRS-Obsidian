<!--
reps: 0
priority: 0
-->
#Databases/OLAP/ClickHouse #Databases/Indexes #Databases/SQL #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по ClickHouse (2026). Не сверен с официальной документацией ClickHouse. Не считать ответом для ревью.

**hasToken vs LIKE?**

hasToken(haystack, 'error') matches a token bounded by non-alphanumerics — pairs with tokenbf_v1 or text index. LIKE '%error%' matches substrings inside tokens ('preerroring'). For logs, hasToken + text index is the indexable search; LIKE is the last resort.
