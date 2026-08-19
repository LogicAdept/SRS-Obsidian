<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/FilterChain #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump default order: RequestCacheAwareFilter restores the original pre-login request after redirect-to-login-and-back (SavedRequest / RequestCache). Position after Basic/Bearer in the dump table (~1100).
> [!warning] Unverified traps from the dump
> - STATELESS / JWT APIs usually have nothing useful in RequestCache. Form-login apps rely on it so POST /checkout survives the login round-trip.
