<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebSocket #Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

`@EnableWebSocketMessageBroker` enables WebSocket message handling backed by a broker and STOMP. Config class implements `WebSocketMessageBrokerConfigurer`: `registerStompEndpoints` (handshake URL, often `.withSockJS()`) and `configureMessageBroker` (`enableSimpleBroker`, `setApplicationDestinationPrefixes`).

> [!warning] Unverified traps from the dump
> - This is not `@EnableWebSocket`. Mixing both models on one app is not what these dumps show.

