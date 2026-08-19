<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebSocket #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Spring bean for pushing STOMP messages from any component (service, scheduler, listener), not only from a `@MessageMapping` return. `convertAndSend("/topic/notifications", payload)` broadcasts. `convertAndSendToUser(username, "/queue/reply", payload)` targets one user.

Dumps: this is how the server talks first without a client SEND into a controller.

> [!warning] Unverified traps from the dump
> - `convertAndSend` to `/topic` is public. User targeting requires `convertAndSendToUser` plus `/user` subscribe on the client.

