<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC/Lifecycle #Java/Annotations #SRS

# What is the Lazy annotation in Spring?

> [!abstract] Short answer
> `@Lazy` (since **3.0**) skips **eager singleton pre-instantiation**. The bean is created on **first request** (or first real use of an injection-point proxy), not when the `ApplicationContext` starts. XML is `lazy-init="true"`; `@Lazy` on a `@Configuration` class is `default-lazy-init` for that class’s `@Bean` methods (`@Lazy(false)` on a method turns one back to eager). On an `@Autowired` / `@Inject` **parameter or field**, `@Lazy` injects a **lazy-resolution proxy**, not “leave the field null.” That is how you defer a collaborator (including some constructor cycles). It does **not** apply to `BeanPostProcessor` / `BeanFactoryPostProcessor` beans — those stay eager.

## Definition lazy vs injection-point lazy

Default `ApplicationContext` behavior: create every **singleton** at startup so misconfiguration fails immediately. `@Lazy` / `lazy-init` opts a **singleton definition** out of that. Prototypes were never pre-instantiated.

```java
@Bean
@Lazy
ExpensiveToCreateBean lazy() {
    return new ExpensiveToCreateBean();
}
```

```xml
<bean id="lazy" class="example.ExpensiveToCreateBean" lazy-init="true"/>
```

**Listing 1.** Conceptual. `notLazy` singletons still start eagerly. If an **eager** singleton **depends** on `lazy`, the container still creates `lazy` at startup to fill that dependency — the flag is then a no-op.

`@Lazy` on `@Component` / `@Bean`: not initialized until another bean references it or you `getBean`. `@Lazy(false)` forces eager init even under a `@Lazy` `@Configuration` or Boot’s `spring.main.lazy-initialization=true`.

**Injection point** (`@Autowired` / `@Inject` + `@Lazy`): a **proxy** is always injected. First method call materializes a **singleton** target and caches it; other scopes re-resolve. A missing target fails on **invocation**, not at injection — awkward for optional dependencies. Prefer `ObjectProvider` for optional / repeated lookup ([[What is ObjectProvider and a scoped proxy in Spring]]).

```java
public ServiceA(@Lazy ServiceB b) {
    this.b = b;
}
```

**Listing 2.** Conceptual. Constructor can finish; `b` is a proxy. Constructor **cycles** still fail if both sides need a fully built instance with no proxy (`BeanCurrentlyInCreationException`) ([[How would you explain dependency injection]]). `@Lazy` on **both bean definitions** does not replace a proxy on the injection point, and an eager singleton that `@Autowired` them will still create them at startup.

```d2
direction: down
eager: "Eager singleton\npre-instantiated at refresh" {
  width: 260
  height: 55
  style.fill: "#e3f2fd"
}
def: "@Lazy on @Bean / @Component\ncreate on getBean" {
  width: 280
  height: 55
  style.fill: "#fff3e0"
}
inj: "@Lazy on injection point\nproxy now, target on first call" {
  width: 300
  height: 55
  style.fill: "#e8f5e9"
}

eager -> def: "unless this bean depends on it"
inj -> def: first invocation
```

**Fig. 1.** Two meanings of `@Lazy`. Dependency from an eager singleton defeats definition-level laziness.

Startup cost moves to **first use**: invalid properties or missing classes surface then, not at `refresh()` ([[How do you fix a circular dependency caused by self-injection in Spring]]). That is why eager singletons are the default.

> [!warning] Lazy definition + eager collaborator = still created at startup
> Mark the **injection point** `@Lazy` (proxy) or inject `ObjectProvider` if the consumer must stay an eager singleton. `default-lazy-init` is ignored for factory and bean **post-processors**.

> [!warning] The injection-point proxy always exists
> You cannot treat `@Lazy` `ServiceB` as optional `null`. Missing beans throw when you **call** the proxy. Use `ObjectProvider` / `Optional` for optionality.

> [!tip] Interview answer
> @Lazy delays singleton creation until first request, matching XML lazy-init. If an eager singleton depends on that bean, Spring still creates it at startup. On an autowired parameter it injects a lazy proxy — useful for constructor cycles — but ObjectProvider is better for optional or repeated lookup. Errors move from context startup to first use.
