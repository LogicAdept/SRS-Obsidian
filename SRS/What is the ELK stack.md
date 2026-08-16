<!--
reps: 0
priority: 0
-->
#Observability #Logging #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**ELK: как искать логи теста?**

Elasticsearch хранит/индексирует, Kibana — UI для поиска. Фильтр: traceId + временной диапазон. KQL: level:ERROR AND service:payment. MDC: Mapped Diagnostic Context — traceId пробрасывается через потоки. К багу прикладываешь: запрос/ответ + лог по traceId + timestamp.
