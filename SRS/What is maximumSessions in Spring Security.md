<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/SessionManagement #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

GFG-style dump: sessionManagement maximumSessions(1) plus ConcurrentSessionFilter limits how many simultaneous sessions a user may have. maxSessionsPreventsLogin(true) rejects the new login; false expires the old session.
> [!warning] Unverified traps from the dump
> - STATELESS JWT APIs have no server session to count. This is cookie-session concurrency.
