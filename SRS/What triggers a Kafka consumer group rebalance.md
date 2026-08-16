<!--
reps: 0
priority: 0
-->
#Messaging/Tools/Kafka #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по Kafka (2026). Не сверен с официальной документацией Apache Kafka. Не считать ответом для ревью.

**What triggers a consumer group rebalance and how do you reduce its impact?**

Triggers: member join/leave/crash, missed heartbeats (session.timeout.ms), poll gap (max.poll.interval.ms), partition count change.
Eager/range: revoke all partitions — stop-the-world pause.
Cooperative sticky (preferred): only moving partitions are revoked.
Static membership (group.instance.id): rolling restart reclaims the same partitions without a full rebalance — useful on Kubernetes.
Tune session.timeout.ms, heartbeat.interval.ms (~1/3 of session), max.poll.interval.ms; do not block the poll loop.

**What does the group leader do on rebalance?**

Источник: https://habr.com/ru/articles/968844/

Триггеры из статьи: новый консьюмер, выход/падение, смена топиков. Лидер считает новое распределение партиций и отправляет каждому его список; все применяют assignment и читают с сохранённого offset.
