<!--
reps: 0
priority: 0
-->
#Java/Persistence/JPA #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Какой Fetch type по умолчанию?**

Для коллекций (@OneToMany, @ManyToMany) — Lazy. Для скалярных связей (@OneToOne, @ManyToOne) — Eager. Eager по умолчанию для @ManyToOne — частая ловушка: при загрузке Order сразу подтянется User, а если у User тоже есть @ManyToOne — и его связь. Может уйти каскадом.
