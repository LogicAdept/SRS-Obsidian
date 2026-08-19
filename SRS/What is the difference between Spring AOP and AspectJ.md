<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/AOP #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

AspectJ is the full AOP implementation (compile-time / load-time weaving, many join-point kinds: fields, constructors, …).

Spring AOP is **proxy-based** and, in typical use, only **method-execution** join points on Spring beans. It can use AspectJ *annotations* (`@Aspect`, `@Before`, …) so the programming model looks similar, but weaving is still Spring proxies unless you opt into AspectJ weaving.

Spring AOP is simpler (no weave step) and only advises beans that live in the Spring context.

> [!warning] Unverified traps from the dump
> - Self-invocation and `final`/`private` methods skip Spring proxies; AspectJ weaving can advise those call sites.
> - “Spring AOP uses AspectJ” means the annotation/pointcut language, not full AspectJ weaving by default.
