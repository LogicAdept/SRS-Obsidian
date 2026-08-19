<!--
reps: 0
priority: 0
-->
#Java/Spring/Data #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

PagingAndSortingRepository extends CrudRepository and adds paginated and sorted access:

```java
public interface PagingAndSortingRepository<T, ID> extends CrudRepository<T, ID> {
    Iterable<T> findAll(Sort sort);
    Page<T> findAll(Pageable pageable);
}
```

Dump usage: Sort.by / Sort.Direction and PageRequest of page index plus size; then page.getTotalPages() and nextPageable().
> [!warning] Unverified traps from the dump
> - Page index in dump examples is zero-based.
> - JpaRepository and MongoRepository include this surface rather than forcing you to extend PagingAndSortingRepository yourself.
