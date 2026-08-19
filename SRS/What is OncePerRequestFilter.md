<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/FilterChain #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

JWT and custom-token dumps extend OncePerRequestFilter and override doFilterInternal so the logic runs once per request. Read Authorization, validate, set SecurityContextHolder, then chain.doFilter.

Register with addFilterBefore(..., UsernamePasswordAuthenticationFilter.class). GenericFilterBean is the other dump base class.
> [!warning] Unverified traps from the dump
> - FORWARD/ERROR dispatches can still surprise you if you assume ‘once’ means once per user click; the class is about the dispatcher type.
