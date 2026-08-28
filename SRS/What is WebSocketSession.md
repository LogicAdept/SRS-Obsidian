<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebSocket #SRS

# What is `WebSocketSession`?

> [!abstract] Short answer
> **`WebSocketSession`** (Framework 4.0, `org.springframework.web.socket`) is Spring’s handle for **one upgraded connection**: **`sendMessage`** (`TextMessage` / `BinaryMessage`), **`close`** (plain close = **1000** `NORMAL`), **`isOpen`**, handshake URI/headers, **`getAttributes()`**, **`getPrincipal()`**, negotiated sub-protocol and extensions, size limits. **`getId()`** is a **unique session identifier**, not a STOMP user name. The JSR-356 session **does not allow concurrent sends** — wrap with **`ConcurrentWebSocketSessionDecorator`**.

## After 101, this is the API

On the server, **`getAttributes()`** is filled from **`HandshakeInterceptor`** (copied map). On the client, from `WebSocketClient` handshake methods. **`getPrincipal()`** is **`null`** if the user was not authenticated. **`getLocalAddress()`** is not always available (Standard WebSocket client in 6.2.x synthesizes a host/port; 7.0 returns **`null`**). Handshake: [[How does the WebSocket handshake work in Spring]]. Interceptor attributes: [[What is a HandshakeInterceptor for WebSocket]]. Sending from a handler: [[What is TextWebSocketHandler]]. Protocol: [[What is WebSocket]].

```java
public class MyHandler extends TextWebSocketHandler {

	@Override
	public void handleTextMessage(WebSocketSession session, TextMessage message)
			throws Exception {
		if (session.isOpen()) {
			session.sendMessage(new TextMessage(message.getPayload()));
		}
	}
}
```

**Listing 1.** Conceptual echo. Several threads calling `sendMessage` on the same JSR-356 session is **undefined**; decorate the session. Default Java-config already adds logging and **`ExceptionWebSocketHandlerDecorator`** (uncaught → close **1011**).

STOMP’s **`SimpUserRegistry`** and user destinations key off **messaging** session/user names. Do not treat **`WebSocketSession.getId()`** as `simpUser`. Broker stack: [[What is STOMP in Spring WebSocket]].

```d2
direction: down
hs: "HTTP 101 + attributes" {
  width: 240
  height: 40
  style.fill: "#e3f2fd"
}
sess: "WebSocketSession" {
  width: 240
  height: 40
  style.fill: "#fff3e0"
}
ops: "sendMessage / close / isOpen" {
  width: 260
  height: 40
  style.fill: "#e8f5e9"
}

hs -> sess
sess -> ops
```

**Fig. 1.** The session object exists only after a successful upgrade. Sending in `afterConnectionClosed` is discouraged and usually fails.

> [!warning]getId is not the STOMP user
> `getId()` is an opaque connection id. User-targeted STOMP (`convertAndSendToUser`) uses the **user name** / `SimpUserRegistry`, not this string. Concurrent `sendMessage` without a decorator can fail even if `isOpen()` is true.

> [!tip] Interview answer
> **`WebSocketSession` is the raw connection: send text/binary, close, attributes from the handshake interceptor, optional Principal.** Wrap it for concurrent sends. Its id is not the STOMP username. Size limits are `setTextMessageSizeLimit` / `setBinaryMessageSizeLimit`.
