<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC/SpEL #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

`Environment` models the runtime: **profiles** and **properties**. Property access comes from `PropertyResolver`.

A profile is a named group of bean definitions registered only when that profile is active (`@Profile`, XML `beans profile="…"`). The `Environment` decides which profiles are active and which should be default.

Properties may come from files, JVM system properties, OS environment variables, JNDI, servlet context params, ad-hoc `Properties`/`Map`s. The `Environment` searches a chain of `PropertySource`s. `StandardEnvironment` starts with JVM system properties and OS environment variables.

> [!warning] Unverified traps from the dump
> - Boot’s `application-{profile}.properties` is the same `Environment` idea, not a second mechanism.
> - `@Value` and `Environment.getProperty` both read this chain; order of `PropertySource`s matters.
