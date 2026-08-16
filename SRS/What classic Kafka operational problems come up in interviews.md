<!--
reps: 0
priority: 0
-->
#Messaging/Tools/Kafka #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из шпаргалок Хабра (MishaBucha, 2025). Не сверен с официальной документацией. Не считать ответом для ревью.

**What classic Kafka problems does the article list?**

Источник: https://habr.com/ru/articles/968844/

Message duplication — at-least-once, падение консьюмера → idempotent producer, транзакции, фильтр по ID.
Consumer lag — медленная обработка, мало партиций → больше партиций/консьюмеров, быстрее обработка.
Stuck partitions — блокирующая обработка, долгий commit → async, таймауты, отдельные потоки.
Hot partitions — плохие ключи → равномерные ключи, больше партиций, custom partitioner.
Rebalancing storm — частые join/leave, короткий session.timeout.ms → увеличить timeout, стабильные instance.
