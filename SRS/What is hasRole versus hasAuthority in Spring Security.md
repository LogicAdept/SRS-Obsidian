<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/Authentication #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Medium dump: hasRole('USER') automatically prefixes ROLE_ and looks for ROLE_USER. hasAuthority('READ_REPORTS') checks the exact string and does not add ROLE_.

So hasRole('ADMIN') is hasAuthority('ROLE_ADMIN'). If you store authority ADMIN without the prefix, hasRole('ADMIN') fails.
> [!warning] Unverified traps from the dump
> - This is the same ROLE_ convention as role vs authority cards; the interview prompt is specifically the two matcher methods.
