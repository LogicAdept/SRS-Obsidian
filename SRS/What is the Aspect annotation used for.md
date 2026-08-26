<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/AOP #Java/Annotations #SRS

# What is the `Aspect` annotation used for?

> [!abstract] Short answer
> **`@Aspect` marks a class as an AspectJ-style aspect** so it can hold **`@Pointcut`** and advice (`@Before`, `@Around`, …) plus introductions. Spring detects **`@Aspect` beans** when **`@EnableAspectJAutoProxy`** is on. **`@Aspect` is not a stereotype** — you still need **`@Component`**, **`@Bean`**, or XML to register the class.

## Annotation-style aspect module

`@AspectJ` style (AspectJ 5 annotations, Spring AOP runtime): any context bean whose class has `@Aspect` is used to configure auto-proxying. The class may contain pointcut, advice, and introduction declarations like any other type.

```java
@Aspect
@Component
public class LoggingAspect {

    @Pointcut("execution(* com.xyz.service.*.*(..))")
    public void serviceLayer() {}

    @Before("serviceLayer()")
    public void log(JoinPoint jp) { /* ... */ }
}
```

**Listing 1.** Usual pairing: `@Aspect` for AOP metadata, `@Component` so component-scan creates a bean. What an aspect is: [[What is an Aspect in Spring AOP]]. Enabling: [[How do you enable AOP in a Spring application]], [[What is the EnableAspectJAutoProxy annotation]].

```d2
direction: right
aspect: "@Aspect" {
  width: 140
  height: 50
  style.fill: "#fff3e0"
}
bean: "@Component / @Bean" {
  width: 180
  height: 50
  style.fill: "#e3f2fd"
}
proxy: "auto-proxy advised beans" {
  width: 220
  height: 60
  style.fill: "#e8f5e9"
}

aspect -> bean -> proxy
```

**Fig. 1.** Both metadata and a bean definition are required. Difference vs `@Component` alone: [[What is the difference between Aspect and Component annotations]].

> [!warning] `@Aspect` does not register a bean
> Classpath scanning ignores a class that is only `@Aspect`. Add `@Component` (or a custom stereotype) or an explicit `@Bean`.

> [!warning] Aspects are excluded from auto-proxying
> Spring will **not** advise other `@Aspect` beans. You cannot stack aspects on an aspect in Spring AOP.

> [!tip] Interview answer
> **`@Aspect` declares the class as an aspect** — pointcuts and advice live there. It is **not** `@Component`. Register the bean and turn on `@EnableAspectJAutoProxy` (or Boot’s AOP starter). The runtime is still Spring proxies unless you add AspectJ weaving.
