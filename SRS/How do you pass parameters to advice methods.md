<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/AOP #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Bind arguments with `args(...)` in the pointcut and a matching advice parameter:

```java
@Before("execution(* com.example.service.*.*(String)) && args(name)")
public void logBeforeMethod(String name) { ... }
```

> [!warning] Unverified traps from the dump
> - The advice parameter name must match the args() token.
