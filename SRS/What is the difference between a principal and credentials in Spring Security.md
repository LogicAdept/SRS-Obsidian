<!--
reps: 0
priority: 0
-->
#Java/Spring/Security #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump: principal is who (user, device, system). Credentials are how you prove it (password, token). The secured resource is what. After login, Authentication.getPrincipal() is often a UserDetails; credentials may be cleared.
> [!warning] Unverified traps from the dump
> - AnonymousAuthenticationFilter still installs a principal (anonymous). isAuthenticated() true on that token is a dump trick question.
