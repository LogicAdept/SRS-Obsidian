<!--
reps: 0
priority: 0
-->
#Java/Spring/Data #Java/Annotations #API/REST #SRS

# What is the RepositoryRestResource annotation?

> [!abstract] Short answer
> **`@RepositoryRestResource`** customizes how **Spring Data REST** exports a repository: URL **`path`**, HAL link **`rel`**s, optional **`excerptProjection`**, and whether the repository is **`exported`** at all. Method-level tweaks and hiding individual finders/CRUD ops use **`@RestResource`**.

## What it configures

Place it on a Spring Data repository interface that the REST exporter would otherwise expose under a pluralized domain-type path (e.g. `/persons`).

```java
@RepositoryRestResource(path = "people", collectionResourceRel = "people")
interface PersonRepository extends CrudRepository<Person, Long> {

  @RestResource(path = "names", rel = "names")
  List<Person> findByName(String name);
}
```

**Listing 1.** Collection at `/people`; finder at `/people/search/names` (Spring Data REST URL-path docs).

| Attribute | Role |
| --- | --- |
| `path` | URL segment for the collection |
| `collectionResourceRel` / `itemResourceRel` | Link relation names in HAL `_links` |
| `exported` | `false` → do not export this repository |
| `excerptProjection` | Projection type when embedding items in collections |
| `*Description` | ALPS/description metadata |

```d2
direction: right
repo: "PersonRepository" {
  style.fill: "#e3f2fd"
}
ann: "@RepositoryRestResource\npath / rel / exported" {
  style.fill: "#fff3e0"
}
http: "/people\n/people/{id}\n/people/search/…" {
  style.fill: "#e8f5e9"
}

repo -> ann -> http
```

**Fig. 1.** Annotation reshapes the generated REST surface without writing a `@RestController`.

## Hiding and overrides

- Whole repository: `@RepositoryRestResource(exported = false)`.
- One finder or field: `@RestResource(exported = false)` on the method/field.
- Hide delete/save: override the `CrudRepository` methods and annotate those overrides (often **both** delete overloads).

Deeper customization (controllers, events) is covered in [[How can you customize Spring Data REST endpoints]] and [[How do you hide a Spring Data REST endpoint]].

> [!warning] Not a Spring MVC stereotype
> `@RepositoryRestResource` is **not** `@RestController` / `@RequestMapping`. It only affects the **Spring Data REST exporter**. A plain repository without Spring Data REST on the classpath ignores it for HTTP.

> [!warning] Projections can re-expose fields
> Docs note that projections can side-step field-level `exported = false`. If you hide a property on the entity, keep projections from putting it back on the wire.

> [!tip] Interview answer
> `@RepositoryRestResource` tells Spring Data REST how to export a repository — path, link rels, and whether it is exported. I use `path`/`rel` to rename `/persons` to `/people`, `exported = false` to hide a repository, and `@RestResource` on methods for finder paths or to turn off specific CRUD HTTP operations.

See [[What is Spring Data REST]], [[How can you customize Spring Data REST endpoints]], and [[How do you hide a Spring Data REST endpoint]].
