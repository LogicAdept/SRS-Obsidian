<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/AOP #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Reuse named `@Pointcut` methods with `&&`, `||`, `!`:

```java
@Before("serviceMethods() || repositoryMethods()")
public void logMethods() {}

@Pointcut("execution(* com.example.service.*.*(..)) && !execution(* com.example.service.SomeService.someMethod(..))")
public void serviceMethodsExcludingSomeMethod() {}
```

> [!warning] Unverified traps from the dump
> - Operator precedence can surprise; dumps use parentheses on excludes.
