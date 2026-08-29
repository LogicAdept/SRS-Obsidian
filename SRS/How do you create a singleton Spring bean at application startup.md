<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC/Scopes #SRS

# How do you create a singleton Spring bean at application startup?

> [!abstract] Short answer
> **Define it as a singleton and start an `ApplicationContext`.** Singleton is the **default** scope. `ApplicationContext` **eagerly pre-instantiates** those singletons during `refresh()` (`preInstantiateSingletons`) so configuration errors show up at startup, not on first `getBean`. You do **not** call `new` or a special “startup API.” Skip startup creation with `lazy-init="true"` / `@Lazy` ([[What is the Lazy annotation in Spring]]) — unless an eager singleton **depends** on that bean, which forces creation anyway.

## Default: one instance, created on `refresh()`

Register a `BeanDefinition` as usual ([[How do you create a bean in Spring]]). Omit `scope` (or set `scope="singleton"` / `@Scope("singleton")`). Constructing `AnnotationConfigApplicationContext(AppConfig.class)` or `ClassPathXmlApplicationContext("…")` **is** a `refresh()` ([[What is the difference between close and refresh on ApplicationContext]]). That pass loads definitions, runs post-processors, then **creates every non-lazy singleton** (and its dependency graph), including init callbacks.

That eager step is **why** `ApplicationContext` exists as the usual container: a successfully refreshed context has already built the singleton graph. A plain `BeanFactory` historically **does not** pre-instantiate; beans appear on first request.

```xml
<bean id="accountService" class="example.AccountService"/>
<bean id="expensive" class="example.ExpensiveToCreateBean" lazy-init="true"/>
```

**Listing 1.** Conceptual. `accountService` is a singleton created at context startup. `expensive` waits until first use — unless some **eager** singleton injects it, in which case it is still created during `refresh()`.

`default-lazy-init="true"` on `<beans>` (or `@Lazy` on a `@Configuration` class) turns the default around for that set of `@Bean` methods. `@Lazy(false)` on one method restores eager. `BeanPostProcessor` / `BeanFactoryPostProcessor` beans **ignore** lazy and still start eagerly.

**Not** created at application startup: **prototype** (and request/session) beans — they are created when requested. Parent **template** definitions that specify a `class` must be `abstract="true"`, or the context will try to pre-instantiate them.

```d2
direction: down
refresh: "ApplicationContext.refresh()" {
  width: 240
  height: 40
  style.fill: "#e3f2fd"
}
pre: "preInstantiateSingletons" {
  width: 220
  height: 40
  style.fill: "#fff3e0"
}
eager: "non-lazy singletons" {
  width: 200
  height: 40
  style.fill: "#e8f5e9"
}
lazy: "lazy / prototype: wait" {
  width: 220
  height: 40
  style.fill: "#eceff1"
}

refresh -> pre
pre -> eager
pre -> lazy
```

**Fig. 1.** Startup creates the default singleton set; lazy and shorter scopes wait.

> [!warning] Lazy collaborator of an eager singleton is not lazy
> `@Lazy` on `Expensive` does nothing for startup if `AccountService` (eager singleton) injects it. The dependency must be satisfied while pre-instantiating `AccountService`. Use an injection-point `@Lazy` **proxy** if you must defer that collaborator.

> [!warning] Eager is the feature, not a bug
> Pre-instantiation costs time and memory **on purpose**: missing properties and bad constructors fail when the context starts. Turning on global lazy (Boot `spring.main.lazy-initialization`) hides those failures until first request.

> [!tip] Interview answer
> A singleton is the default scope. An ApplicationContext creates those beans during refresh so the app fails fast at startup. I just register the bean and start the context. To skip startup I mark it lazy, knowing an eager singleton dependency will still create it.
