<!--
reps: 0
priority: 0
-->
#Java/Spring/Boot/AutoConfiguration #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump: `@SpringBootApplication(exclude = { DataSourceAutoConfiguration.class })`. Also `excludeName`, or `spring.autoconfigure.exclude`.

Classic case: a JDBC starter came in transitively and you do not want a `DataSource`.

> [!warning] Unverified traps from the dump
> - Excluding the auto-config does not remove the starter jars from the classpath.
