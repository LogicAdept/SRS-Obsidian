<!--
reps: 0
priority: 0
-->
#Java/Spring/Security #Java/Spring/Framework/WebFlux #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump: ServerHttpSecurity authorizeExchange().pathMatchers("/public/**").permitAll(). pathMatchers is the reactive URL matcher (Ant-style in dumps), not servlet requestMatchers.

anyExchange() is the catch-all after specific pathMatchers.
> [!warning] Unverified traps from the dump
> - Order still matters: a broad pathMatchers("/**") first shadows later rules.
