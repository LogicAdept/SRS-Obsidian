<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC/Lifecycle #Java/Annotations #SRS

# What is the DependsOn annotation in Spring?

> [!abstract] Short answer
> `@DependsOn` (since **3.0**) names beans the container must **create first**, when there is **no** constructor/`ref`/`@Autowired` edge — only a **side effect** of the other bean’s initialization (for example a static initializer / driver registration). XML’s `depends-on` is the same contract. For **singletons**, it also sets **destroy order**: beans that `@DependsOn` X are destroyed **before** X. Ordinary injection already initializes the collaborator (including `@PostConstruct` / `afterPropertiesSet` / `init-method`) before it is injected — you do **not** add `@DependsOn` for that ([[How would you explain dependency injection]], [[In what order do PostConstruct InitializingBean and init-method run]]).

## Side-effect order, not a substitute for DI

Place it on a `@Component` (or other stereotype) type, or on a `@Bean` method. The `value` is bean **names**.

```java
@Component
@DependsOn("driverRegistrar")
public class DataAccessBootstrap {
}
```

```java
@Bean
@DependsOn({"manager", "accountDao"})
ExampleBean beanOne() {
    return new ExampleBean();
}
```

**Listing 1.** Conceptual. Names, not types. Multiple names are an array on the annotation; in XML, commas, whitespace, or semicolons.

```xml
<bean id="beanOne" class="example.ExampleBean" depends-on="manager"/>
<bean id="manager" class="example.ManagerBean"/>
```

**Listing 2.** Conceptual. Class-level `@DependsOn` is **ignored** if this class is declared as XML `<bean>` — use the `depends-on` **attribute**. `@DependsOn` on a class **has no effect unless component scanning** (or an equivalent stereotype registration) creates the definition from that class.

`@DependsOn` is also how you pin order for `@Bean(bootstrap = BACKGROUND)`: the named beans initialize on the **main** bootstrap thread first.

`SmartLifecycle` start/stop still honor depends-on: the dependent **starts after** and **stops before** its dependency ([[How do you shut down a Spring ApplicationContext]]).

```d2
direction: down
dep: "manager\ncreated + init callbacks" {
  width: 240
  height: 55
  style.fill: "#e8f5e9"
}
bean: "beanOne (@DependsOn manager)\nthen created" {
  width: 260
  height: 55
  style.fill: "#e3f2fd"
}
stop: "Shutdown (singletons):\nbeanOne destroyed, then manager" {
  width: 280
  height: 55
  style.fill: "#fff3e0"
}

dep -> bean: startup
bean -> stop
```

**Fig. 1.** Init: dependency first. Destroy: **dependent** first, then the bean it depended on ([[What destroy callbacks does Spring invoke when a bean is destroyed]]).

> [!warning] XML `<bean>` does not read class-level `@DependsOn`
> Scanning picks up the annotation. An XML bean definition uses `depends-on="…"` instead. Forgetting that looks like “`@DependsOn` did nothing.”

> [!warning] Destroy ordering is singleton-only
> Prototype (and other non-singleton) `depends-on` is an **init** constraint only. The container does not apply the matching destroy-time pairing outside singletons.

> [!tip] Interview answer
> DependsOn forces named beans to be fully created before this one when you only care about their init side effects, not an injected reference. For singletons it also destroys the dependent beans first. You do not need it for constructor or autowired collaborators — those are already initialized first — and on a @Component class it only works with component scanning, not a plain XML bean tag.
