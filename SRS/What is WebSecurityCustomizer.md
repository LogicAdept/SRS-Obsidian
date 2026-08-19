<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/FilterChain #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump skip-security option 2: a WebSecurityCustomizer bean returns web -> web.ignoring().requestMatchers("/static/**", "/favicon.ico"). Those paths bypass the entire SecurityFilterChain — no filters at all.
> [!warning] Unverified traps from the dump
> - ignoring() is not permitAll(). No CORS headers, no security headers, no CSRF. Dumps say use it only for truly static resources.
