<!--
reps: 0
priority: 0
-->
#Java/Spring/Data #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

CrudRepository<T, ID> extends Repository<T, ID> and provides basic CRUD: save, findById, existsById, findAll, deleteById, count (and other methods).

It lives in spring-data-commons. findAll returns Iterable. Dumps call it database-agnostic (usable for JPA, MongoDB, and others).

```java
public interface StudentRepository extends CrudRepository<Student, Long> {
}
```
> [!warning] Unverified traps from the dump
> - JpaRepository is the JPA-specific subtype; CrudRepository is the shared CRUD contract.
> - findAll on CrudRepository is Iterable, not List.
