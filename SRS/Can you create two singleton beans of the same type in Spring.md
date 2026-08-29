<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC/Scopes #Java/Spring/Core/IoC/Autowiring #SRS

# Can you create two singleton beans of the same type in Spring?

> [!abstract] Short answer
> **Yes.** Identity is the **bean name** (unique in that container), not the Java type. **Singleton** means one instance **per definition** per container, not “one object of that class in the JVM.” Two `<bean>` / `@Bean` recipes with the same `class` (or the same interface) are two singletons. What **fails** is a **single-valued type match** with no disambiguation: `getBean(MovieCatalog.class)`, XML `autowire="byType"`, or `@Autowired MovieCatalog` → `NoUniqueBeanDefinitionException`. Fix with **names** (`getBean("first")`), `@Primary`, `@Qualifier`, or inject `List`/`Map` of that type.

## Two recipes, two instances

Every bean has one or more identifiers ([[What is the difference between a Spring bean id and a bean alias]]). The container is happy to host `jpaMovieFinder` and `stubMovieFinder` both implementing `MovieFinder`, each `scope="singleton"` (the default).

```java
@Configuration
public class MovieConfiguration {

    @Bean
    @Primary
    public MovieCatalog firstMovieCatalog() { return new FirstCatalog(); }

    @Bean
    public MovieCatalog secondMovieCatalog() { return new SecondCatalog(); }
}
```

**Listing 1.** Conceptual, after the Framework `@Primary` example. Two singleton `MovieCatalog` beans. A single-valued `@Autowired MovieCatalog` receives **`firstMovieCatalog`**. Without `@Primary` or `@Qualifier`, that injection point is fatal.

```xml
<bean id="jpaFinder" class="example.JpaMovieFinder"/>
<bean id="stubFinder" class="example.JpaMovieFinder"/>
```

**Listing 2.** Conceptual. Same class, two ids, two objects. Explicit `ref="jpaFinder"` is unambiguous. `autowire="byType"` on a single `MovieFinder` property is not ([[What XML autowiring modes exist in Spring]]).

`getBean("jpaFinder")` returns one; `getBean(JpaMovieFinder.class)` throws if both exist. Arrays, typed collections, and `Map<String, MovieCatalog>` **collect all** candidates (keys = bean names).

**Not** two beans: extra **aliases** for one definition (`@Bean({"a", "b"})`, XML `name` / `<alias>`) — same instance. Two `@Component` classes that **decapitalize to the same default name** clash on the **id**, which is a different error than “two types.” Give `@Component("other")` or use two `@Bean` methods.

```d2
direction: down
type: "type MovieCatalog" {
  width: 180
  height: 36
  style.fill: "#e3f2fd"
}
a: "singleton firstMovieCatalog" {
  width: 240
  height: 40
  style.fill: "#e8f5e9"
}
b: "singleton secondMovieCatalog" {
  width: 260
  height: 40
  style.fill: "#fff3e0"
}

type -> a
type -> b
```

**Fig. 1.** Type is a lookup key for autowiring, not a uniqueness constraint on definitions.

> [!warning] Same type is legal; same **name** is not
> Duplicate ids / generated component names fail registration. Duplicate types fail only **by-type** injection and `getBean(Class)`.

> [!warning] `@Primary` needs exactly one winner
> Two `@Primary` beans of that type is still ambiguous. `@Qualifier` (or a named `@Resource`) picks one among type matches ([[What is the difference between Autowired Resource and Inject]]).

> [!tip] Interview answer
> Yes — singleton is per bean definition, not per class. Register two beans with different names and the same type freely. Autowiring and getBean by type then need Primary, Qualifier, a name, or a collection. Aliases are extra names for one instance, not a second singleton.
