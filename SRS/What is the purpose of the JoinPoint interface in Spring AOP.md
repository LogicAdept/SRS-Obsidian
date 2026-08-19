<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/AOP #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

`org.aspectj.lang.JoinPoint` gives reflective access at the join point: signature, args, target.

```java
@Before("execution(* com.example.service.*.*(..))")
public void logBefore(JoinPoint joinPoint) {
    joinPoint.getSignature().getName();
    joinPoint.getArgs();
}
```

> [!warning] Unverified traps from the dump
> - Around advice needs ProceedingJoinPoint (a JoinPoint subtype), not a plain JoinPoint, if you call proceed().
