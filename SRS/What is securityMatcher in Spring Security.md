<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/FilterChain #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps: http.securityMatcher("/api/**") scopes that SecurityFilterChain to URLs that match. FilterChainProxy asks each chain matches(request) in @Order; the first yes wins.

Use it when you have more than one chain — JWT + STATELESS on /api/**, form login on the rest. Without a matcher, a chain typically claims every request.
> [!warning] Unverified traps from the dump
> - securityMatcher selects which chain runs. authorizeHttpRequests requestMatchers are rules inside the chosen chain. Mixing the two names in an interview is a common slip.
> - A catch-all chain at @Order(1) with no matcher means later chains never see the request.
