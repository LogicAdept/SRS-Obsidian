<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/AOP #Java/Annotations #SRS

# What is the `Configurable` annotation in Spring?

> [!abstract] Short answer
> **`@Configurable`** marks a class so Spring can **inject dependencies into instances the container did not create** (`new`, ORM). The work is **`AnnotationBeanConfigurerAspect`** in **`spring-aspects.jar`**, which requires **AspectJ weaving** (compile-time or LTW) plus **`@EnableSpringConfigured`**. The annotation **alone does nothing**. It is **not** a stereotype like `@Service`.

## DI after `new`, not a Spring bean

Spring *Using AspectJ to Dependency Inject Domain Objects*: the container can configure a **pre-existing** object from a bean definition. `@Configurable` opts a type into that. Simplest form is a marker: new `Account` instances are configured from a (usually **prototype**) definition named the **FQN** (`com.xyz.domain.Account`). `@Configurable("account")` uses a bean named `account` instead. Prefer **`@Autowired` / `@Inject`** on the domain type over `autowire=BY_TYPE|BY_NAME`. `dependencyCheck=true` then asserts non-primitive properties were set.

```java
@Configurable
public class Account {
    @Autowired
    private FundsTransferService fundsTransferService;
}
```

```java
@Configuration
@EnableSpringConfigured
public class ApplicationConfiguration {
}
```

**Listing 1.** Marker on the domain type; enable the aspect (`<context:spring-configured/>` in XML). Types must be **woven**. Enable LTW: [[How do you perform load-time weaving with AspectJ in a Spring application]]. Objects **not** in the container: [[Can you use Spring AOP with beans not managed by Spring]].

The aspect runs **after initialization** of a new object (and on **deserialization** / `readResolve()`). Constructor bodies **do not** see injected fields unless **`preConstruction = true`**. Objects created **before** the aspect is configured are **not** injected (debug log). Use `depends-on` on the configurer aspect bean if a Spring bean constructs domain objects at startup.

```d2
direction: down
new: "new Account() / ORM" {
  width: 220
  height: 50
  style.fill: "#e3f2fd"
}
weave: "AspectJ-woven class\n+ AnnotationBeanConfigurerAspect" {
  width: 280
  height: 70
  style.fill: "#fff3e0"
}
di: "Spring applies prototype\ndefinition / @Autowired" {
  width: 260
  height: 70
  style.fill: "#e8f5e9"
}

new -> weave -> di
```

**Fig. 1.** `@EnableAspectJAutoProxy` does **not** implement this. XML `aspectj-weaving="on"` used to pull in spring-configured; **`@EnableLoadTimeWeaving(ENABLED)` does not** — add `@EnableSpringConfigured` yourself.

> [!warning] Not `@Component`
> Do **not** put `@Configurable` on classes that are **already** Spring beans. You get **double initialization** (container + aspect). Unwoven unit tests: the annotation is a no-op (you can set mocks yourself); woven tests without a context log that the object was not configured.

> [!warning] One aspect, one `BeanFactory`
> `AnnotationBeanConfigurerAspect` is an AspectJ **singleton per ClassLoader**. Put `@EnableSpringConfigured` on the **parent** web context. Child servlet beans are not visible to domain injection. Each WAR should load `spring-aspects.jar` in its **own** ClassLoader.

> [!tip] Interview answer
> **`@Configurable` lets Spring inject `new` domain objects, but only if AspectJ weaves the class and `AnnotationBeanConfigurerAspect` is enabled.** It is not component scanning. Without weaving, the annotation is ignored.
