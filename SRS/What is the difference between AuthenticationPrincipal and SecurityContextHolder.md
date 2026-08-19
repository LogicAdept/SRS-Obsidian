<!--
reps: 0
priority: 0
-->
#Java/Spring/Security #Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump retrieve-user lists: SecurityContextHolder is the static ThreadLocal API (full Authentication). @AuthenticationPrincipal is MVC injection of the principal object. Principal as a method arg is only the username.

Dumps: use the annotation in controllers; do not scatter the static holder in services.
> [!warning] Unverified traps from the dump
> - Both still need the request thread (or a propagated context). The annotation is not magic across @Async.
