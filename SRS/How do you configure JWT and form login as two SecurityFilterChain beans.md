<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/FilterChain #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps: two @Bean SecurityFilterChain methods. API chain @Order(1) with securityMatcher("/api/**"), STATELESS, csrf.disable(), JWT/Bearer filter. UI chain later with formLogin. First match wins.
> [!warning] Unverified traps from the dump
> - A UI chain without a matcher at a lower order number will also match /api/** and starve the JWT chain.
