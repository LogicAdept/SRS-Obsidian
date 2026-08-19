<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/FilterChain #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump: http.cors() / http.cors(Customizer.withDefaults()) plus a CorsConfigurationSource bean (UrlBasedCorsConfigurationSource, allowed origins/methods/headers, optionally allowCredentials).

This is the Security filter-chain CORS, distinct from WebMvcConfigurer.addCorsMappings. Security’s CorsFilter must run for authenticated APIs or the browser preflight never reaches MVC.
> [!warning] Unverified traps from the dump
> - MVC-only CORS can still fail once Spring Security is on the classpath because the security chain answers first.
