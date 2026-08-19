<!--
reps: 0
priority: 0
-->
#Java/Spring/Boot/Properties #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

A profile groups beans and config per environment. Dumps activate with, in increasing precedence among these:

- `spring.profiles.active=dev` in `application.properties` (lowest of this list)
- env `SPRING_PROFILES_ACTIVE`
- command line `java -jar app.jar --spring.profiles.active=prod`

`@Profile("prod")` on a `@Component` / `@Bean` makes it eligible only when that profile is active.

> [!warning] Unverified traps from the dump
> - Command-line `--spring.profiles.active` is not the same as a profile-specific file name.
