<!--
reps: 0
priority: 0
-->
#Messaging/Tools/Kafka #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по Kafka (2026). Не сверен с официальной документацией Apache Kafka. Не считать ответом для ревью.

**Why is enable.auto.commit dangerous?**

Default auto-commit fires on a timer after poll, not after your handler succeeds. Crash between commit and processing → skip (silent loss). Crash after processing before commit → duplicate.
For at-least-once: enable.auto.commit=false, commitSync after successful processing. For EOS: sendOffsetsToTransaction instead.
