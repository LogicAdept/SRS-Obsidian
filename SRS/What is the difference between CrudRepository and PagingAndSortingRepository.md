<!--
reps: 0
priority: 0
-->
#Java/Spring/Data #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

CrudRepository: fundamental CRUD only; findAll returns Iterable; no pagination API.

PagingAndSortingRepository: extends CrudRepository; adds findAll(Sort) and findAll(Pageable) so you can page and sort without a store-specific repository.

Store modules such as JpaRepository extend the paging type and add flush, saveAndFlush, and List-returning findAll.
> [!warning] Unverified traps from the dump
> - Choosing CrudRepository is the dump's advice when you do not need paging, sorting, or JPA flush APIs.
> - Pagination also appears as Pageable parameters on derived methods, not only on findAll.
