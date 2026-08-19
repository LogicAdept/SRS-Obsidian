<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebSocket #Java/Spring/Framework/WebMvc #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Extend `TextWebSocketHandler` or `BinaryWebSocketHandler`. Override `handleTextMessage(WebSocketSession, TextMessage)`, read payload, `session.sendMessage(...)`.

Register: `@EnableWebSocket` config implementing `WebSocketConfigurer`, `registry.addHandler(handler, "/user")`. Client: `new WebSocket('ws://localhost:8080/user')`.

> [!warning] Unverified traps from the dump
> - This path has no `/app` prefix and no `@MessageMapping`.
> - A `@Component` handler still must be registered; constructing `new SocketTextHandler()` in `addHandler` skips the Spring bean in one dump example.

