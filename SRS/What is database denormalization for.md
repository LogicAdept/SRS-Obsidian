<!--
reps: 0
priority: 0
-->
#Databases/NormalForms #Databases/SQL #SystemDesign/Tradeoffs #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Что такое ORM?**

Object-Relational Mapping — маппинг Java-объектов на таблицы. Hibernate — реализация JPA. Позволяет работать с БД через объекты. НО: всегда следи за тем, какой SQL реально выполняется (Hibernate может генерировать неоптимальные запросы — включи hibernate.show_sql).

**Что такое ORM?**

Object-Relational Mapping — маппинг объектов на таблицы БД. Позволяет работать с БД как с объектами, не писать SQL руками.

**Что такое ORM?**

Object-Relational Mapping — отображение объектов на таблицы БД. Класс User → таблица users, поля → колонки, связи (@OneToMany) → JOIN'ы. Hibernate берёт на себя SQL — разработчик работает с объектами. Плюс — меньше boilerplate, минус — нужно понимать, что Hibernate генерирует под капотом.
