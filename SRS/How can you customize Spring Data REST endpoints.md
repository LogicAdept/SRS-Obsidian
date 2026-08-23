<!--
reps: 0
priority: 0
-->
#Java/Spring/Data #API/REST #SRS

# How can you customize Spring Data REST endpoints?

> [!abstract] Short answer
> Customize export with `@RepositoryRestResource` / `@RestResource`, tune global exposure through `RepositoryRestConfigurer`, replace or extend handlers with `@RepositoryRestController`, and hook lifecycle with repository event listeners. Plain `@RestController` sits outside Spring Data REST’s stack.

## Hide or reshape what is exported

`@RepositoryRestResource` on the repository sets collection `path` / `rel`, or turns export off with `exported = false`. On a finder or an overridden CRUD method, `@RestResource(exported = false)` keeps the Java API while removing the HTTP resource. Finder paths live under `/search/…` unless you rename them with `@RestResource(path = …, rel = …)`.

```java
@RepositoryRestResource(path = "people", rel = "people")
interface PersonRepository extends CrudRepository<Person, Long> {

  @RestResource(path = "names", rel = "names")
  List<Person> findByName(String name);

  @Override
  @RestResource(exported = false)
  void deleteById(Long id);

  @Override
  @RestResource(exported = false)
  void delete(Person entity);
}
```

**Listing 1.** Path/rel customization plus hiding both `delete` overloads (Spring Data REST docs: annotate every delete variant you want off).

When method-level export is too coarse (`save` backs `POST`, `PUT`, and `PATCH`), use `RepositoryRestConfiguration.getExposureConfiguration()` from a `RepositoryRestConfigurer` bean to disable specific HTTP methods per type or globally.

```java
@Component
class RestCustomization implements RepositoryRestConfigurer {

  @Override
  public void configureRepositoryRestConfiguration(
      RepositoryRestConfiguration config, CorsRegistry cors) {
    config.setBasePath("/api");
    config.getExposureConfiguration()
        .forDomainType(Person.class)
        .withItemExposure((metadata, httpMethods) ->
            httpMethods.disable(HttpMethod.PATCH));
  }
}
```

**Listing 2.** Base path plus type-scoped HTTP method exposure (Spring Data REST 3.1+ / Boot 2.1+ style API).

```d2
direction: down
annot: "@RepositoryRestResource\n/@RestResource" {
  width: 280
  height: 80
  style.fill: "#e3f2fd"
}
config: "RepositoryRestConfigurer\nbasePath · exposure · EntityLookup" {
  width: 300
  height: 90
  style.fill: "#fff3e0"
}
ctrl: "@RepositoryRestController\ncustom handlers under basePath" {
  width: 300
  height: 90
  style.fill: "#e8f5e9"
}
events: "AbstractRepositoryEventListener\nor @RepositoryEventHandler" {
  width: 300
  height: 90
  style.fill: "#f3e5f5"
}

annot -> config
config -> ctrl
ctrl -> events
```

**Fig. 1.** Common customization layers: annotations, configurer, custom controllers, then lifecycle events.

## Custom handlers and events

Prefer `@RepositoryRestController` (or `@BasePathAwareController`) so the handler uses Spring Data REST’s base path, converters, and exception handling. A normal `@RestController` / `@Controller` is outside that scope. Map into the repository URI space when you need to replace a generated handler; otherwise you only add parallel endpoints.

For validation or side effects on create/save/delete through the REST API, extend `AbstractRepositoryEventListener` (`onBeforeSave`, `onBeforeDelete`, …) or use a `@RepositoryEventHandler` POJO with `@HandleBeforeSave` / `@HandleBeforeCreate`. That changes behavior of the still-exported resources; it does not remove them. HAL representations can be adjusted with a `RepresentationModelProcessor`.

> [!warning] `exported = false` is not authorization
> Hiding a resource only drops the HTTP mapping. The repository bean remains injectable, and `exported = false` is not a substitute for Spring Security. Generated CRUD stays available until you hide methods, change exposure, or override the handler.

Related: [[What is Spring Data REST]], [[How do you hide a Spring Data REST endpoint]], and [[What is the RepositoryRestResource annotation]].

> [!tip] Interview answer
> I customize Spring Data REST with `@RepositoryRestResource` / `@RestResource` for paths and export, `RepositoryRestConfigurer` for base path and HTTP method exposure, `@RepositoryRestController` for custom handlers under the same API base path, and repository event listeners for before/after save or delete logic. I do not use a plain `@RestController` when I need Spring Data REST’s converters and exception handling, and I never treat `exported = false` as security.
