<!--
reps: 0
priority: 0
-->
#Messaging/Tools/Kafka #Messaging/Tools/RabbitMQ #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Kafka vs RabbitMQ: ключевые различия.**

Kafka: pull (consumer сам забирает), хранит сообщения (retention), log compaction, высокая пропускная способность, горизонтальное масштабирование. RabbitMQ: push (брокер отправляет), удаляет после ACK, rich routing (exchanges), проще для простых сценариев. В Т1: Kafka для event-driven, RabbitMQ для task queues.

**Kafka vs RabbitMQ?**

Kafka: dumb broker, durable log, replay, high throughput, per-partition order, fan-out via groups.
RabbitMQ: smart routing (exchanges), per-message ack, better for task queues and RPC. Pick by replay vs routing.

**Kafka versus RabbitMQ delivery model?**

Источник: https://habr.com/ru/articles/968844/

Kafka — pull: консьюмер сам читает из лога; сообщения хранятся до retention, не удаляются после обработки. Rabbit — push: брокер толкает сообщение и удаляет после обработки.

**RabbitMQ vs Kafka — interview contrast?**

RabbitMQ: AMQP broker, push to competing consumers, delete after ack, rich routing (exchange types), better for tasks/RPC/flexible routing. Pull vs push: consumers are pushed (with prefetch).
Kafka: partitioned log, consumers pull and keep offsets, replay, high throughput stream. Don't use RabbitMQ as an event store; don't use Kafka as a simple work queue unless you need the log.
