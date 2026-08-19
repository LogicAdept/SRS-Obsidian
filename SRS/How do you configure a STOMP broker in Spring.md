<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebSocket #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

`configureMessageBroker`: `enableSimpleBroker("/topic", "/queue")` for an in-memory broker that fans out those prefixes. `setApplicationDestinationPrefixes("/app")` so client SEND to `/app/...` hits `@MessageMapping`.

`registerStompEndpoints`: `addEndpoint("/ws").setAllowedOriginPatterns("*").withSockJS()` (restrict origins in production).

> [!warning] Unverified traps from the dump
> - Simple broker is in-process; it does not fan out across app instances.
> - setAllowedOrigins star is called out as a production CORS mistake.

