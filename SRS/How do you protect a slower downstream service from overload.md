<!--
reps: 0
priority: 0
-->
#Java/Language #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Кейс: сервис A — 1000 TPS, сервис B — 200 TPS. Как защитить B?**

Rate limiter на стороне A (ограничить исходящие). Kafka как буфер: A пишет в топик → B читает со своей скоростью (backpressure). Circuit Breaker: при перегрузке B → A получает fallback. Bulkhead: отдельный пул потоков для вызовов B (не блокирует остальные). Самое надёжное: Kafka-буфер + rate limiter.

**Spring tools for protecting B?**

Resilience4j: CB + bulkhead + rate limiter + TimeLimiter. Queue (Kafka) as buffer. Don't only retry harder.
