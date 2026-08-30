<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/Authentication #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Interview dumps: JAAS is the low-level Java Authentication and Authorization Service. Spring Security can delegate authentication to JAAS LoginModule / handler classes instead of DaoAuthenticationProvider.

JAAS also appears in ‘essential features’ lists as one of the authentication options Spring can plug in.
> [!warning] Unverified traps from the dump
> - Most Boot apps never configure JAAS. Naming it is not the same as using form login.
