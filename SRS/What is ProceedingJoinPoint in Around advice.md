<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/AOP #SRS

# What is `ProceedingJoinPoint` in Around advice?

> [!abstract] Short answer
> **`ProceedingJoinPoint` is the first parameter of `@Around` advice** — a `JoinPoint` subtype that can **run the target method** via **`proceed()`**. No-arg `proceed()` uses the caller’s arguments; **`proceed(Object[])`** replaces them. You may call it **zero, one, or many** times; whatever the advice **returns** is what the caller sees.

## Around owns the invocation

Spring *Declaring Advice*: around advice runs **around** a matched method. The first parameter **must** be **`ProceedingJoinPoint`**. You **must** invoke `proceed()` for the underlying method to run. That is the only advice type that can skip, retry, or wrap the join point — weaker types (`@Before`, `@After…`) receive a plain **`JoinPoint`** with no `proceed()`.

```java
@Around("execution(* com.xyz..service.*.*(..))")
public Object doBasicProfiling(ProceedingJoinPoint pjp) throws Throwable {
    Object retVal = pjp.proceed();
    return retVal;
}
```

**Listing 1.** Spring’s around example — capture `proceed()` and return it. Declaring the advice `void` always returns `null` to the caller.

| Call | Effect |
| --- | --- |
| `proceed()` | Target runs with original arguments |
| `proceed(Object[])` | Target runs with that array as arguments — [[Can Around advice modify method arguments]] |
| never `proceed()` | Target skipped (cache hit, short-circuit) |
| `proceed()` in a loop | Retry; legal |

```d2
direction: down
around: "@Around method\nProceedingJoinPoint pjp" {
  width: 280
  height: 70
  style.fill: "#fff3e0"
}
proceed: "pjp.proceed()" {
  width: 180
  height: 50
  style.fill: "#e8f5e9"
}
target: "Target method" {
  width: 180
  height: 50
  style.fill: "#e3f2fd"
}
ret: "return value to caller" {
  width: 220
  height: 50
  style.fill: "#fce4ec"
}

around -> proceed -> target -> around -> ret
```

**Fig. 1.** The around method is the return path; losing `proceed()`’s result is a common bug — [[Why can Around advice lose the join point return value]].

> [!warning] First parameter type is required
> If the first argument is not `ProceedingJoinPoint`, Spring cannot wire around advice. `JoinPoint` is enough for `@Before` / `@After*` but cannot invoke the target.

> [!warning] Spring `proceed(Object[])` ≠ AspectJ compiler `proceed`
> Native AspectJ around binds `proceed` args to **advice** parameters, not join-point arity. Spring proxy AOP treats the array as the **target method** arguments. Bind parameters in order if the same `@Aspect` must weave in both worlds.

> [!tip] Interview answer
> **`ProceedingJoinPoint` is Around’s handle on the join point.** Call `proceed()` to run the target, optionally with new arguments. Skip it to short-circuit, call it more than once to retry, and always return that result (or a deliberate substitute) so the caller is not given `null`.
