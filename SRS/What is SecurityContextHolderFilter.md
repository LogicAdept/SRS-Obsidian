<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/FilterChain #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump: SecurityContextHolderFilter loads SecurityContext from a SecurityContextRepository at request start and saves it at the end. Every request. If you remove it, SecurityContextHolder stays empty even after a successful login.

It is the Spring Security 6 replacement dump for the older SecurityContextPersistenceFilter in the default order (position ~100).
> [!warning] Unverified traps from the dump
> - Custom auth filters that run before this filter cannot read a restored session Authentication yet.
