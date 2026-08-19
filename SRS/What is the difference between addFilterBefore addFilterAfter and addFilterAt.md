<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/FilterChain #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps: addFilterBefore(your, Landmark.class) runs yours first, then the landmark. addFilterAfter is the reverse. addFilterAt places yours at the same FilterOrderRegistration slot as the landmark.

JWT / API-key auth dumps put the custom filter before UsernamePasswordAuthenticationFilter so SecurityContext is set before AnonymousAuthenticationFilter.
> [!warning] Unverified traps from the dump
> - addFilterAt does not replace the original filter — both run. To swap UsernamePasswordAuthenticationFilter, also disable form login.
> - A JWT filter after AnonymousAuthenticationFilter is a dump classic: anonymous Authentication is already set and your token is ignored.
