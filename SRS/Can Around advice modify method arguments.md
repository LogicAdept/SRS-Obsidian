<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/AOP #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps: yes, via `proceed(Object[] args)`:

```java
@Around("execution(* com.example.service.*.*(String)) && args(name)")
public Object logAround(ProceedingJoinPoint joinPoint, String name) throws Throwable {
    return joinPoint.proceed(new Object[]{"Modified Argument"});
}
```

> [!warning] Unverified traps from the dump
> - Replacing args without matching the method signature throws.
