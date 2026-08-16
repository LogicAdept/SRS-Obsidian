<!--
reps: 0
priority: 0
-->
#Messaging/Tools/Kafka #DistributedSystems/Communication #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по Kafka (2026). Не сверен с официальной документацией Apache Kafka. Не считать ответом для ревью.

**How does Kafka handle message ordering?**

Non-null key → default murmur2 hash → same key always hits the same partition → per-key order.
Null key → sticky/round-robin spread, no key-based order.
Use orderId/userId when lifecycle events must stay ordered. Hot keys overload one partition. Increasing partition count later does not rehash old records — new hash mapping can split a key's future vs past.
