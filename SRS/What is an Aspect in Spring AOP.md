<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/AOP #SRS

# What is an Aspect in Spring AOP?

> [!abstract] Short answer
> An **aspect** is the **module** for a **cross-cutting concern** — a class that holds **pointcuts**, **advice**, and optionally **introductions**. In Spring you mark it **`@Aspect`** and register it as a **Spring bean**. With `@EnableAspectJAutoProxy`, Spring auto-proxies advised beans so that advice runs on matching method executions.

## Module for cross-cutting work

Spring’s AOP overview: the unit of modularity in AOP is the **aspect**, used for concerns that cut across types (transactions, logging, security). `@AspectJ` style declares that module as a regular Java class with AspectJ 5 annotations; the **runtime is still Spring AOP** (proxies), not the AspectJ compiler unless you opt into weaving.

An `@Aspect` class can contain:

* **Pointcuts** — which join points match — [[What is a Pointcut in Spring AOP]]
* **Advice** — what runs there — [[What is Advice in Spring AOP]]
* **Introductions** (inter-type declarations) — extra interfaces mixed onto the target

```java
@Configuration
@EnableAspectJAutoProxy
public class ApplicationConfiguration {

    @Bean
    public NotVeryUsefulAspect myAspect() {
        return new NotVeryUsefulAspect();
    }
}

@Aspect
public class NotVeryUsefulAspect {
}
```

**Listing 1.** Spring’s minimal aspect: `@Aspect` on the class **and** a bean in the context. For component scanning you also need `@Component` (or another stereotype) — `@Aspect` alone is **not** enough for autodetection.

You can have **many** aspect beans. Schema style uses `<aop:aspect ref="…">` on a regular POJO instead of `@Aspect`.

```d2
direction: right
aspect: "@Aspect bean\npointcuts + advice" {
  width: 220
  height: 80
  style.fill: "#fff3e0"
}
proxy: "Auto-proxy\nadvised beans" {
  width: 200
  height: 70
  style.fill: "#e3f2fd"
}
target: "Target method\nexecution" {
  width: 180
  height: 70
  style.fill: "#e8f5e9"
}

aspect -> proxy -> target
```

**Fig. 1.** Detected `@Aspect` beans drive auto-proxying of matching targets.

> [!warning] `@Aspect` is not a stereotype
> Without `@Component` / `@Bean` / XML, Spring never sees the class. Enable auto-proxy separately (`@EnableAspectJAutoProxy` or `<aop:aspectj-autoproxy/>`).

> [!warning] Aspects are not advised by other aspects
> `@Aspect` **excludes** the class from auto-proxying. You cannot stack advice onto another aspect in Spring AOP.

> [!tip] Interview answer
> **An aspect packages a cross-cutting concern: pointcuts plus advice (and maybe introductions).** In Spring it is an `@Aspect` **bean**. `@Aspect` does not register the bean by itself; add `@Component` or `@Bean`, and turn on `@EnableAspectJAutoProxy`.
