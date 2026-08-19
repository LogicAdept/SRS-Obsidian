<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC/Configuration #Java/Spring/Boot/Properties #Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

`@Profile` binds a bean (or a whole `@Configuration`) to one or more profile names. Those definitions are registered only when a matching profile is active. Dumps say it is implemented on top of the more general `@Conditional`.

Example: a bean tagged `@Profile("dev")` exists in development and is absent in production if `dev` is not active. `@Profile("postgres")` vs `@Profile("mysql")` with `spring.profiles.active=mysql` in `application.properties`.

If a bean has no profile, dumps put it in the `"default"` profile. `spring.profiles.default` sets which profile is active when none is chosen.

> [!warning] Unverified traps from the dump
> - `@Profile` on a `@Configuration` class also gates its `@Bean` methods, `@Import`s, and `@ComponentScan`.
> - Profile expressions (`p1 & p2`) exist in later Spring; many dumps only show a single name.
