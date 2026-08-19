<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/AOP #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps use the `bean(...)` designator (Spring-specific):

```java
@Before("bean(myService) && execution(* *(..))")
public void logBefore(JoinPoint joinPoint) { ... }
```

Matches the bean named `myService`.

> [!warning] Unverified traps from the dump
> - bean() is not core AspectJ; it is a Spring AOP extension.
