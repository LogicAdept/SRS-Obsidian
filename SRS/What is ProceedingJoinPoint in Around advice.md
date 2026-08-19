<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/AOP #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

`ProceedingJoinPoint` is the Around-only join point. `proceed()` runs the target method (or `proceed(Object[] args)` with replaced arguments). You can skip `proceed()`, change the return, or catch exceptions.

```java
@Around("execution(* com.example.service.*.*(..))")
public Object logAround(ProceedingJoinPoint joinPoint) throws Throwable {
    Object result = joinPoint.proceed();
    return result;
}
```

> [!warning] Unverified traps from the dump
> - If Around does not return proceed()’s value, the caller loses the real result — a dedicated nearby card.
