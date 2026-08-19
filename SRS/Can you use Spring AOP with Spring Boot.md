<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/AOP #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Yes. Dumps: Boot auto-configures AOP when the right starter/dependencies are on the classpath (`spring-boot-starter-aop`). You still write `@Aspect` beans; you often skip a manual `@EnableAspectJAutoProxy`.

> [!warning] Unverified traps from the dump
> - Without the AOP starter, @Aspect classes may sit unused.
