<!--
reps: 0
priority: 0
-->
#Java/Spring/Security #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump options: wrap the Executor in DelegatingSecurityContextExecutor (copies context when the task is submitted), or MODE_INHERITABLETHREADLOCAL for true child threads. @Async without one of these sees an empty SecurityContextHolder.
> [!warning] Unverified traps from the dump
> - WebAsyncManagerIntegrationFilter helps Spring MVC async on the request, not your own Executors.newFixedThreadPool.
