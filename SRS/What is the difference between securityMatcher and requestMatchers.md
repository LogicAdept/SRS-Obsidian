<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/FilterChain #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump: securityMatcher (on HttpSecurity) decides whether this SecurityFilterChain handles the request at all. requestMatchers inside authorizeHttpRequests are authorization rules once the chain is selected.

FilterChainProxy uses the matcher first; AuthorizationFilter uses the rules second.
> [!warning] Unverified traps from the dump
> - Putting /api/** only in requestMatchers on a catch-all chain does not create a second chain. You still need securityMatcher + @Order for JWT vs form-login split.
