<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/AOP #SRS

# What is Introduction in Spring AOP?

> [!abstract] Short answer
> An **introduction** (AspectJ **inter-type declaration**) adds members **on behalf of** a type. **Spring AOP** does this by making the **advised object** implement an extra **interface** plus a **`defaultImpl`**. The target class is **not** rewritten. Declare it with **`@DeclareParents`** (or schema `declare-parents`). Classic example: mix in **`IsModified`** for caching.

## Interface mixin on the proxy

Spring *AOP Concepts*: introduction is declaring additional methods or fields on behalf of a type. Then it narrows Spring’s implementation: **new interfaces and a corresponding implementation** on any advised object.

The `@AspectJ` *Introductions* chapter: the aspect states that matching types have a **new parent**. The **field type** is the interface; **`value`** is an AspectJ type pattern; **`defaultImpl`** is the mixin class.

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

**Listing 1.** Spring’s `UsageTracked` example (e.g. JMX stats). `this(usageTracked)` binds the **proxy**, which now implements `UsageTracked`. From the container: `context.getBean("myService", UsageTracked.class)`. Annotation details: [[What is the DeclareParents annotation in Spring AOP]].

Programmatic API: **`IntroductionAdvisor`** + **`IntroductionInterceptor`** (`DelegatingIntroductionInterceptor`). Not a `DefaultPointcutAdvisor` — introductions are **type-level**, not a method pointcut. Stateful mixins need a **per-instance** advisor. You cannot add/remove an introduction advisor on an **existing** proxy (`Advised`) — get a new proxy. Advisors: [[What is an Advisor in Spring AOP]]. Proxy: [[What is an AOP proxy in Spring]].

```d2
direction: right
target: "Service bean\n(unchanged class)" {
  width: 200
  height: 70
  style.fill: "#e3f2fd"
}
proxy: "AOP proxy also\nimplements UsageTracked" {
  width: 240
  height: 70
  style.fill: "#fff3e0"
}
impl: "DefaultUsageTracked\n(defaultImpl)" {
  width: 200
  height: 70
  style.fill: "#e8f5e9"
}

target -> proxy
impl -> proxy
```

**Fig. 1.** Callers use the introduced interface on the **proxy**. Casting the raw target type to `UsageTracked` fails.

> [!warning] Not AspectJ field ITDs
> Code-style AspectJ can insert fields/methods into bytecode. Spring AOP introductions are **interface mixins** on the **runtime proxy**. The original class file still does not implement `UsageTracked`.

> [!warning] Lookup type must be the interface
> `getBean("myService", MyServiceImpl.class)` does not magically implement the mixin for you as that Java type. Ask for **`UsageTracked`** (or cast the injected proxy). JDK proxies already implement interfaces; the introduction **adds another**.

> [!tip] Interview answer
> **Introduction means the advised object implements an extra interface with a provided implementation — in Spring, `@DeclareParents`.** It is an inter-type declaration / mixin, not a method interceptor. The target class source stays the same; the proxy exposes the new API.
