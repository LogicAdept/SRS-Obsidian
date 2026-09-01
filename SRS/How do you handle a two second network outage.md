<!--
reps: 0
priority: 0
-->
#SystemDesign/Reliability #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Кейс: сеть «моргнула» на 2 секунды. Что делать?**

Retry с exponential backoff + jitter (не все клиенты ретраят одновременно). Circuit Breaker: после N ошибок → OPEN (не шлём запросы) → HALF_OPEN (тестовый) → CLOSED. Idempotency-Key: чтобы retry не создал дубль. Timeout: не ждать бесконечно (5–10 сек). Fallback: кэшированный ответ или graceful degradation.
