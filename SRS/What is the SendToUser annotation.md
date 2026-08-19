<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebSocket #Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

`@SendToUser` targets only the user/session that sent the request, not every subscriber of a `/topic`. Pair with client subscribe to `/user/queue/...`.

`convertAndSendToUser` is the programmatic form. Private chat dumps warn: `@SendTo("/topic/messages")` on a private handler leaks messages to everyone.

> [!warning] Unverified traps from the dump
> - User destinations still need a bound `Principal` for `convertAndSendToUser` to deliver.

