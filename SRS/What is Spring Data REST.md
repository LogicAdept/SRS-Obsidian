<!--
reps: 0
priority: 0
-->
#Java/Spring/Data #API/REST #SRS

# What is Spring Data REST?

> [!abstract] Short answer
> **Spring Data REST** is a separate module that **exports Spring Data repositories as hypermedia-driven HTTP resources** (HAL by default). You declare repositories; it maps collection/item CRUD and finder methods to REST endpoints so you avoid hand-written `@RestController` boilerplate for basic CRUD.

## What gets exposed

With the module on the classpath (e.g. Boot `spring-boot-starter-data-rest`) and an exported repository:

```java
@RepositoryRestResource(collectionResourceRel = "people", path = "people")
public interface PersonRepository extends CrudRepository<Person, Long> {

  List<Person> findByLastName(@Param("name") String name);
}
```

**Listing 1.** Repository customized with path/rel; query methods become search resources (Spring Data REST repository-resources docs).

Default shape for a `Person` / `CrudRepository`:

| Resource | Example | Typical HTTP |
| --- | --- | --- |
| Collection | `/people` | `GET`, `POST` |
| Item | `/people/{id}` | `GET`, `PUT`, `PATCH`, `DELETE` |
| Search index | `/people/search` | `GET` (links to finders) |
| Query method | `/people/search/findByLastName?name=…` | `GET` |

Path defaults to the uncapitalized plural domain type name unless `@RepositoryRestResource` / `@RestResource` override it. Exposure follows **which repository methods exist** — missing or `@RestResource(exported = false)` methods omit the matching HTTP verbs.

```d2
direction: right
repo: "Spring Data\nRepository" {
  style.fill: "#e3f2fd"
}
sdr: "Spring Data REST\nexporter" {
  style.fill: "#fff3e0"
}
hal: "HAL JSON\n_links" {
  style.fill: "#e8f5e9"
}
client: "HTTP client" {
  style.fill: "#f3e5f5"
}

repo -> sdr -> hal -> client
```

**Fig. 1.** Repositories are exported as discoverable hypermedia resources; clients start from the API root `_links`.

## Not the same as JPA alone

`JpaRepository` / `MongoRepository` do **not** publish HTTP by themselves. Spring Data REST is an **extra** module on top of repositories. Customize or hide endpoints with annotations and config — see [[How can you customize Spring Data REST endpoints]] and [[How do you hide a Spring Data REST endpoint]].

> [!warning] Finders live under `/search`
> Derived/`@Query` methods are **not** arbitrary `POST` mappings. They appear as **search** sub-resources (e.g. `/people/search/findByLastName`). Clients discover them via the collection’s `search` link.

> [!warning] Export is a security surface
> Every exported repository is a public CRUD API unless you lock it down (security, `exported = false`, projections). Do not assume “repository for internal use only” when Spring Data REST is on the classpath.

> [!tip] Interview answer
> Spring Data REST turns Spring Data repositories into HAL REST resources automatically — collection and item URLs plus `/search` for query methods. It is a separate module, not something `JpaRepository` does alone. I customize paths with `@RepositoryRestResource` and hide sensitive operations with `@RestResource(exported = false)`.

See [[How can you customize Spring Data REST endpoints]], [[What is the RepositoryRestResource annotation]], and [[How do you hide a Spring Data REST endpoint]].
