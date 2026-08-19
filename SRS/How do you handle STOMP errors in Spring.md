<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebSocket #Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Malformed or unknown destination can produce a STOMP `ERROR` frame. Controller-level: `@MessageExceptionHandler` plus `@SendTo("/topic/errors")` to publish `Error: ` + message to subscribers of that destination.

> [!warning] Unverified traps from the dump
> - That broadcasts errors on a topic; it is not automatically a private ERROR frame to the offending client.

