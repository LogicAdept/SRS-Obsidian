<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC/Autowiring #Java/Annotations #SRS

# Can `@Qualifier` be used on a class instead of a `@Component` name?

> [!abstract] Short answer
> **Yes.** On a scanned `@Component`, type-level `@Qualifier` (or a custom qualifier) is **qualifier metadata** for autowire narrowing. It is **not** a second way to set the bean name. `@Component("name")` still names the bean; `@Qualifier("value")` on the class is a separate label that injection points match after a type match.

## Bean name and qualifier are different knobs

`@Component.value` is a **suggested bean name** for an autodetected component. If you omit it, the default name generator uses the decapitalized short class name (`actionMovieCatalog` for `ActionMovieCatalog`).

`@Qualifier` (Spring 2.5+) is legal on **fields, methods, parameters, types, and other annotations**. On a **candidate class**, it does not rename the bean. It attaches a semantic qualifier that `QualifierAnnotationAutowireCandidateResolver` matches against `@Qualifier` (or a custom qualifier) on the injection point.

```java
@Component                          // bean name: actionMovieCatalog
@Qualifier("Action")                // qualifier value: Action
public class ActionMovieCatalog implements MovieCatalog {
}
```

**Listing 1.** Conceptual: stereotype for registration, type-level `@Qualifier` for autowire narrowing. The default bean name stays `actionMovieCatalog`.

At the injection point you match the **qualifier**, not the generated name:

```java
@Autowired
@Qualifier("Action")
private MovieCatalog movieCatalog;
```

**Listing 2.** Conceptual injection point: type match first (`MovieCatalog`), then narrow by qualifier `"Action"`.

You can still write `@Component("Action")` and inject with `@Qualifier("Action")`. That works because a qualifier `value` **falls back** to the bean name or an alias when no explicit qualifier attribute matches. The container still treats this as **type-driven injection with optional narrowing**, not as “look up this unique id”. Prefer qualifier values that describe the component (`Action`, `main`, `EMEA`) rather than copying an auto-generated bean id.

```d2
direction: down
type: "1. Candidates by type\n(MovieCatalog beans)" {
  width: 280
  height: 80
  style.fill: "#e3f2fd"
}
qual: "2. Narrow by qualifier\n(class / @Bean / XML metadata)" {
  width: 300
  height: 80
  style.fill: "#fff3e0"
}
name: "Fallback: qualifier value\nmatches bean name or alias?" {
  width: 280
  height: 80
  style.fill: "#fff8e1"
}
one: "One remaining candidate\n→ inject it" {
  width: 260
  height: 70
  style.fill: "#e8f5e9"
}
many: "Still several\n→ NoUniqueBeanDefinitionException\nunless @Primary / name match" {
  width: 300
  height: 90
  style.fill: "#ffebee"
}

type -> qual
qual -> name: no explicit qualifier match
qual -> one: unique after qualifier
qual -> many: qualifier is only a filter
name -> one: name / alias matches
name -> many: no unique remaining bean
```

**Fig. 1.** `@Autowired` selects by type, then qualifier metadata. Bean name is a fallback for the qualifier `value`, not the primary meaning of `@Qualifier` on a class.

## Custom qualifiers on the class

You can meta-annotate your own annotation with `@Qualifier` and put **that** on the component class (for example `@Genre("Action")` or a marker such as `@Offline`).

```java
@Target({ElementType.TYPE, ElementType.FIELD, ElementType.PARAMETER})
@Retention(RetentionPolicy.RUNTIME)
@Qualifier
public @interface Genre {
    String value();
}

@Component
@Genre("Action")
public class ActionMovieCatalog implements MovieCatalog {
}
```

**Listing 3.** Conceptual custom qualifier used as class-level metadata. Include `ElementType.TYPE` if the annotation must sit on the component class.

> [!warning] `@Target` must include `TYPE` for class use
> A custom qualifier declared only for `FIELD` and `PARAMETER` **cannot** be placed on a class. Expand `@Target` when the same annotation is the class-level metadata.

Qualifiers are **filters**, not unique keys. Several `MovieCatalog` beans may share `@Qualifier("Action")`; a `Set<MovieCatalog>` (or other typed collection) annotated with that qualifier receives **all** of them.

## `@Bean` methods and XML: per definition, not per class

Class-level annotation metadata is **bound to the class**. Two beans of the same class cannot carry different type-level `@Qualifier` values.

For per-definition labels, put `@Qualifier` on each `@Bean` method (or use XML `<qualifier value="…"/>` / `<meta/>`):

```java
@Configuration
public class CatalogConfig {

    @Bean
    @Qualifier("main")
    MovieCatalog mainCatalog() {
        return new SimpleMovieCatalog();
    }

    @Bean
    @Qualifier("action")
    MovieCatalog actionCatalog() {
        return new SimpleMovieCatalog();
    }
}
```

**Listing 4.** Conceptual: method-level `@Qualifier` labels two beans of the same class. XML can do the same per `<bean>` because qualifier metadata there is per instance.

See [[What is the Spring Bean annotation]] for factory methods, and [[How do you choose among several matching beans with Primary and Qualifier]] for the default-versus-explicit choice.

## `@Primary` keeps a default; `@Qualifier` keeps both selectable

If several beans share a type, a single-valued injection point is ambiguous. `@Primary` (since 3.0) marks the candidate used when **exactly one** primary remains among the type matches and the injection point does not demand another qualifier. The other beans stay in the context.

`@Qualifier` on the class (or `@Bean` method) plus `@Qualifier` at the injection point lets you **keep both** and choose explicitly — including injecting the non-primary bean. `@Primary` does not apply to arrays, collections, maps, or `ObjectProvider` streams: every type match is included there.

> [!warning] `@Qualifier` does not rename the bean
> `applicationContext.getBean("Action")` looks up a **bean name**, not a qualifier. Listing 1 is still named `actionMovieCatalog` unless you also set `@Component("Action")`. Mixing the two is the usual interview mix-up.

## Not the same as `@Resource(name = …)`

JSR-250 / Jakarta `@Resource(name = "…")` is **by-name** lookup: the declared type is irrelevant to matching. `@Autowired` + `@Qualifier` is the opposite order: type first, then a string qualifier **within that type set**.

`@Resource` is supported on fields and single-argument setters. Constructor and multi-argument method parameters should use qualifiers. Contrast: [[What is the difference between Autowired Resource and Inject]]. Constructor parameters: [[Why is constructor injection preferred in Spring]].

> [!tip] Interview answer
> Yes — put `@Qualifier` on the `@Component` class (or a custom qualifier meta-annotated with `@Qualifier`). That is autowire metadata, not the bean name; `@Component("name")` still names the bean, and a qualifier string only falls back to that name. Use `@Primary` for a default among several types, and put `@Qualifier` on each `@Bean` method when two beans share one class.
