<!--
reps: 0
priority: 0
-->
#Java/IO #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Что такое SEQUENCE?**

Oracle: SEQUENCE — отдельный объект БД, генератор уникальных чисел. Используется для auto-increment ID: INSERT VALUES (my_seq.nextval, ...). Postgres: аналог — SERIAL или IDENTITY. SERIAL — алиас для INTEGER + sequence. IDENTITY (SQL стандарт) — более явный. MySQL: AUTO_INCREMENT.
