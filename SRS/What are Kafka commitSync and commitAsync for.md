<!--
reps: 0
priority: 0
-->
#Messaging/Tools/Kafka #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по Kafka (2026). Не сверен с официальной документацией Apache Kafka. Не считать ответом для ревью.

**commitSync vs commitAsync?**

Manual commits after processing. commitSync blocks until broker ack (safer). commitAsync is faster, may lose a commit on crash. At-least-once: process then commit. Never auto-commit on a timer for critical work.

**What offset-commit styles does the article mention?**

Источник: https://habr.com/ru/articles/968844/

Варианты сдвига offset в статье: автоматически при отправке/принятии; после обработки лидером; после обработки всеми (кворум) — формулировки сырые.
commitSync — ждёт ack брокера, для гарантированной фиксации после обработки.
commitAsync — не ждёт подтверждения; быстрее, риск потерять последний commit.
