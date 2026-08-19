<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/FilterChain #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

RememberMeAuthenticationFilter runs when the session has no Authentication. It reads the remember-me cookie, rebuilds Authentication, and puts it in the SecurityContext so the user is logged in without the form.

Dumps say it stores a persistent token in a cookie (and optionally in a store) after a successful login with the remember-me checkbox.
> [!warning] Unverified traps from the dump
> - STATELESS JWT APIs should not rely on this cookie. It is a session-cookie feature.
