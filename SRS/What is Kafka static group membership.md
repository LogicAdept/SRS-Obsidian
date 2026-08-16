<!--
reps: 0
priority: 0
-->
#Messaging/Tools/Kafka #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по Kafka (2026). Не сверен с официальной документацией Apache Kafka. Не считать ответом для ревью.

**What is static group membership (group.instance.id)?**

Give a consumer a stable group.instance.id. After a restart it reclaims the same partitions instead of triggering a full eager rebalance.
Useful for Kubernetes rolling deploys. session.timeout still applies if the instance is really gone.
