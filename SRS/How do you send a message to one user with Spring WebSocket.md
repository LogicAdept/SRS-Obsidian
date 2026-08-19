<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebSocket #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Use `SimpMessagingTemplate.convertAndSendToUser(username, "/queue/private", body)` or `@SendToUser`. Client subscribes to `/user/queue/private`. Spring keeps a per-user queue (`/user/queue/...`) and maps username to sessions.

`convertAndSendToUser` requires a `Principal` on the STOMP session. Without it, user messages drop with no error — called a hard-to-diagnose bug.

> [!warning] Unverified traps from the dump
> - convertAndSend to a /topic destination is not private even if the payload contains a user id.

