<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Instrumentation #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

LTW happens when a class is loaded: a special class loader (or agent) rewrites the target bytecode before the class is used. Interview dumps say both AspectJ and Spring ship load-time weavers so you can add that capability to the class loader with “simple configuration.”

Spring-side dump config is `@EnableLoadTimeWeaving` plus `META-INF/aop.xml` and a `-javaagent`. Spring AOP itself still weaves at runtime via proxies, not via this weaver.

> [!warning] Unverified traps from the dump
> - “Spring supports three weaving mechanisms” in some lists still means typical Spring AOP is runtime proxies unless you opt into AspectJ LTW.
> - A load-time weaver is not a Spring AOP proxy factory.
