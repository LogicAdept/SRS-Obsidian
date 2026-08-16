<!--
reps: 0
priority: 0
-->
#Java/Persistence #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Какие способы работы с БД в Java?**

JDBC — низкий уровень, прямой SQL и работа с ResultSet. JPA / Hibernate — ORM, маппинг объектов на таблицы. jOOQ — typesafe SQL builder, generated code. Spring Data — удобная обёртка над JPA, query methods. Всё в итоге работает через JDBC-драйвер.
