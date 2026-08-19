<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/AOP #Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Yes. Set `returning` on `@AfterReturning` to the advice parameter name:

```java
@AfterReturning(pointcut = "execution(* com.example.service.*.*(..))", returning = "result")
public void logAfterReturning(Object result) { ... }
```

> [!warning] Unverified traps from the dump
> - returning name must match the method parameter; otherwise the advice does not bind (or fails at startup — dump unspecified).
