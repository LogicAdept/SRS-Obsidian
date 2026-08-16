<!--
reps: 0
priority: 0
-->
#Messaging/Tools/Kafka #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по Kafka (2026). Не сверен с официальной документацией Apache Kafka. Не считать ответом для ревью.

**Standalone consumer vs Kafka Streams?**

Standalone consumer: poll, your logic, commit. Fine for stateless routing/enrichment.
Streams: state stores, windowing, joins, EOS packaging. Choose Streams when you need state; consumer when you do not.
