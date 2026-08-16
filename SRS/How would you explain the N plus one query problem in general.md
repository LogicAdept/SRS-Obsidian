<!--
reps: 0
priority: 0
-->
#Problems/Persistence #Databases #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**N+1 — детально.**

1 findAll() + N доп. запросов на lazy-коллекции. 1000 заказов → 1001 SQL. Обнаружение: hibernate.generate_statistics=true, datasource-proxy. Решения: JOIN FETCH, @EntityGraph, @BatchSize(100), @Fetch(FetchMode.SUBSELECT), DTO-проекция. EAGER — неправильный ответ.

**Проблема N+1.**

При итерации по списку на каждую связанную сущность делается отдельный SELECT. Решения: JOIN FETCH, @EntityGraph, @BatchSize, @Fetch(FetchMode.SUBSELECT).

**Что такое N+1?**

Загрузил список из N сущностей одним запросом. Потом в цикле обращаешься к их LAZY-связям — на каждую идёт отдельный SELECT. Итого 1 + N запросов. На 100 сущностях это 101 запрос — катастрофа для производительности.

**Как решить N+1?**

(1) JPQL с JOIN FETCH: select o from Order o join fetch o.user. (2) @EntityGraph — атрибут на репозиторий-методе, говорит «подгрузить эти поля сразу». (3) Hibernate batch_size — группирует SELECT'ы по пачкам. (4) DTO-проекция через JPQL select new com.x.OrderDto(...) — сразу плоский результат без загрузки entity.

**N+1 проблема в Spring Data JPA.**

При fetch = LAZY на связи, при итерации по списку делается +1 запрос за каждую связанную сущность. Решения: JOIN FETCH, @EntityGraph, BatchSize.

**N+1 в JPA — как диагностировать?**

Включить логи SQL (spring.jpa.show-sql=true), смотреть количество запросов на эндпоинт, использовать p6spy или Hibernate Statistics.

**N+1 проблема.**

1 findAll() + N доп. запросов на lazy-коллекции. Решения: JOIN FETCH, @EntityGraph, @BatchSize(100), DTO-проекция. EAGER — неправильный ответ.

**N+1 SQL rewrite?**

Batch with JOIN / IN / ANY. Index children by parent_id. Avoid JOIN that multiplies then DISTINCT. APM: N similar queries, not one slow SQL.
