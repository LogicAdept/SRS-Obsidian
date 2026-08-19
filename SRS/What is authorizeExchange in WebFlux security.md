<!--
reps: 0
priority: 0
-->
#Java/Spring/Security #Java/Spring/Framework/WebFlux #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump ServerHttpSecurity DSL: authorizeExchange() then pathMatchers("/public/**").permitAll() and anyExchange().authenticated(). That is authorizeHttpRequests for reactive apps.

Gateway dumps use the same pattern plus oauth2Login and oauth2ResourceServer().jwt().
> [!warning] Unverified traps from the dump
> - authorizeRequests() on ServerHttpSecurity is the wrong API.
