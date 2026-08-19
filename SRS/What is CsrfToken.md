<!--
reps: 0
priority: 0
-->
#Java/Spring/Security #Security/AppSec #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump: the synchronizer token CsrfFilter expects on POST/PUT/DELETE/PATCH. Stored in session or a cookie (CookieCsrfTokenRepository). AJAX dumps send it as X-CSRF-TOKEN. GET/HEAD/OPTIONS are not checked.
> [!warning] Unverified traps from the dump
> - httpOnly cookie + SPA that cannot read the cookie needs a non-httpOnly cookie or a header from a meta tag. CookieCsrfTokenRepository.withHttpOnlyFalse() is the dump SPA variant.
