<!--
reps: 0
priority: 0
-->
#Patterns/Enterprise/Integration #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Idempotent consumer.**

Таблица processed_events(event_id UUID PK). INSERT перед обработкой — конфликт → skip. Или upsert по бизнес-ключу (ON CONFLICT DO UPDATE). В транзакции с бизнес-логикой.

**Идемпотентный consumer.**

processed_events(event_id UUID PK). INSERT ON CONFLICT DO NOTHING. В транзакции с бизнес-логикой. Или upsert по бизнес-ключу.
