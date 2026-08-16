<!--
reps: 0
priority: 0
-->
#Java/Persistence/JPA #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Чем отличается JpaRepository от CrudRepository?**

JpaRepository extends PagingAndSortingRepository extends CrudRepository. Добавляет flush(), saveAllAndFlush(), работу с List вместо Iterable, deleteAllInBatch.
