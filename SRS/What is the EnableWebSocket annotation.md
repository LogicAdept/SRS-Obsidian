<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebSocket #Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

`@EnableWebSocket` turns on the low-level handler model. A `@Configuration` implements `WebSocketConfigurer` and `registerWebSocketHandlers` maps a `TextWebSocketHandler` (or binary) to a path such as `/user` or `/websocket`.

This is the echo/chat style in dumps: `handleTextMessage(WebSocketSession, TextMessage)` and `session.sendMessage(...)`. No STOMP broker.

> [!warning] Unverified traps from the dump
> - Do not confuse with `@EnableWebSocketMessageBroker`, which is the STOMP/broker stack.

