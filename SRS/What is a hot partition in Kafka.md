<!--
reps: 0
priority: 0
-->
#Messaging/Tools/Kafka #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по Kafka (2026). Не сверен с официальной документацией Apache Kafka. Не считать ответом для ревью.

**What is a hot partition?**

One partition receives far more traffic than others — usually a hot key (one user/tenant/orderId dominates). Consumers on that partition lag while others idle. Fix: better keys, salt hot keys, or more partitions only if keys actually spread.

**What is a hot partition (skew)?**

Источник: https://habr.com/ru/articles/968844/

Нагрузка распределена неравномерно из-за несбалансированных ключей. Решение: равномерные ключи, больше партиций, custom partitioner.
