<!--
reps: 0
priority: 0
-->
#Java/Language #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Liquibase vs Flyway?**

Liquibase — описание изменений в XML / YAML, поддерживает rollback, кросс-БД (одно описание — для разных БД). Flyway — версионированные SQL-скрипты (V1__init.sql, V2__add_table.sql), проще, но без rollback и кросс-БД. Сбер любит Liquibase, многие стартапы — Flyway.
