<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/AOP #SRS

# What is Advice in Spring AOP?

> [!abstract] Short answer
> **Advice** is the action an aspect runs at a **join point** selected by a **pointcut** — the extra behavior (logging, security, transactions) woven around a matched method execution on a Spring bean.

## How advice fits the AOP model

Spring AOP models each advice method as an **interceptor** in a chain around the join point. An aspect bundles one or more pointcuts with the advice methods that should run when those pointcuts match.

In `@AspectJ` style, you declare advice on methods inside an `@Aspect` class. Each advice annotation binds the method to a pointcut expression (inline or by reference). When a caller invokes the proxied bean, the framework runs matched advice at the appropriate point in the call — before, after, around, or on a specific return or throw outcome.

```d2
direction: right
aspect: "@Aspect class\n(pointcuts + advice)" {
  width: 220
  height: 90
  style.fill: "#fff3e0"
}
pointcut: "Pointcut\nmatches join points" {
  width: 200
  height: 80
  style.fill: "#e3f2fd"
}
advice: "Advice method\n(extra behavior)" {
  width: 200
  height: 80
  style.fill: "#e8f5e9"
}
join: "Join point\n(method execution)" {
  width: 200
  height: 80
  style.fill: "#fce4ec"
}

aspect -> pointcut
pointcut -> advice: "runs at"
advice -> join
```

**Fig. 1.** Advice is the executable part of an aspect; the pointcut decides **where** it runs on proxied method executions.

## Advice kinds in Spring

Spring supports five advice types, declared with AspectJ annotations:

| Annotation | Role |
|---|---|
| `@Before` | Runs before the join point; cannot stop execution unless it throws |
| `@AfterReturning` | Runs after a **normal** return |
| `@AfterThrowing` | Runs when the join point exits by **throwing** |
| `@After` | **Finally** advice — runs on any exit (normal or exceptional) |
| `@Around` | Wraps the join point; calls `ProceedingJoinPoint.proceed()` to continue |

See [[What advice types does Spring AOP support]] for per-type behavior and `@Around` control flow. Spring recommends the **least powerful** advice type that meets the requirement — for example, prefer `@AfterReturning` over `@Around` when you only need the return value.

```java
@Aspect
@Component
public class AuditAspect {

    @Before("execution(* com.example.service.*.*(..))")
    public void logEntry(JoinPoint jp) {
        // runs before matched service methods
    }
}
```

**Listing 1.** A `@Before` advice method associated with an inline pointcut on service-layer executions.

> [!warning] Advice sees the join-point boundary, not internal catches
> `@AfterThrowing` receives exceptions thrown **by the advised method as a whole**, not exceptions caught and handled inside the method body. If the target catches an exception in `try/catch` and returns normally, after-throwing advice does not run — and declarative transaction rollback tied to an uncaught exception will not trigger either. The failure must **leave** the advised method for throwing advice (and typical rollback rules) to see it.

Any advice method may take `JoinPoint` (or `ProceedingJoinPoint` for `@Around`) to read the signature, arguments, and proxy. See [[What is a JoinPoint in Spring AOP]] and [[What is a Pointcut in Spring AOP]] for how join points differ from the predicate that selects them.

> [!tip] Interview answer
> Advice is what an aspect **does** at a matched join point — the interceptor code around a proxied method. It is always tied to a pointcut and comes in before, after-returning, after-throwing, after-finally, and around forms; around advice is the most powerful because it can skip or replace the call via `proceed()`.
