<!--
reps: 0
priority: 0
-->
#Messaging/Tools/Kafka #Java/Security #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по Kafka (2026). Не сверен с официальной документацией Apache Kafka. Не считать ответом для ревью.

**How do you secure Kafka in production?**

TLS in transit. SASL (SCRAM or OAuth). ACLs: each service principal only produce or consume the topics it needs. No public plaintext brokers. Rotate credentials. Separate topics per bounded context.
