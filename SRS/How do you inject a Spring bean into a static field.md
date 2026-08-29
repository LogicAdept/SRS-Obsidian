<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC/Autowiring #Java/Annotations #SRS

# How do you inject a Spring bean into a static field?

> [!abstract] Short answer
> You do not. `@Autowired`, `@Value`, and `@Inject` run through `AutowiredAnnotationBeanPostProcessor`, which **skips** `static` fields and methods (info log: not supported) and never assigns them. `@Resource` / `@EJB` on a static member **throw**. To copy a bean into a class field, autowire a **non-static** constructor or config method and assign the static field yourself — or, better, keep an instance field.

## Injection targets a bean instance

`@Autowired` marks a constructor, **instance** field, setter, or config method on a managed bean. Fields are filled **right after construction**, before config methods. That is instance lifecycle, not class initialization.

`AutowiredAnnotationBeanPostProcessor.buildAutowiringMetadata` walks fields and methods. If `Modifier.isStatic` is true, it logs at **INFO** and `return`s without creating an `AutowiredFieldElement` / `AutowiredMethodElement`. The member is not in the injection list, so `required = true` never runs: startup **succeeds**, the static reference stays at its initializer (typically `null`).

`CommonAnnotationBeanPostProcessor` is stricter: `@Resource` or `@EJB` on a static field or method throws `IllegalStateException` (`@Resource annotation is not supported on static fields`).

```d2
direction: down
ann: "@Autowired on static field\n(legal Java, compiles)" {
  width: 280
  height: 70
  style.fill: "#fff3e0"
}
skip: "BPP skips member\nINFO log, no inject" {
  width: 260
  height: 70
  style.fill: "#ffebee"
}
null: "Field stays default\n(usually null)" {
  width: 240
  height: 55
  style.fill: "#ffebee"
}
inst: "Non-static @Autowired\nctor / config method" {
  width: 260
  height: 70
  style.fill: "#e3f2fd"
}
copy: "Method body assigns\nthe static field" {
  width: 240
  height: 55
  style.fill: "#e8f5e9"
}

ann -> skip -> null
inst -> copy
```

**Fig. 1.** The annotation on a static field is a no-op. Only an **instance** injection point can receive a bean; any write to a `static` field is ordinary Java after that.

Do not confuse this with **`static @Bean` methods** on a `@Configuration` class. Those are factory methods that avoid a self-reference on the configuration instance. They do not inject into static fields.

## Copy from an instance injection point

If legacy code truly needs a class-level holder, register a bean and autowire an **instance** member, then assign:

```java
@Component
public class MovieCatalogHolder {

    private static MovieCatalog movieCatalog;

    @Autowired
    public void setMovieCatalog(MovieCatalog movieCatalog) {
        MovieCatalogHolder.movieCatalog = movieCatalog;
    }
}
```

**Listing 1.** Conceptual. Spring injects the **method** (any name, any number of arguments — see [[Can Autowired be applied to methods other than constructors and setters]]). The static write is not container injection. A constructor parameter works the same way.

The holder class **must** be a Spring bean, or the setter never runs. Prefer a normal instance field and constructor injection instead ([[Why is Autowired often omitted on a single constructor in modern Spring]]).

Class initialization runs before the first instance is created (and before any static use). A static initializer, or any code that reads the holder during another class’s init, still sees `null` even if a setter will later fill it. Populate-then-init order is the usual bean timeline ([[How do you call a method after a Spring bean is initialized]]); it does not move class-init earlier.

> [!warning] `@Autowired` on `static` does not fail the context
> The processor drops the member instead of treating it as an unsatisfied dependency. You get a later `NullPointerException`, not `UnsatisfiedDependencyException`. Raise logging for `AutowiredAnnotationBeanPostProcessor` to INFO if you need the skip message. `@Resource` on the same static field fails fast with `IllegalStateException`.

> [!warning] The static field outlives the bean
> Destroy callbacks and context close do not clear it unless you write that. A second `ApplicationContext` in the same JVM can overwrite the same class field. Tests that reuse the JVM keep the last assignment.

> [!tip] Interview answer
> Spring autowires instance members through a BeanPostProcessor; static fields and methods are skipped, so @Autowired on a static field stays null and does not fail startup. If you must fill a static holder, autowire a non-static setter or constructor and assign the field in Java. Prefer instance injection so the dependency follows the bean lifecycle.
