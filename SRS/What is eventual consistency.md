<!--
reps: 0
priority: 0
-->
#SystemDesign/Consistency #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Eventual consistency — почему assertEquals сразу может упасть?**

Kafka/RabbitMQ — асинхронные. Сообщение отправлено, но ещё не обработано consumer'ом. assertEquals сразу после send → данных в БД ещё нет. Решение: Awaitility с polling, или Thread.sleep (плохо — хрупко), или callback/listener.
