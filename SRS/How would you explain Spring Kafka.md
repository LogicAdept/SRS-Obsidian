<!--
reps: 0
priority: 0
-->
#Messaging/Tools/Kafka #Java/Spring/Kafka #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Spring Kafka: основные компоненты.**

KafkaTemplate: отправка сообщений (send). @KafkaListener: получение (метод с @KafkaListener(topics="...")). ConcurrentKafkaListenerContainerFactory: настройка concurrency, error handler, retry. ConsumerConfig: bootstrap-servers, group-id, deserializer. ProducerConfig: acks, retries, serializer.

**Spring Kafka listener concurrency?**

spring-kafka: KafkaTemplate.send(topic, key, payload). Producer: acks=all, enable.idempotence=true, JsonSerializer/Avro.
@KafkaListener(topics, groupId, concurrency). concurrency should be ≤ partition count. Manual ack or DefaultErrorHandler + DLT. Do not set concurrency higher than partitions. Test with @EmbeddedKafka or Testcontainers.
