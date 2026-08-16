<!--
reps: 0
priority: 0
-->
#Messaging/Tools/Kafka #Java/Spring/Framework/Boot #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по Kafka (2026). Не сверен с официальной документацией Apache Kafka. Не считать ответом для ревью.

**How do you configure a Kafka producer and @KafkaListener in Spring Boot?**

spring-kafka: KafkaTemplate.send(topic, key, payload). Producer: acks=all, enable.idempotence=true, JsonSerializer/Avro.
@KafkaListener(topics, groupId, concurrency). concurrency should be ≤ partition count. Manual ack or DefaultErrorHandler + DLT. Do not set concurrency higher than partitions. Test with @EmbeddedKafka or Testcontainers.
