<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/AOP #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Use AspectJ syntax, usually `execution`:

```
execution(* com.example.service.*.*(..))
```

`*` return type, package `com.example.service`, any class, any method, any args.

Reuse it with `@Pointcut` or inline it on `@Before` / `@Around`. Combine with `&&`, `||`, `!`.

> [!warning] Unverified traps from the dump
> - execution(* com.example.service.*.*(..)) is types in that package, not subpackages; .. is the subpackage form in AspectJ (dump often gets this wrong).
