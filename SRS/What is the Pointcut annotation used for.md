<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/AOP #Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

`@Pointcut` names a reusable pointcut expression. Advice methods refer to it by the method name.

```java
@Pointcut("execution(* com.example.service.*.*(..))")
public void serviceMethods() {}

@Before("serviceMethods()")
public void log() {}
```

> [!warning] Unverified traps from the dump
> - The @Pointcut method body is empty; the expression is the annotation value.
