<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/AOP #Java/Annotations #SRS

# What is the difference between After AfterReturning and AfterThrowing advice?

> [!abstract] Short answer
> **`@AfterReturning`** runs only after a **normal** return and can bind the value (`returning`). **`@AfterThrowing`** runs only when the **target method throws** and can bind the exception (`throwing`). **`@After`** is **after-finally**: it runs on **either** outcome and is for cleanup, not for reading the return or the throwable.

## Three exits from a method execution

Spring *Declaring Advice*:

| | **`@AfterReturning`** | **`@AfterThrowing`** | **`@After`** |
| --- | --- | --- | --- |
| Runs when | Method **returns normally** | Method **exits by throwing** | **Any** exit (return or throw) |
| Binding | `returning = "retVal"` | `throwing = "ex"` | None in the usual form |
| Typical use | Observe / cache the result | Recovery / log the failure | Unlock, close, always-cleanup |

```java
@AfterReturning(pointcut = "execution(* com.xyz.dao.*.*(..))", returning = "retVal")
public void onSuccess(Object retVal) { /* ... */ }

@AfterThrowing(pointcut = "execution(* com.xyz.dao.*.*(..))", throwing = "ex")
public void onFailure(DataAccessException ex) { /* ... */ }

@After("execution(* com.xyz.dao.*.*(..))")
public void doReleaseLock() { /* ... */ }
```

**Listing 1.** Patterns from Spring’s after-returning / after-throwing / after-finally examples. Binding names must match the advice parameter; the clause also **restricts** matching to that return or exception type.

In the **same** `@Aspect`, type order is `@Around` > `@Before` > `@After` > `@AfterReturning` > `@AfterThrowing`, but **`@After` still runs as finally** — after the returning or throwing companion. Full type list: [[What advice types does Spring AOP support]]. Binding the success value: [[Can you access the return value in AfterReturning advice]].

```d2
direction: down
method: "Target method exits" {
  width: 220
  height: 50
  style.fill: "#e3f2fd"
}
ok: "normal return" {
  width: 180
  height: 40
  style.fill: "#e8f5e9"
}
fail: "throws" {
  width: 140
  height: 40
  style.fill: "#ffebee"
}
ar: "@AfterReturning" {
  width: 180
  height: 40
  style.fill: "#e8f5e9"
}
at: "@AfterThrowing" {
  width: 180
  height: 40
  style.fill: "#ffebee"
}
af: "@After (finally)" {
  width: 180
  height: 40
  style.fill: "#fff3e0"
}

method -> ok -> ar
method -> fail -> at
ok -> af
fail -> af
```

**Fig. 1.** Returning and throwing are exclusive; `@After` runs for both, like `finally`.

> [!warning] Caught exceptions never reach `@AfterThrowing`
> If the target **catches** internally and returns, the join point did **not** exit by throwing. `@AfterReturning` / `@After` may still run; `@AfterThrowing` does not.

> [!warning] `@AfterThrowing` is not a catch handler for sibling advice
> It observes exceptions from the **user method**, not from accompanying `@After` / `@AfterReturning`. It does not swallow the exception.

> [!warning] `@After` does not bind `retVal` or `ex`
> Need the result or the throwable? Use the specialized annotations (or `@Around`). `@After` must tolerate **both** success and failure.

> [!tip] Interview answer
> **`@AfterReturning` is success-only and can bind the return value. `@AfterThrowing` is throw-only and can bind the exception. `@After` is finally — always, for cleanup.** If the method swallows the exception, throwing advice never runs.
