<!--
reps: 0
priority: 0
-->
#Java/Spring/Data #API/REST #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Spring Data REST exposes Spring Data repositories as hypermedia-driven (HATEOAS) REST APIs so you skip repetitive @RestController CRUD.

With the module on the classpath and a repository declared:

```java
@RepositoryRestResource(collectionResourceRel = "people", path = "people")
public interface PersonRepository extends PagingAndSortingRepository<Person, Long> {
    List<Person> findByLastName(@Param("name") String name);
}
```

Generated endpoints in the dump: GET/POST /people, GET/PUT/DELETE /people/{id}, and GET /people/search/findByLastName?name=Smith for the finder.
> [!warning] Unverified traps from the dump
> - Finder methods become /search/... resources, not extra POST mappings.
> - This is a separate Spring Data module, not something JpaRepository does alone.
