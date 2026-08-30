<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/Authentication #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

ROLE_ANONYMOUS is the authority Spring Security’s anonymous authentication filter assigns to an unauthenticated caller (on by default). Dumps prefer isAnonymous() over matching that role by name.

ROLE_USER has no built-in meaning. You assign it when you load UserDetails. intercept-url access="ROLE_USER" only works if you actually grant that authority after login.
> [!warning] Unverified traps from the dump
> - Anonymous is not the same as permitAll. Anonymous users still fail authenticated() rules.
> - Disabling anonymous authentication makes unauthenticated requests have a null Authentication instead of ROLE_ANONYMOUS.
