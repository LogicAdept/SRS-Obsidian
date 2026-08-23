<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/AOP #SRS

# What is aspect oriented programming AOP?

> [!abstract] Short answer
> **AOP** modularizes **cross-cutting concerns** (transactions, logging, security, caching) into **aspects** so they stay out of domain classes. In Spring, an aspect is usually an `@Aspect` bean: **pointcuts** select join points, **advice** runs there. Spring AOP is **proxy-based** and, by default, only advises **method executions** on Spring beans at **runtime**.

## Cross-cutting concern vs AOP

| Term | Meaning |
|---|---|
| **Cross-cutting concern** | Behavior needed across many types (logging, security, tx) — [[What is a cross-cutting concern]] |
| **AOP** | A technique to **extract** that behavior into reusable aspects instead of copy-paste |

AOP **complements** OOP: the class remains the unit for domain structure; the **aspect** is the unit for shared infrastructure — [[Is security a cross-cutting concern]], [[Which parts of a system would you move into aspects]].

## Core AOP vocabulary (Spring)

| Term | Spring meaning |
|---|---|
| **Aspect** | Module that holds pointcuts + advice (`@Aspect` class or schema) |
| **Join point** | A point in execution — in Spring AOP **always a method execution** |
| **Pointcut** | Predicate matching join points (AspectJ expression language) |
| **Advice** | Action at a matched join point — [[What is Advice in Spring AOP]] |
| **Target / advised object** | The bean being advised (behind a proxy) |
| **AOP proxy** | JDK interface proxy or **CGLIB** subclass proxy |
| **Weaving** | Linking aspects to objects — Spring AOP weaves at **runtime** via proxies |

Full AspectJ can weave at compile/load time and advise more join-point kinds — [[What is the difference between Spring AOP and AspectJ]].

## Advice kinds (use the weakest that fits)

`@Before` · `@AfterReturning` · `@AfterThrowing` · `@After` (finally) · `@Around` (`ProceedingJoinPoint.proceed()`).

Spring recommends the **least powerful** advice type that works — e.g. prefer `@AfterReturning` over `@Around` when you only need the return value — [[Why can Around advice lose the join point return value]].

```java
@Aspect
@Component
public class TimingAspect {

    @Around("execution(* com.example.service..*(..))")
    public Object time(ProceedingJoinPoint pjp) throws Throwable {
        long start = System.nanoTime();
        try {
            return pjp.proceed(); // must call and return
        } finally {
            long ms = (System.nanoTime() - start) / 1_000_000;
            // log pjp.getSignature() + ms
        }
    }
}
```

**Listing 1.** Around advice wraps the join point; skipping `proceed()` or dropping its return value breaks the call.

```d2
direction: right
caller: "Caller" {
  width: 100
  height: 45
  style.fill: "#e3f2fd"
}
proxy: "AOP proxy\n(JDK / CGLIB)" {
  width: 140
  height: 55
  style.fill: "#fff3e0"
}
advice: "Advice\n(before/around/after)" {
  width: 150
  height: 55
  style.fill: "#fce4ec"
}
target: "Target bean\n(method execution)" {
  width: 160
  height: 55
  style.fill: "#e8f5e9"
}

caller -> proxy -> advice -> target
```

**Fig. 1.** Spring AOP inserts advice on the proxy path to the real bean method.

> [!warning] Proxy limits
> Self-invocation (`this.method()`) skips the proxy — advice does not run — [[Why does a self-invocation skip Spring AOP advice]]. **Private** / **final** methods and non-Spring objects are outside default Spring AOP. In Boot, **CGLIB** is the default (`spring.aop.proxy-target-class=true`); set it `false` for JDK proxies.

> [!tip] Interview answer
> AOP extracts cross-cutting concerns into aspects (pointcut + advice). Spring AOP uses runtime proxies and only method-execution join points on beans. Built-in declarative services — @Transactional, @Cacheable, @PreAuthorize — are AOP under the hood.
