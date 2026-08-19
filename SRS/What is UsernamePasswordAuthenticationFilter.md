<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/FilterChain #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

UsernamePasswordAuthenticationFilter is the dump’s default form-login filter. It reads username and password from the request, builds an unauthenticated UsernamePasswordAuthenticationToken, and calls AuthenticationManager.

Custom JWT/token dumps almost always addFilterBefore(theirFilter, UsernamePasswordAuthenticationFilter.class) so the bearer filter runs before form login. It is the usual landmark in the filter chain.
> [!warning] Unverified traps from the dump
> - Anchoring addFilterBefore on BasicAuthenticationFilter in a form-login app puts your filter in the wrong phase.
