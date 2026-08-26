<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/AOP #SRS

# How would you exclude a method from being advised?

> [!abstract] Short answer
> **Narrow the pointcut** with **`!`** — typically `execution(...) && !execution(specificMethod)` or `&& !@annotation(...)`. Spring combines expressions with **`&&`**, **`||`**, and **`!`**. That only drops matches for **this** pointcut; a second aspect with a broader cut still advises the method.

## Negate the join points you do not want

Spring’s *Combining Pointcut Expressions*: compose with `&&`, `||`, `!`, and named `@Pointcut` methods. Best practice is small named cuts, then a composite. Visibility of the named method follows Java rules; it does not change matching.

```java
@Pointcut("execution(* com.xyz.service.*.*(..))")
public void inServicePackage() {}

@Pointcut("execution(* com.xyz.service.HealthService.ping(..))")
public void healthPing() {}

@Pointcut("inServicePackage() && !healthPing()")
public void serviceExceptHealth() {}

@Before("serviceExceptHealth()")
public void logService() { /* ... */ }
```

**Listing 1.** Conceptual composition — same operators as Spring’s `publicMethod() && inTrading()` example. Inline form: `execution(* com.xyz.service.*.*(..)) && !execution(* com.xyz.service.HealthService.ping(..))`.

Other useful excludes:

* `!@annotation(com.xyz.NoLog)` — skip methods carrying that annotation
* `!within(com.xyz.internal..*)` — skip a package tree
* `!bean(healthService)` — Spring-only `bean` PCD (proxy mode)

How to write `execution` vs `..` subpackages: [[How do you define a pointcut expression in Spring AOP]]. Combining named cuts: [[How do you combine multiple pointcut expressions]].

```d2
direction: right
wide: "execution(* service.*.*(..))" {
  width: 260
  height: 70
  style.fill: "#e3f2fd"
}
not: "! execution(* Health.ping(..))" {
  width: 260
  height: 70
  style.fill: "#ffebee"
}
adv: "Advice runs on\nthe intersection" {
  width: 220
  height: 70
  style.fill: "#e8f5e9"
}

wide -> not -> adv
```

**Fig. 1.** Exclusion is set difference on join points, not a global “do not advise” flag.

> [!warning] One pointcut is not a firewall
> Another `@Aspect` whose expression still matches **will** run. You must tighten **every** advising aspect, or use a shared named cut they all reuse.

> [!warning] Self-invocation is already excluded
> Calls on `this` never hit the proxy, so they look “unadvised” even without `!`. That is proxy semantics, not a pointcut exclude.

> [!tip] Interview answer
> **Exclude by composing pointcuts with `&& !…`** — another `execution`, `@annotation`, `within`, or `bean`. That only affects that expression. Other aspects can still match unless they share the same narrowed cut.
