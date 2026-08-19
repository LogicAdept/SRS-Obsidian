<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/FilterChain #Security/AppSec #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

CsrfFilter checks the synchronizer token on POST/PUT/PATCH/DELETE. GET/HEAD/OPTIONS are skipped because they must not change state.

It runs after CORS in dump order lists. Missing token → 403 Invalid CSRF token. Stateless JWT dumps disable this filter via csrf.disable().
> [!warning] Unverified traps from the dump
> - A 403 on POST with a valid JWT is often CsrfFilter, not JwtDecoder.
