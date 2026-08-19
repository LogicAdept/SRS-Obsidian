<!--
reps: 0
priority: 0
-->
#Java/Spring/Boot/Embedded #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Yes. Set `spring.main.web-application-type=none` so Boot does not start an embedded servlet or reactive server. Use this for CLI jobs, Kafka consumers, or batch workers that should not bind a port.

Related: you can also exclude web auto-configuration, but the property is the dump’s direct answer.

> [!warning] Unverified traps from the dump
> - A `spring-boot-starter-web` dependency still sits on the classpath; `none` stops Boot from creating a web context, it does not remove the jars.
> - `SERVLET` vs `REACTIVE` vs `NONE` are the three `WebApplicationType` values.
