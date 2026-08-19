<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/FilterChain #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps: Spring picks a chain using bean discovery order, which is not stable across restarts. Result: intermittent 401s, or an actuator-only chain matching everything.

Always @Order, most specific securityMatcher first (for example /api/** then the catch-all UI chain). Only one chain runs per request.
> [!warning] Unverified traps from the dump
> - A second chain without securityMatcher matches all URLs and can steal traffic from the first.
