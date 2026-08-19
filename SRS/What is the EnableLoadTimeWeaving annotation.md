<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Instrumentation #Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

`@EnableLoadTimeWeaving` is the dump switch that tells Spring to use load-time weaving instead of (or in addition to) proxy AOP. Compilations pair it with AspectJ LTW: `@EnableLoadTimeWeaving(aspectjWeaving = EnableLoadTimeWeaving.AspectJWeaving.ENABLED)`.

It is the annotation counterpart dumps contrast with `@EnableAspectJAutoProxy` (Spring AOP proxies that understand `@Aspect` syntax).

> [!warning] Unverified traps from the dump
> - `aspectjWeaving = ENABLED` in the dump does not replace the Java agent or `META-INF/aop.xml`; those still appear as extra steps.
> - Putting this on `@SpringBootApplication` is dump sample code, not proof it weaves every class in a Boot process.
