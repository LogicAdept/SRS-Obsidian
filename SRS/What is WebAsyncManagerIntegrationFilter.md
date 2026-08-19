<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/FilterChain #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump default chain (position ~0): WebAsyncManagerIntegrationFilter copies SecurityContext onto Spring MVC async dispatches (@Async on the request / WebAsyncManager), so the worker still sees Authentication.
> [!warning] Unverified traps from the dump
> - It does not wrap your own Executors.newFixedThreadPool. That still needs DelegatingSecurityContextExecutor.
