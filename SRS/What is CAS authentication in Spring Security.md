<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/Authentication #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps call it Central Authentication Server (CAS): enterprise central login. Spring Security ships supporting classes so the app redirects to the CAS server instead of collecting passwords locally.

It is listed with form login, OAuth2, SAML, remember-me, JAAS, and X.509 as a built-in mechanism.
> [!warning] Unverified traps from the dump
> - CAS here is the Yale/Apereo protocol, not compare-and-swap.
