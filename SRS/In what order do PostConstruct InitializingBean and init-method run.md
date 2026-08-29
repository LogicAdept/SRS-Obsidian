<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC/Lifecycle #Java/Annotations #SRS

# In what order do `@PostConstruct`, `InitializingBean`, and `init-method` run?

> [!abstract] Short answer
> After properties (and `Aware` callbacks) are set, Spring runs init in this **fixed** order when the methods are **different** names: **`@PostConstruct`**, then **`InitializingBean.afterPropertiesSet()`**, then a custom **`init-method` / `@Bean(initMethod)`**. `@PostConstruct` is applied by `CommonAnnotationBeanPostProcessor` in **`postProcessBeforeInitialization`**, which is **before** those two container init methods. If the same method is registered under more than one of these mechanisms, it runs **once**. Destroy uses the **same** order, not the reverse: `@PreDestroy` → `DisposableBean.destroy()` → `destroy-method`.

## Combined initialization

Since Spring **2.5** you can stack three init styles on one bean ([[How do you call a method after a Spring bean is initialized]]):

1. Methods annotated `@PostConstruct` (`jakarta.annotation` as of Jakarta EE 9; not on the JDK 11+ classpath by itself).
2. `afterPropertiesSet()` from `InitializingBean`.
3. A POJO method named by XML `init-method`, `@Bean(initMethod)`, or `default-init-method` on `<beans>`.

`BeanNameAware` / other `Aware` interfaces run **after** property population and **before** that init sequence.

`@PostConstruct` is not a fourth “container init method” beside `afterPropertiesSet`. `CommonAnnotationBeanPostProcessor` extends `InitDestroyAnnotationBeanPostProcessor`, a `BeanPostProcessor` whose `postProcessBeforeInitialization` runs **before** `InitializingBean.afterPropertiesSet()` and any custom init-method. That is why the combined list starts with `@PostConstruct` and why dumps that say “inside before-init” and dumps that list it as step 1 of three are describing the **same** timeline. After those init methods, `postProcessAfterInitialization` runs; AOP infrastructure post-processors may wrap the instance there.

The container calls the configured init callback on the **raw** instance. AOP interceptors are not applied yet. The target is created and initialized first; then a proxy (if any) is applied ([[What is the difference between BeanFactoryPostProcessor and BeanPostProcessor]]).

```java
public class LifecycleDemo implements InitializingBean {

    @PostConstruct
    public void postConstruct() {
        // 1
    }

    @Override
    public void afterPropertiesSet() {
        // 2
    }

    public void customInit() {
        // 3
    }
}
```

```xml
<bean id="lifecycleDemo" class="example.LifecycleDemo" init-method="customInit"/>
```

**Listing 1.** Conceptual. Three **different** method names: `@PostConstruct`, then `afterPropertiesSet`, then `init-method`. `@Bean(initMethod = "customInit")` is the Java-config form of the same third slot.

```d2
direction: down
props: "Populate properties\nAware callbacks" {
  width: 240
  height: 70
  style.fill: "#e3f2fd"
}
before: "BPP postProcessBeforeInitialization\n@PostConstruct here" {
  width: 300
  height: 70
  style.fill: "#fff3e0"
}
ib: "InitializingBean.afterPropertiesSet" {
  width: 300
  height: 50
  style.fill: "#e8f5e9"
}
im: "init-method / @Bean(initMethod)" {
  width: 300
  height: 50
  style.fill: "#e8f5e9"
}
after: "BPP postProcessAfterInitialization\nAOP proxy wrap" {
  width: 300
  height: 70
  style.fill: "#fce4ec"
}

props -> before -> ib -> im -> after
```

**Fig. 1.** Combined init. `@PostConstruct` is a before-init post-processor callback; `afterPropertiesSet` and `init-method` are the container initialization methods that follow.

Spring recommends `@PostConstruct` or a POJO init-method over `InitializingBean` to avoid coupling to Spring. `@PostConstruct` (and init methods in general) run **inside the singleton creation lock**. Use them to validate configuration or prepare local structures, not to call other beans. Work that needs the whole container should wait for `SmartInitializingSingleton.afterSingletonsInstantiated()`, `ContextRefreshedEvent` ([[How does ApplicationContext publish events]]), or `(Smart)Lifecycle`.

Destroy callbacks, when the names differ, are **`@PreDestroy`**, then **`DisposableBean.destroy()`**, then a custom **`destroy-method` / `@Bean(destroyMethod)`** — the **same** sequence as init, not a reverse “mirror.” `@Bean` also infers a public `close` / `shutdown` destroy method unless you set `destroyMethod = ""`. Shutdown of the context is a separate card: [[How do you shut down a Spring ApplicationContext]].

> [!warning] Init sees the target, not the proxy
> `@PostConstruct`, `afterPropertiesSet`, and `init-method` run on the original instance. A later AOP proxy is not in place yet, so `@Transactional` (or other interceptors) on `this` does not apply. After-init post-processors wrap the bean; callers of the bean go through the proxy, init did not.

> [!warning] Same method name runs once; destroy is not reversed
> If `init()` is both `@PostConstruct` and `init-method`, Spring invokes it **once**. Do not count on a second call. Destroy is `@PreDestroy` then `DisposableBean` then `destroy-method` — not the reverse of construction. `@PostConstruct` that reaches out to other singletons can deadlock under the creation lock.

> [!tip] Interview answer
> After injection, Spring runs @PostConstruct, then InitializingBean.afterPropertiesSet, then init-method or @Bean(initMethod), as long as the method names differ. @PostConstruct is fired by CommonAnnotationBeanPostProcessor in postProcessBeforeInitialization, which is why it precedes the other two. Those callbacks run on the raw bean before after-init processors create an AOP proxy. Destroy uses that same annotation, interface, custom-method order, not the reverse.
