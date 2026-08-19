<!--
reps: 0
priority: 0
-->
#Java/Spring/Security #Security/AppSec #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump: you cannot put the CSRF token in a form parameter for JSON. Put it in a header instead (meta _csrf / _csrf_header, or X-XSRF-TOKEN with a cookie repository).

State-changing methods only; GET stays token-free.
> [!warning] Unverified traps from the dump
> - Content-Type application/json plus a missing CSRF header is a default 403, not a 401.
