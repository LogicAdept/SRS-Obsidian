<!--
reps: 0
priority: 0
-->
#Java/Spring/Data/JPA #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Что такое Spring Data JPA?**

Модуль, который позволяет работать с БД через интерфейсы-репозитории. Достаточно унаследоваться от JpaRepository<Entity, ID> — Spring сам сгенерирует реализацию.

**Что такое Spring Data JPA?**

Удобная обёртка над JPA / Hibernate. Создаёшь интерфейс, наследуешь JpaRepository — Spring сам сгенерирует реализацию. Query methods: метод findByEmail — Spring сам соберёт SQL по имени. @Query — кастомный JPQL или native SQL. Pageable — пагинация и сортировка. public interface UserRepository extends JpaRepository<User, Long> { // Метод сам генерируется по имени Optional<User> findByEmail(String email); List<User> findByAgeGreaterThanOrderByNameAsc(int age);
