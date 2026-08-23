<!--
reps: 0
priority: 0
-->
#Java/Spring/Data #Java/Annotations #API/REST #SRS

# How do you hide a Spring Data REST endpoint?

> [!abstract] Short answer
> Set `@RepositoryRestResource(exported = false)` on the repository interface to drop the whole resource, or `@RestResource(exported = false)` on a query method or an overridden CRUD method. The Spring bean remains injectable — only the HTTP export disappears.

## Hide a repository or a method

Spring Data REST auto-exports public repositories. `exported = false` tells the exporter to skip that scope.

```java
@RepositoryRestResource(exported = false)
interface InternalJobRepository extends CrudRepository<Job, Long> {}

@RepositoryRestResource(path = "people")
interface PersonRepository extends CrudRepository<Person, Long> {

  @RestResource(exported = false)
  List<Person> findBySocialSecurityNumber(String ssn);

  @Override
  @RestResource(exported = false)
  void deleteById(Long id);

  @Override
  @RestResource(exported = false)
  void delete(Person entity);
}
```

**Listing 1.** Hide an entire repository or selected finders / CRUD methods (Spring Data REST “Hiding Certain Repositories, Query Methods, or Fields”).

For `CrudRepository` deletes, Spring Data REST docs require **both** `delete` overloads to be overridden and annotated if you want HTTP `DELETE` off — the exporter’s method selection is not fine-grained enough to hide only one variant.

Remaining exported finders are exposed under **`/search/…`** (default segment `search`, method segment from the finder name unless you set `@RestResource(path = …)`).

```d2
direction: down
repo: "Repository interface" {
  width: 220
  height: 70
  style.fill: "#e3f2fd"
}
hideAll: "@RepositoryRestResource\n(exported = false)" {
  width: 280
  height: 70
  style.fill: "#ffebee"
}
hideOne: "@RestResource(exported = false)\non method / field" {
  width: 280
  height: 70
  style.fill: "#fff3e0"
}
http: "No HAL resource\nJava API unchanged" {
  width: 240
  height: 70
  style.fill: "#e8f5e9"
}

repo -> hideAll -> http
repo -> hideOne -> http
```

**Fig. 1.** Export flags affect HTTP mapping only; the repository bean is still a normal Spring Data interface.

You can also put `@RestResource(exported = false)` on **entity fields** (for example a password) so they are not serialized — projections can still expose fields unless you design them carefully.

> [!warning] Hiding is not securing
> `exported = false` removes the REST route from the exporter; it is **not** Spring Security. Callers with repository access can still invoke the method in-process. For authentication and authorization use security rules, not export flags alone.

See [[What is the RepositoryRestResource annotation]], [[How can you customize Spring Data REST endpoints]], and [[What is Spring Data REST]].

> [!tip] Interview answer
> To hide a Spring Data REST endpoint I set `exported = false` — on the repository to drop the whole resource, or on individual finder/CRUD methods. For delete I override and annotate both delete methods. The repository still works for injection; only HTTP export is gone, and that is not a substitute for security.
