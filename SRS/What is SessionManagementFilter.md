<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/FilterChain #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

InterviewBit-style dump: SessionManagementFilter plus SessionAuthenticationStrategy handle session timeouts, concurrent sessions, and session-fixation protection as the request flows through the chain.
> [!warning] Unverified traps from the dump
> - STATELESS chains still may include session machinery unless you disable it. Dumps pair csrf.disable() with SessionCreationPolicy.STATELESS for JWT APIs.
