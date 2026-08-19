<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/AOP #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

A pointcut is a predicate / expression that matches join points. Advice runs only where the pointcut matches.

Spring uses the AspectJ expression language. Typical dump example:

```java
@Pointcut("execution(* com.example.service.*.*(..))")
public void serviceMethods() {}
```

That matches all methods in `com.example.service`.

> [!warning] Unverified traps from the dump
> - A nearby card compares advice vs pointcuts; this one is the term itself.
> - execution() is not the only designator; dumps also show args, bean, @annotation, within.
