<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/FilterChain #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump pipeline:

1. Request hits security filters. If anonymous, DefaultLoginPageGeneratingFilter / AuthorizationFilter redirect to login.
2. UsernamePasswordAuthenticationFilter reads username/password, builds UsernamePasswordAuthenticationToken, calls ProviderManager.authenticate.
3. ProviderManager picks AuthenticationProvider (default DaoAuthenticationProvider).
4. DaoAuthenticationProvider calls UserDetailsService (dump example: InMemoryUserDetailsManager) then PasswordEncoder.matches.
5. Authenticated Authentication is stored in SecurityContext for later requests.

User → filters → ProviderManager → AuthenticationProvider → UserDetailsService → PasswordEncoder.
> [!warning] Unverified traps from the dump
> - JWT/Bearer dumps skip this form-login filter and set Authentication in a bearer filter instead.
