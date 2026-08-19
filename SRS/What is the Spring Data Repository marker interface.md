<!--
reps: 0
priority: 0
-->
#Java/Spring/Data #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Repository<T, ID> is the central marker interface. T is the domain type, ID is the identifier type. It does not declare CRUD methods by itself.

CrudRepository extends it and adds save, findById, findAll, count, deleteById. PagingAndSortingRepository extends CrudRepository and adds findAll(Pageable) and findAll(Sort). Store modules add JpaRepository, MongoRepository, and similar.
> [!warning] Unverified traps from the dump
> - Extending the empty Repository marker is enough to get query methods without the full CRUD set.
> - CrudRepository is in spring-data-commons and is store-agnostic in these dumps.
