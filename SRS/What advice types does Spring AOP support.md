<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/AOP #SRS

# What advice types does Spring AOP support?

> [!abstract] Short answer
> Five `@AspectJ` advice kinds: **`@Before`**, **`@AfterReturning`**, **`@AfterThrowing`**, **`@After`** (finally), and **`@Around`**. Spring AOP join points are **method executions** on beans. Prefer the **weakest** kind that fits — do not use `@Around` when `@Before` is enough.

## Five annotations, one interceptor chain

Advice is bound to a pointcut and runs before, after, or around matched executions.

| Annotation | When it runs |
| --- | --- |
| **`@Before`** | Before the method |
| **`@AfterReturning`** | After a **normal** return; optional `returning` binds the value |
| **`@AfterThrowing`** | After the method **throws**; optional `throwing` binds the exception |
| **`@After`** | After **any** exit (success or throw) — AspectJ “after finally” |
| **`@Around`** | Wraps the call via **`ProceedingJoinPoint.proceed()`** |

```java
@Aspect
public class DaoGuards {

    @Before("execution(* com.xyz.dao.*.*(..))")
    public void doAccessCheck() { /* ... */ }

    @AfterReturning(pointcut = "execution(* com.xyz.dao.*.*(..))", returning = "retVal")
    public void onSuccess(Object retVal) { /* ... */ }

    @AfterThrowing(pointcut = "execution(* com.xyz.dao.*.*(..))", throwing = "ex")
    public void onFailure(DataAccessException ex) { /* ... */ }

    @After("execution(* com.xyz.dao.*.*(..))")
    public void doReleaseLock() { /* ... */ }

    @Around("execution(* com.xyz..service.*.*(..))")
    public Object profile(ProceedingJoinPoint pjp) throws Throwable {
        return pjp.proceed();
    }
}
```

**Listing 1.** Conceptual mix of Spring’s advice examples. `@Around` can skip the target, change args, retry, or replace the return — [[What is ProceedingJoinPoint in Around advice]].

Same-aspect order (highest first): `@Around`, `@Before`, `@After`, `@AfterReturning`, `@AfterThrowing`. `@After` still behaves as **finally** (after returning/throwing companions). Detail: [[What is the difference between After AfterReturning and AfterThrowing advice]].

Full AspectJ can advise fields and constructors; Spring AOP does **not** unless you switch to AspectJ weaving.

```d2
direction: down
before: "@Before" {
  width: 160
  height: 40
  style.fill: "#e3f2fd"
}
around: "@Around / proceed()" {
  width: 200
  height: 50
  style.fill: "#fff3e0"
}
method: "target method" {
  width: 160
  height: 40
  style.fill: "#e8f5e9"
}
after: "@After (finally)" {
  width: 180
  height: 40
  style.fill: "#fce4ec"
}
ret: "@AfterReturning XOR\n@AfterThrowing" {
  width: 220
  height: 50
  style.fill: "#fff3e0"
}

before -> around -> method -> after
method -> ret
```

**Fig. 1.** Around wraps the method; after-finally always runs; returning vs throwing are exclusive outcomes.

> [!warning] `@AfterReturning` cannot swap the return object
> You can **read** `retVal`; you cannot replace the caller’s result. To substitute a value, use `@Around`.

> [!warning] `@AfterThrowing` is not a catch handler
> It observes exceptions from the **join point**, not from sibling `@After` / `@AfterReturning`. Swallowing or skipping the target is `@Around` only.

> [!tip] Interview answer
> **Spring AOP has `@Before`, `@AfterReturning`, `@AfterThrowing`, `@After` (finally), and `@Around`.** Join points are method executions. `@Around` is the only type that can skip or rewrite the call via `proceed()`. Use the least powerful advice that works.
