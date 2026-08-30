<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/Authentication #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump Authentication.getDetails(): often WebAuthenticationDetails — remote IP and session id captured at login. Used in session-fixation and extra audit logs, not for hasRole.
> [!warning] Unverified traps from the dump
> - Details are not GrantedAuthority. Do not put roles in getDetails().
