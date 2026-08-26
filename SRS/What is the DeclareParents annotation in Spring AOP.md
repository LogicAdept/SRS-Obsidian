<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/AOP #Java/Annotations #SRS

# What is the `DeclareParents` annotation in Spring AOP?

> [!abstract] Short answer
> **`@DeclareParents`** (on a **field** in an `@Aspect`) is the `@AspectJ` **introduction**: matching types get a **new parent interface**. The **field type** is that interface; **`value`** is an AspectJ type pattern; **`defaultImpl`** is the mixin class. Spring wires this as a **`DeclareParentsAdvisor`**. XML twin: **`<aop:declare-parents>`**.

## Field is the interface, `value` is who gets it

AspectJ: `@Retention(RUNTIME)` `@Target(FIELD)`. `value` is the target-types expression. `defaultImpl` supplies interface method bodies (javadoc: **should always be specified**; default sentinel is `DeclareParents.class` meaning “none”).

Spring *Introductions*: any **bean** whose type matches `value` then **implements** the field’s interface via `defaultImpl`.

```java
@Aspect
public class UsageTracking {

    @DeclareParents(value = "com.xyz.service.*+", defaultImpl = DefaultUsageTracked.class)
    public static UsageTracked mixin;

    @Before("execution(* com.xyz..service.*.*(..)) && this(usageTracked)")
    public void recordUsage(UsageTracked usageTracked) {
        usageTracked.incrementUseCount();
    }
}
```

**Listing 1.** Official pattern: `*+` is the type and its subtypes. Bind with `this(usageTracked)` — the **proxy** is a `UsageTracked`. Programmatic lookup: `context.getBean("myService", UsageTracked.class)`. Concept: [[What is Introduction in Spring AOP]].

Schema equivalent:

```xml
<aop:declare-parents
    types-matching="com.xyz.service.*+"
    implement-interface="com.xyz.service.tracking.UsageTracked"
    default-impl="com.xyz.service.tracking.DefaultUsageTracked"/>
```

**Listing 2.** `implement-interface` / `types-matching` / `default-impl` map to field type / `value` / `defaultImpl`. The aspect class still holds `recordUsage`.

AspectJ without `defaultImpl` only adds a **marker** interface (no method ITDs). Spring’s documented examples always pass `defaultImpl` so the mixin has behavior. The field must be the **interface**, not a class. Advisors: [[What is an Advisor in Spring AOP]].

```d2
direction: down
ann: "@DeclareParents on field\ntype = UsageTracked" {
  width: 280
  height: 70
  style.fill: "#e3f2fd"
}
match: "value type pattern\n(beans that match)" {
  width: 260
  height: 60
  style.fill: "#fff3e0"
}
proxy: "Proxy implements interface\nvia defaultImpl" {
  width: 260
  height: 70
  style.fill: "#e8f5e9"
}

ann -> match -> proxy
```

**Fig. 1.** The annotation does not change the target `.class`. Callers must use the **introduced** type.

> [!warning] Injecting `MyService` does not give mixin methods
> `MyService s` has no `incrementUseCount()`. Use `UsageTracked`, a cast of the **proxy**, or `getBean(..., UsageTracked.class)`. Casting the raw implementation class fails.

> [!warning] Type pattern is not `execution()`
> `value` is a **type** pattern (`com.xyz.service.*+`), not a method pointcut. A wrong pattern means **no** introduction and **no** compile error.

> [!tip] Interview answer
> **`@DeclareParents` on an aspect field mixes an interface into matching bean types.** Field type = interface, `value` = type pattern, `defaultImpl` = implementation. Look the bean up as that interface; the original class is unchanged.
