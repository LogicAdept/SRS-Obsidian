<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/FilterChain #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps place CorsFilter early in the chain so CORS preflight (OPTIONS) is handled before CSRF and authentication. http.cors(Customizer.withDefaults()) wires a CorsConfigurationSource bean.

Without it, a browser SPA on another origin fails preflight even if JWT auth is correct.
> [!warning] Unverified traps from the dump
> - CORS is not authentication. allowCredentials(true) plus allowedOrigins * is rejected by browsers.
