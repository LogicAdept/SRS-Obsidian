<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC/Lifecycle #Java/Annotations #SRS

# How do you call a method after a Spring bean is initialized?

> [!abstract] Short answer
> After the container has created the instance and injected dependencies, use **`@PostConstruct`**, a named **`init-method`** / **`@Bean(initMethod = "…")`**, or **`InitializingBean.afterPropertiesSet()`**. Prefer `@PostConstruct` or a POJO init method. `InitializingBean` couples the class to Spring. A custom `BeanPostProcessor` can also run code around those callbacks.

## When “initialized” happens

Populate properties and satisfy `*Aware` callbacks first. Then initialization:

1. `BeanPostProcessor.postProcessBeforeInitialization` — `CommonAnnotationBeanPostProcessor` invokes `@PostConstruct` here
2. `InitializingBean.afterPropertiesSet()`
3. Custom `init-method` / `@Bean(initMethod)`
4. `BeanPostProcessor.postProcessAfterInitialization` (AOP proxies typically wrap here)

If several of those init hooks exist with **different** method names, Spring runs them in that order. If the **same** method is registered under more than one mechanism, it runs **once**. Full order: [[In what order do PostConstruct InitializingBean and init-method run]]. Mirror on shutdown: [[What destroy callbacks does Spring invoke when a bean is destroyed]].

```d2
direction: down
inject: "Construct + inject deps\n+ Aware callbacks" {
  width: 260
  height: 70
  style.fill: "#e3f2fd"
}
before: "BPP before-init\n@PostConstruct" {
  width: 240
  height: 70
  style.fill: "#fff3e0"
}
ib: "InitializingBean\nafterPropertiesSet()" {
  width: 240
  height: 70
  style.fill: "#fff3e0"
}
named: "init-method /\n@Bean(initMethod)" {
  width: 240
  height: 70
  style.fill: "#fff3e0"
}
after: "BPP after-init\n(AOP proxy)" {
  width: 240
  height: 70
  style.fill: "#e8f5e9"
}

inject -> before -> ib -> named -> after
```

**Fig. 1.** Init callbacks run on the **raw** instance. Proxies are applied afterward, so `@Transactional` on the same bean is not in force yet.

## The three bean-level hooks

Spring’s reference treats `@PostConstruct` as the usual choice (no Spring type on your class). If you skip JSR-250 / Jakarta Annotations, use `init-method` metadata.

```java
public class CacheWarmup {

    @PostConstruct
    public void populate() {
        // runs after injection, before the bean is published
    }
}
```

**Listing 1.** Conceptual `@PostConstruct`. Needs `CommonAnnotationBeanPostProcessor` (registered by `context:annotation-config` / `component-scan` and by `AnnotationConfigApplicationContext`).

Jakarta `PostConstruct` (non-interceptor bean): **no parameters**, return type **`void`**, **not static** (except an application client), any visibility. Spring’s processor also allows **multiple** annotated init methods, but one is the documented recommendation.

```xml
<bean id="exampleInitBean" class="examples.ExampleBean" init-method="init"/>
```

**Listing 2.** XML named init method: **void**, **no arguments**. Java config: `@Bean(initMethod = "init")`. You can instead call `init()` inside the `@Bean` factory before returning — that is ordinary Java, not the container init slot.

```java
public class ExampleBean implements InitializingBean {

    @Override
    public void afterPropertiesSet() {
        // after properties and Aware callbacks
    }
}
```

**Listing 3.** Conceptual `InitializingBean`. Official guidance: **do not** use it for application code; it couples the type to Spring.

A project-wide XML `default-init-method="init"` makes every bean with that method name participate without repeating `init-method` on each `<bean>`.

## Container-level alternatives

Implement `BeanPostProcessor` for behavior that should apply to **many** beans (`postProcessBeforeInitialization` / `postProcessAfterInitialization`). Internally, Spring already uses post-processors for `@PostConstruct`.

For work that must run **after all singletons exist** (and outside the singleton creation lock), use `SmartInitializingSingleton.afterSingletonsInstantiated()`, `@EventListener(ContextRefreshedEvent.class)`, or `SmartLifecycle` — not `@PostConstruct`.

> [!warning] `@PostConstruct` is not on the JDK module path
> It lived in `javax.annotation` on JDK 6–8, left the JDK in 9, and was removed in 11. Today it is `jakarta.annotation.PostConstruct` on **`jakarta.annotation-api`**. Without that JAR (or Boot bringing it in), the annotation is invisible and the method never runs.

> [!warning] Init is not a place to call other beans
> `@PostConstruct` and init methods run under the container’s **singleton creation lock**. The bean is published only after they return. Use them to validate config and fill local structures. Calling other beans from here can deadlock. AOP advice on **this** bean is not applied yet.

> [!warning] `InitializingBean` is the coupled option
> The Spring team recommends against it for application beans. Prefer `@PostConstruct` or a named POJO method. `afterPropertiesSet` is still what Spring itself uses internally on many framework types.

> [!tip] Interview answer
> After injection, Spring can call @PostConstruct, then InitializingBean.afterPropertiesSet, then a named init-method. Prefer @PostConstruct or init-method so the class stays a POJO. Put jakarta.annotation-api on the classpath from JDK 11 onward. Do not use @PostConstruct to talk to other beans or to rely on the bean’s own AOP proxy.
