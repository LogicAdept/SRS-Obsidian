<!--
reps: 0
priority: 0
-->
#Databases #SystemDesign/Reliability #SystemDesign/Availability #DistributedSystems #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из шпаргалок Хабра (MishaBucha, 2025). Не сверен с официальной документацией. Не считать ответом для ревью.

**What is replication?**

Источник: https://habr.com/ru/articles/968532/

Копирование данных на другие базы. Зачем: отказоустойчивость и HA. Синхронная (пишется сразу на все реплики) и асинхронная (с задержкой). Реплика может читать; запись идёт в мастер.

**Postgres in the generic replication answer?**

Streaming physical for HA; logical for CDC/upgrades. Sync vs async RPO. Slots retain WAL and can fill the disk.
