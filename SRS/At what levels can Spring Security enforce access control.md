<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/FilterChain #Java/Spring/Security/MethodSecurity #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps name two levels:

- Web/URL — servlet filter chain and authorizeHttpRequests on incoming HTTP.
- Method — AOP and @PreAuthorize / @Secured on service methods.

URL rules only guard the HTTP entry. Method security still applies if the same service is called from a scheduler, a listener, or another bean. Defense in depth is both.
> [!warning] Unverified traps from the dump
> - Method security is skipped on self-invocation and private methods because it is a proxy.
