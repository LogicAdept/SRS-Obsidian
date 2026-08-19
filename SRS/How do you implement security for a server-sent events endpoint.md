<!--
reps: 0
priority: 0
-->
#Java/Spring/Security #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps protect /sse/** with authenticated() (often HTTP Basic) and return SseEmitter from a controller. The stream is just another HTTP GET that must pass the filter chain before events are written.

Long-lived connections still need the SecurityContext on that request; session timeout can kill the stream.
> [!warning] Unverified traps from the dump
> - SSE is GET. CSRF is not the issue; authentication of the initial request is.
