<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/AOP #SRS

# Why can Around advice lose the join point return value?

> [!abstract] Short answer
> **`@Around` is responsible for the value the caller receives.** Spring Framework states that **the around advice's return value is the return value seen by the caller**. If the advice **does not return the result of `proceed()`**, declares **`void`**, **never calls `proceed()`**, or **returns a substitute** (cache, wrapper, `null` after catching an exception), the join point's real return value is lost or replaced.

## Caller sees the advice return, not the target directly

Around advice wraps the matched method. The framework runs your `@Around` method instead of jumping straight to the target; **`ProceedingJoinPoint.proceed()`** is what actually invokes the underlying method and yields its result.

Official guidance:

- The advice method should normally declare return type **`Object`** and **`return` the value from `proceed()`**, even when the advised method is **`void`** (Spring still expects you to propagate the `proceed()` outcome through an `Object` return).
- If the advice method is declared **`void`**, **`null` is always returned to the caller**, **ignoring whatever `proceed()` produced**.

```java
@Aspect
@Component
public class TimingAspect {

    @Around("@annotation(com.example.TrackTime)")
    public Object around(ProceedingJoinPoint joinPoint) throws Throwable {
        long start = System.currentTimeMillis();
        Object retVal = joinPoint.proceed();   // run target; capture return
        long elapsed = System.currentTimeMillis() - start;
        logger.info("{} took {} ms", joinPoint.getSignature(), elapsed);
        return retVal;                         // must reach the caller
    }
}
```

**Listing 1.** Correct pattern — store `proceed()` result and return it.

## Common ways the return value disappears

| Mistake | Effect |
|---|---|
| **`return` omitted or wrong variable returned** | Caller gets `null` or an unrelated object |
| **Advice method declared `void`** | `proceed()` result always discarded (`null` to caller) |
| **`proceed()` never called** | Target never runs; caller sees whatever the advice returns (often `null`) |
| **Catch block returns `null` / default without rethrow** | Exception swallowed; real outcome replaced |
| **Intentional substitute** (cache hit, mock, wrapper) | Original join-point value deliberately not returned — valid pattern, but callers must expect it |

`proceed()` may be called **zero, one, or many times** — all legal — but whatever your advice **returns** is what the external caller observes. See [[What is ProceedingJoinPoint in Around advice]].

```d2
direction: right
caller: "Caller" {
  width: 100
  height: 40
  style.fill: "#e3f2fd"
}
around: "@Around advice" {
  width: 140
  height: 50
  style.fill: "#fff3e0"
}
proceed: "proceed()\n→ target method" {
  width: 160
  height: 60
  style.fill: "#e8f5e9"
}
lost: "return void / null\ninstead of retVal" {
  width: 180
  height: 60
  style.fill: "#ffcdd2"
}

caller -> around -> proceed -> around -> caller: "return retVal"
around -> lost: "bug path"
lost -> caller
```

**Fig. 1.** The advice sits in the return path; only its return value escapes to the caller.

> [!warning] void advice silently drops non-void targets
> A logging aspect written as **`public void logAround(ProceedingJoinPoint pjp)`** that calls **`pjp.proceed()`** but returns nothing makes every advised **`String`**, **`List`**, or DTO method appear to return **`null`** to callers. Declare **`Object`** and **`return pjp.proceed()`** (or the cached/wrapped value). See [[What is Advice in Spring AOP]].

> [!tip] Interview answer
> Around advice owns the return value seen by the caller. You must call proceed() when the target should run and return its result — typically Object retVal = pjp.proceed(); return retVal. Declaring void on the advice method always returns null to the caller, ignoring proceed(). Skipping return, swallowing exceptions, or returning a substitute also loses the real join-point value.
