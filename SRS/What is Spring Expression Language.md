<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC/SpEL #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

SpEL (Spring Expression Language) evaluates expressions at runtime against beans and the environment. Dumps place it on `@Value`, XML, and Spring Security method security (`hasRole`, argument SpEL).

`@Value("#{…}")` is SpEL; `@Value("${…}")` is a property placeholder (often confused with SpEL).

> [!warning] Unverified traps from the dump
> - `${}` vs `#{}` is the usual mix-up.
> - Security SpEL (`@PreAuthorize`) is the same language, different evaluation context.
