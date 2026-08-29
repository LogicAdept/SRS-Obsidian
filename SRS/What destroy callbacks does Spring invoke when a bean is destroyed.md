<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC/Lifecycle #Java/Annotations #SRS

# What destroy callbacks does Spring invoke when a bean is destroyed?

> [!abstract] Short answer
> For a **singleton** (and other scopes the factory fully manages), close of the context runs destroy in this **fixed** order when the methods have **different** names: **`@PreDestroy`**, then **`DisposableBean.destroy()`**, then a custom **`destroy-method` / `@Bean(destroyMethod)`**. Same name under more than one mechanism runs **once**. Prototypes get **init** callbacks but **not** configured destroy callbacks. `DisposableBean.destroy` exceptions are **logged, not rethrown**, so later beans can still clean up.

## Combined destruction

Since Spring **2.5** you can stack three destroy styles, matching init ([[In what order do PostConstruct InitializingBean and init-method run]]):

1. `@PreDestroy` (`jakarta.annotation`; `CommonAnnotationBeanPostProcessor` / `InitDestroyAnnotationBeanPostProcessor`). Methods may be any visibility. Prefer **one** destroy method.
2. `DisposableBean.destroy()` — `BeanFactory` calls it on destruction of a managed bean; an `ApplicationContext` disposes **singletons** on shutdown. Spring also honors `AutoCloseable` / `Closeable`. Prefer `@PreDestroy` or a POJO method over this interface (it couples you to Spring).
3. XML `destroy-method`, `@Bean(destroyMethod=…)`, or `default-destroy-method` on `<beans>`. `@Bean` **defaults** to `destroyMethod = "(inferred)"`: a public no-arg `close` or `shutdown` on the **instance** is registered. `@Bean(destroyMethod = "")` turns **inference** off; `DisposableBean` still runs.

`@PreDestroy` is a destruction post-processor (`postProcessBeforeDestruction`), not a fourth container method after `DisposableBean`. Combined order still starts with the annotation.

On a **regular** context close, `Lifecycle` / `SmartLifecycle` beans get **stop** first, then singleton destroy. A cancelled refresh or stop timeout can destroy **without** a preceding stop ([[How do you shut down a Spring ApplicationContext]]).

**Prototype:** the container instantiates, initializes, and **hands off**. Configured destroy callbacks are **not** called; the client must close resources. `@Bean` destroy methods run only when the factory fully controls the lifecycle — **always** for singletons, **not** guaranteed for other scopes.

Nothing runs if the process dies without `ConfigurableApplicationContext.close()` or `registerShutdownHook()`. A non-web `main` should register the hook. Spring Boot’s `SpringApplication` registers a JVM shutdown hook by default.

```java
public class CacheHolder implements DisposableBean {

    @PreDestroy
    public void preDestroy() {
        // 1
    }

    @Override
    public void destroy() {
        // 2 — exceptions logged, not rethrown
    }

    public void cleanup() {
        // 3
    }
}
```

```java
@Bean(destroyMethod = "cleanup")
CacheHolder cacheHolder() {
    return new CacheHolder();
}

@Bean(destroyMethod = "")
DataSource dataSource() {
    return lookupFromJndi(); // no inferred close(); DisposableBean still honored
}
```

**Listing 1.** Conceptual. Three **different** names: `@PreDestroy`, then `DisposableBean`, then `destroyMethod`. Empty `destroyMethod` disables **inferred** `close`/`shutdown` only.

```d2
direction: down
close: "Context close / JVM hook" {
  width: 240
  height: 50
  style.fill: "#e3f2fd"
}
stop: "Lifecycle stop\n(regular shutdown)" {
  width: 240
  height: 70
  style.fill: "#fff3e0"
}
pre: "@PreDestroy" {
  width: 200
  height: 45
  style.fill: "#e8f5e9"
}
disp: "DisposableBean.destroy" {
  width: 220
  height: 45
  style.fill: "#e8f5e9"
}
custom: "destroy-method / inferred close" {
  width: 260
  height: 50
  style.fill: "#e8f5e9"
}

close -> stop -> pre -> disp -> custom
```

**Fig. 1.** Regular singleton shutdown. Destroy order is the **same** sequence as init (`@PostConstruct` → `afterPropertiesSet` → `init-method`), not the reverse. Prototypes skip this destroy path.

> [!warning] No `close()` / no hook means no `@PreDestroy`
> A standalone `AnnotationConfigApplicationContext` that you never close skips singleton destruction. Boot hides this with a default hook; a plain `main` does not. Web contexts close with the servlet context.

> [!warning] Prototype and `destroyMethod=""` are easy to misread
> Prototype `@PreDestroy` will not run when the context shuts down. `@Bean(destroyMethod = "")` still invokes `DisposableBean`; it only skips inferred `close`/`shutdown` (use that for a JNDI `DataSource` the server owns). A destroy exception does not stop the rest of the singleton destroy round.

> [!tip] Interview answer
> On context close Spring destroys managed singletons with @PreDestroy, then DisposableBean.destroy, then destroy-method or an inferred public close/shutdown from @Bean. Same method name is invoked once. Prototypes are not destroyed by the container. You must close the context or registerShutdownHook; Boot already registers the hook. Prefer @PreDestroy over DisposableBean so the class stays off the Spring API.
