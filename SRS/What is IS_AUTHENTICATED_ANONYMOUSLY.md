<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/Authentication #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

XML intercept-url dump uses access="IS_AUTHENTICATED_ANONYMOUSLY" for login/index pages so unauthenticated callers may enter.

That is the old non-expression attribute. Expression dumps use permitAll or isAnonymous() instead of matching ROLE_ANONYMOUS by name.
> [!warning] Unverified traps from the dump
> - Anonymous is not authenticated(). isAnonymous() users still fail anyRequest().authenticated().
