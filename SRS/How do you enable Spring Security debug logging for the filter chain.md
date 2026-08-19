<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/FilterChain #Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump toolkit: logging.level.org.springframework.security=DEBUG (and FilterChainProxy TRACE), plus @EnableWebSecurity(debug = true) which prints the Security filter chain list for every request.
> [!warning] Unverified traps from the dump
> - @EnableWebSecurity(debug = true) dumps headers including Authorization bearer tokens. Interview lists mark it never-for-production.
