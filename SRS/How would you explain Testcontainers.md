<!--
reps: 0
priority: 0
-->
#Java/Testing/Testcontainers #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Testcontainers.**

Реальные БД/Kafka в Docker из тестов. @Testcontainers + @Container PostgreSQLContainer. Зачем: тесты на реальной PostgreSQL, а не H2 (которая отличается). Проверка миграций Flyway, SQL, Kafka-consumers.

**Testcontainers — что это?**

Библиотека для запуска Docker-контейнеров из Java-тестов. PostgreSQLContainer, KafkaContainer, GenericContainer (WireMock). @Testcontainers + @Container. Для AQA: поднять реальную БД вместо H2, реальный Kafka вместо embedded. Reusable containers для ускорения.
