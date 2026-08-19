<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/FilterChain #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

addFilterBefore(myFilter, SomeKnownFilter.class) inserts relative to that class. Dumps: if you meant UsernamePasswordAuthenticationFilter but named BasicAuthenticationFilter, your filter runs in the wrong phase — body already consumed, SecurityContext not ready, CORS not applied yet.

Enable TRACE on FilterChainProxy to print the ordered list at startup. Path mismatch (securityMatcher) means the chain — and your filter — never runs.
> [!warning] Unverified traps from the dump
> - Servlet FilterRegistrationBean @Order is a different ordering domain than the security filter chain.
