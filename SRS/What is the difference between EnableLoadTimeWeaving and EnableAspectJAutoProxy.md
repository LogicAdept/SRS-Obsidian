<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Instrumentation #Java/Spring/Framework/AOP #Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps that contrast Spring AOP with AspectJ name both annotations:

- `@EnableAspectJAutoProxy` — Spring AOP: process `@Aspect` beans and build **proxies**. AspectJ here is the annotation style, not bytecode weaving.
- `@EnableLoadTimeWeaving` — AspectJ **load-time weaving**: bytecode change at class load, used when dumps want AspectJ LTW (often with `aspectjWeaving = ENABLED`).

You can use AspectJ aspects alongside Spring AOP; the two enable annotations are not interchangeable.

> [!warning] Unverified traps from the dump
> - The “AspectJ” in `@EnableAspectJAutoProxy` does not mean LTW is on.
> - Enabling both without an agent/`aop.xml` still leaves you on proxies for the auto-proxy side.
