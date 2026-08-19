<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/FilterChain #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Implement Filter (dumps often use OncePerRequestFilter) and insert it in the chain with addFilterBefore / addFilterAfter / addFilterAt relative to a known filter (UsernamePasswordAuthenticationFilter is the dump landmark).

OncePerRequestFilter.doFilterInternal reads a header, builds Authentication, SecurityContextHolder.getContext().setAuthentication(auth), then chain.doFilter.
> [!warning] Unverified traps from the dump
> - A raw Filter registered only as a servlet filter may run twice or outside Spring Security’s order. Register it on HttpSecurity.
> - Always continue the chain (or write the response and return); swallowing the request without a status hangs the client.
