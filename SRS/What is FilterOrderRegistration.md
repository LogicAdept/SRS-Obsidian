<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/FilterChain #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump: each default filter has a position constant (100, 200, … 1500). FilterOrderRegistration is the map addFilterBefore/After/At consult so your custom filter lands next to CsrfFilter or UsernamePasswordAuthenticationFilter instead of at a random servlet order.
> [!warning] Unverified traps from the dump
> - Servlet Filter registration order in web.xml is not this map. Spring Security filters live inside FilterChainProxy, not as sibling Tomcat filters.
