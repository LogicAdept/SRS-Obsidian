<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Instrumentation #Java/Spring/Framework/AOP #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Load-time weaving (LTW) weaves aspects into classes as the JVM loads them. Dumps present it for classes that were not compiled with AspectJ.

Dump steps:

1. Put `aspectjweaver` on the classpath (`spring-boot-starter-aop` plus the AspectJ weaver artifact).
2. Enable Spring LTW: `@EnableLoadTimeWeaving(aspectjWeaving = EnableLoadTimeWeaving.AspectJWeaving.ENABLED)` on the application / `@Configuration` class.
3. Add `META-INF/aop.xml` with a weaver `include` and the aspect class names.
4. Start the JVM with the AspectJ agent: `-javaagent:/path/to/aspectjweaver.jar`.

> [!warning] Unverified traps from the dump
> - `@EnableLoadTimeWeaving` is not the same as `@EnableAspectJAutoProxy` (that one stays proxy-based).
> - Dumps start the agent with `aspectjweaver.jar`. Missing the agent is a common “LTW did nothing” failure.
> - `@EnableLoadTimeWeaving` on a Boot main class is dump sample code; it may not weave classes already loaded before the context starts.
