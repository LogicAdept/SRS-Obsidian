<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC/Autowiring #Java/Annotations #SRS

# What is the Required annotation in Spring?

> [!abstract] Short answer
> `@Required` (since **2.0**, **`@Target(METHOD)`**) marked a JavaBean **setter** as a property that **must be populated at configuration time** (XML `<property>`, autowiring, or any other container injection). `RequiredAnnotationBeanPostProcessor` checked that the setter was **configured with a value** and failed startup if it was not. **Deprecated in 5.1**, **removed in Spring Framework 6** (current 7 Javadoc has no type). Prefer **constructor injection** ([[Why is Autowired often omitted on a single constructor in modern Spring]]) or `InitializingBean` / `@PostConstruct` assertions.

## Configuration-time check, not “non-null”

```java
public class SimpleMovieLister {

    private MovieFinder movieFinder;

    @Required
    public void setMovieFinder(MovieFinder movieFinder) {
        this.movieFinder = movieFinder;
    }
}
```

**Listing 1.** Conceptual (pre-6.0). Missing `movieFinder` → the processor aborts initialization (`BeanInitializationException`: property required for that bean). The 5.3 reference still recommended **your own** init-method assertions so the class stays safe **outside** the container.

The processor **does not** test that the injected value is non-`null`. A configured `null` satisfies `@Required`. It is not an init method and does not replace constructor injection.

Through **5.0**, `<context:annotation-config/>` and `<context:component-scan>` registered `RequiredAnnotationBeanPostProcessor` by default. As of **5.1**, `AnnotationConfigUtils` **stopped** registering it (`REQUIRED_ANNOTATION_PROCESSOR_BEAN_NAME` deprecated “since no Required processor is registered by default anymore”). The 5.3 reference: you had to **declare the processor yourself** if you still wanted `@Required`. Current `annotation-config` does not mention it ([[What does context annotation-config register]]).

`@Autowired`’s `required` flag is a **different** contract: it only governs **autowiring** of that injection point ([[What does Autowired required false do]]). `@Required` was **stronger**: the property had to be set **by any** container mechanism. 5.x docs already recommended `@Autowired` / constructors over `@Required`.

```d2
direction: down
setter: "@Required setter" {
  width: 180
  height: 40
  style.fill: "#e3f2fd"
}
bpp: "RequiredAnnotationBeanPostProcessor" {
  width: 280
  height: 45
  style.fill: "#fff3e0"
}
ok: "property was configured" {
  width: 200
  height: 40
  style.fill: "#e8f5e9"
}
fail: "BeanInitializationException" {
  width: 220
  height: 40
  style.fill: "#ffebee"
}

setter -> bpp
bpp -> ok
bpp -> fail
```

**Fig. 1.** Pre-6.0: a `BeanPostProcessor` checks configuration, not runtime null-safety.

> [!warning] Gone in Spring 6+
> Do not put `@Required` on a Framework **6/7** codebase — the annotation and processor **do not exist**. Interview dumps that still list it next to `@Autowired` on `annotation-config` describe **Spring 5.0 and earlier**.

> [!warning] Configured is not non-null
> XML `<property name="movieFinder"><null/></property>` counts as configured. `@Required` will not save you from an NPE. Constructors (or an init check) will.

> [!tip] Interview answer
> Required was a 2.0 setter marker: RequiredAnnotationBeanPostProcessor failed the bean if that property was never populated. It did not check for null, was deprecated in 5.1, dropped from default annotation-config then, and removed in Spring 6. Today you make dependencies required with constructors, not @Required.
