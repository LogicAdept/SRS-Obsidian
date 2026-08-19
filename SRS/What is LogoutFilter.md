<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/FilterChain #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump default-order list: LogoutFilter intercepts the logout URL, invalidates the session, and clears SecurityContext. It sits after CsrfFilter and before form-login / OAuth2 redirect filters (dump position ~500).
> [!warning] Unverified traps from the dump
> - CSRF still applies to logout POST in cookie-session apps. GET logout without a CSRF token is a dump footgun.
