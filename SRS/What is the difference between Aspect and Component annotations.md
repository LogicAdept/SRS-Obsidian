<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/AOP #Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

`@Aspect` marks the class as an aspect (pointcuts + advice). `@Component` (or `@Bean`) registers it in the container.

Dumps use **both**: without `@Component`/scan/`@Bean`, `@Aspect` is not applied. `@Component` alone is not an aspect.

> [!warning] Unverified traps from the dump
> - @Aspect is not a @Component stereotype; it does not make the class a bean by itself.
