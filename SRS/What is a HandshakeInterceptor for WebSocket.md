<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebSocket #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Runs before the HTTP upgrade. Sample: extract a token, return false to deny. `afterHandshake` often empty. Used to authenticate before a `WebSocketSession` exists.

> [!warning] Unverified traps from the dump
> - Failing the interceptor is not the same as STOMP `ERROR` frames after CONNECT.

