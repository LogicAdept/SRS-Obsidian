<!--
reps: 0
priority: 0
-->
#Messaging/Tools/Kafka #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Kafka Streams vs обычный Consumer.**

Consumer: ты сам управляешь offset, обработкой, сохранением. Kafka Streams: декларативная обработка потоков (filter, map, groupBy, aggregate, join). Stateful (RocksDB для локального состояния). Exactly-once semantics встроены. Для простых задач — Consumer, для stream processing (агрегация, join потоков) — Kafka Streams.

**What is Kafka Streams?**

Java library: stateful aggregations/joins, changelog topics, optional exactly_once_v2. Runs inside your app, no Flink cluster. Use Flink when you need a dedicated stream cluster and heavy event-time windows.

**What is Kafka Streams at cheat-sheet level?**

Источник: https://habr.com/ru/articles/968844/

Работа с потоками из топиков в реальном времени: map/filter/reduce и агрегации без отдельного кластера. Для больших потоков событий с трансформациями «на лету». Спрашивают редко.
