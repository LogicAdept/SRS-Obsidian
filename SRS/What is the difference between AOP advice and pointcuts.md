<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/AOP #SRS

# What is the difference between AOP advice and pointcuts?

> [!abstract] Short answer
> A **pointcut** is the **predicate** that selects join points. **Advice** is the **action** that runs at those matches. Spring associates advice with a pointcut expression; the pointcut does no work by itself. In Spring AOP the join point is always a **method execution** on a proxied bean.

## Where vs what

Spring *AOP Concepts*:

- **Pointcut** — a predicate that matches join points. Advice **runs at any join point matched by the pointcut**.
- **Advice** — action taken by an aspect at a particular join point (before, after returning, after throwing, after finally, around). Many frameworks, including Spring, model advice as an **interceptor** in a chain around the join point.

That split is what AOP adds over “just wrap everything in a decorator”: the same around-advice can apply to **methods that span many types** (for example all service-layer operations) because the pointcut is independent of the class hierarchy.

```java
@Pointcut("execution(* com.xyz.service.*.*(..))")
private void serviceLayer() {}

@Before("serviceLayer()")
public void logEntry(JoinPoint jp) {
    // advice — the work
}
```

**Listing 1.** Conceptual — `serviceLayer` is where; `logEntry` is what. The pointcut method body is empty on purpose.

| | Pointcut | Advice |
|---|---|---|
| Question | **Where** (which executions)? | **What** (extra behavior)? |
| `@AspectJ` | `@Pointcut` or the string on `@Before` / … | The annotated method |
| Spring runtime | AspectJ expression language | `MethodInterceptor` (and before/after adapters) |
| Empty on purpose | Named pointcut methods are `void` stubs | Contains the real code |

An **Advisor** is Spring’s low-level pair: **one advice + one pointcut** — [[What is an Advisor in Spring AOP]]. An **aspect** bundles several of those pairs — [[What is an Aspect in Spring AOP]].

```d2
direction: right
pc: "Pointcut\n(predicate)" {
  width: 180
  height: 70
  style.fill: "#e3f2fd"
}
jp: "Join points\n(method executions)" {
  width: 200
  height: 70
  style.fill: "#fff3e0"
}
adv: "Advice\n(interceptor)" {
  width: 180
  height: 70
  style.fill: "#e8f5e9"
}

pc -> jp: "matches"
jp -> adv: "runs at"
```

**Fig. 1.** Pointcut filters; advice executes. See [[What is a Pointcut in Spring AOP]] and [[What is Advice in Spring AOP]].

> [!warning] A matching pointcut is not a running interceptor
> If the call never enters the **proxy** (`this.foo()`, `private`, `final`), the pointcut never gets a join point — advice does not run. Interviews that treat “I wrote `@Before("execution(* …)")`” as proof of coverage miss the proxy boundary.

> [!tip] Interview answer
> Pointcut is the match rule; advice is the code that runs at matches. Spring AOP only has method-execution join points on proxies. The pointcut expression selects; the advice method (or interceptor) does the work.
