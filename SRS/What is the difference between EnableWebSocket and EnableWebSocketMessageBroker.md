<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebSocket #Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

`@EnableWebSocket` + `WebSocketConfigurer`: register `WebSocketHandler`s, raw frames, `WebSocketSession`.

`@EnableWebSocketMessageBroker` + `WebSocketMessageBrokerConfigurer`: STOMP endpoints, `/app` vs `/topic` prefixes, `@MessageMapping`, in-memory or relay broker, `SimpMessagingTemplate`.

> [!warning] Unverified traps from the dump
> - Interview dumps often show only one of the two; name which stack you mean.

