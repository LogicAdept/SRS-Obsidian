<!--
reps: 0
priority: 0
-->
#Java/Spring/Security #Security/AppSec #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Default CSRF storage is the HTTP session. CookieCsrfTokenRepository puts the token in a cookie so SPAs can read it.

Dump: CookieCsrfTokenRepository.withHttpOnlyFalse() so JavaScript can copy the cookie into the X-XSRF-TOKEN header. HttpOnly true blocks that. Pair with the AJAX header pattern on state-changing requests.
> [!warning] Unverified traps from the dump
> - withHttpOnlyFalse lets XSS steal the CSRF cookie. Dumps still recommend it for SPAs that cannot use a meta tag.
