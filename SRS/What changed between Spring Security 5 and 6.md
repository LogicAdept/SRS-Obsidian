<!--
reps: 0
priority: 0
-->
#Java/Spring/Security #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump interview tip: (1) composition not inheritance — SecurityFilterChain @Bean, WebSecurityConfigurerAdapter gone. (2) AuthorizationManager replaces the voter / AccessDecisionManager pattern. (3) SecurityContextHolderFilter and more explicit context save — fewer accidental sessions on stateless APIs. Also jakarta.* and @EnableMethodSecurity.
> [!warning] Unverified traps from the dump
> - authorizeRequests / antMatchers still compile in some 5.x-style snippets and are the dump signal you have not moved to 6.
