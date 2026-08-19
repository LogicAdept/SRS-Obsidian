<!--
reps: 0
priority: 0
-->
#Java/Spring/Cloud/Config #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Spring Cloud Config is server-side and client-side support for **externalized configuration in a distributed system**. Applications fetch properties from a centralized Config Server (often Git-backed) instead of only from packaged `application.yml`.

Clients typically use `spring-cloud-starter-config` and identify themselves with `spring.application.name`. Values are then available as usual (`@Value`, `@ConfigurationProperties`, `Environment`).

Dumps still mention `bootstrap.properties` as the place that bootstraps the config client **before** the main application context. `@RefreshScope` is the usual follow-up for refreshing beans without a full restart (title-only in some lists).

> [!warning] Unverified traps from the dump
> - Config is loaded at startup by default; changing the Git file does not update running beans until refresh.
> - `bootstrap.properties` is legacy relative to `spring.config.import=configserver:` in newer Boot/Cloud — verify the version you interview for.
