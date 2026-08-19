<!--
reps: 0
priority: 0
-->
#Java/Spring/Security #Security/AppSec #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps treat them as opposite problems.

CSRF defends against forged cookie-authenticated state-changing requests (synchronizer token; on by default). CORS is a browser relaxation of same-origin: which other origins may call your API (CorsConfigurationSource + http.cors()).

CORS is enforced by the browser, not as login. Disable CSRF only for stateless bearer APIs; you may still need CORS for a browser front end. They are separate filters: debug OPTIONS/CORS first, then CSRF 403 on the real POST.
> [!warning] Unverified traps from the dump
> - Disabling CSRF does not fix a CORS preflight failure, and vice versa.
