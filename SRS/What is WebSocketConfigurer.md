<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebSocket #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Callback interface for `@EnableWebSocket`: `registerWebSocketHandlers(WebSocketHandlerRegistry)`. Maps handler beans/paths. MVC dump uses it with `TextWebSocketHandler`.

> [!warning] Unverified traps from the dump
> - STOMP config uses `WebSocketMessageBrokerConfigurer` instead.

