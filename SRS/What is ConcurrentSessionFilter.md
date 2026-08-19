<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/FilterChain #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

InterviewBit dump: ConcurrentSessionFilter refreshes last-modified time of the session and checks the session has not expired under concurrent-session control.

Together with SessionManagementFilter it supports maximumSessions / maxSessionsPreventsLogin. JWT STATELESS apps do not use this filter’s session registry.
> [!warning] Unverified traps from the dump
> - maximumSessions without a SessionRegistry bean is an incomplete dump recipe.
