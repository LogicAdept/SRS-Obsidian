<!--
reps: 0
priority: 0
-->
#Java/Spring/Boot/AutoConfiguration #Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

`@EnableAutoConfiguration` tells Boot to auto-configure the context from the classpath and beans you already defined. It imports the candidate auto-configuration classes (each `@Conditional`).

You rarely write it: `@SpringBootApplication` already includes it.

> [!warning] Unverified traps from the dump
> - It does not mean every auto-config class on the classpath is applied — conditions still filter.
