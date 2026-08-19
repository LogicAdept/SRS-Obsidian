<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/AOP #Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

`@Aspect` declares a class as an aspect so it can contain `@Pointcut` and advice methods (`@Before`, `@Around`, …).

```java
@Aspect
@Component
public class LoggingAspect { }
```

> [!warning] Unverified traps from the dump
> - Without also being a Spring bean, the aspect is ignored.
