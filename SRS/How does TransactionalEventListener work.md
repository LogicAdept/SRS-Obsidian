<!--
reps: 0
priority: 0
-->
#Java/Spring/Transactions #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по Spring (2026). Не сверен с официальной документацией Spring. Не считать ответом для ревью.

**What is @TransactionalEventListener?**

Listen to ApplicationEvent after the publisher's transaction phase (AFTER_COMMIT default) so you don't send Kafka/email if the DB rolls back. BEFORE_COMMIT / AFTER_ROLLBACK also exist. Requires an active transaction around publishEvent. Follow-up: outbox vs sync listener.
