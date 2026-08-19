<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/MethodSecurity #Java/Spring/Framework/Testing #Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump test annotations: @WithAnonymousUser runs the test as the anonymous Authentication (ROLE_ANONYMOUS), opposite of @WithMockUser. Used to prove method security denies unauthenticated calls without standing up SecurityFilterChain.
> [!warning] Unverified traps from the dump
> - Anonymous is still an Authentication. Tests that only check getAuthentication() != null will pass when they should fail.
