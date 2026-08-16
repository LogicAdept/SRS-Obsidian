<!--
reps: 0
priority: 0
-->
#Messaging/Tools/Kafka #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по Kafka (2026). Не сверен с официальной документацией Apache Kafka. Не считать ответом для ревью.

**What does isolation.level=read_committed do?**

Default read_uncommitted: consumers see all records including aborted transactions.
read_committed: hide aborted transactional batches; required for exactly-once consume-transform-produce so downstream never reads rolled-back data.
Pair with transactional producers and disabled auto-commit.
