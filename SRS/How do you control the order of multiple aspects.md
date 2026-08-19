<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/AOP #Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps: `@Order` on the aspect class. **Lower value = higher precedence** (runs first for `@Before`).

```java
@Aspect
@Order(1)
@Component
public class FirstAspect { ... }
```

> [!warning] Unverified traps from the dump
> - For @Around, the highest-precedence aspect is the outermost wrapper — order of after-advice is the reverse of before (verify against docs).
> - Ordered / @Order on the aspect bean, not on the advice method, in the dump examples.
