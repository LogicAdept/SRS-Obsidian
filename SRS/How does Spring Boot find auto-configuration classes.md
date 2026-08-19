<!--
reps: 0
priority: 0
-->
#Java/Spring/Boot/AutoConfiguration #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Boot 3 dumps: candidates are listed in `META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports` — one fully qualified class name per line.

Boot 2.x dumps: `META-INF/spring.factories` under the `EnableAutoConfiguration` key. Boot 2.7 deprecated that; Boot 3 dropped it for the `.imports` file.

`@EnableAutoConfiguration` (inside `@SpringBootApplication`) imports those candidates; each is still gated by `@Conditional`.

> [!warning] Unverified traps from the dump
> - A custom starter that still only has `spring.factories` silently does nothing on Boot 3.
