<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/AOP #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Narrow the pointcut with `!execution(...)` (or `!@annotation(...)`):

```java
@Pointcut("execution(* com.example.service.*.*(..)) && !execution(* com.example.service.SomeService.someMethod(..))")
public void serviceMethodsExcludingSomeMethod() {}
```

> [!warning] Unverified traps from the dump
> - Excluding one method does not help if a broader second aspect still matches.
