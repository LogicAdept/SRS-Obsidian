<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebSocket #SRS

# What is a `HandshakeInterceptor` for WebSocket?

> [!abstract] Short answer
> **`HandshakeInterceptor`** (Framework 4.0, `org.springframework.web.socket.server`) hooks the **HTTP upgrade**. **`beforeHandshake`** inspects the request/response, may put entries on an **attributes** map that later become **`WebSocketSession.getAttributes()`**, and returns **`false` to abort** (no 101). **`afterHandshake`** runs after a handshake **attempt** (`exception` or `null`). If `beforeHandshake` returns **`false`**, Spring does **not** call `afterHandshake` on that interceptor. It is **not** a STOMP `ERROR` handler.

## Before the session exists

The attributes map is **copied**; mutating the original after return does not change the session. Built-in implementations: **`HttpSessionHandshakeInterceptor`** (copy HTTP session attributes and, by default, the HTTP session id under **`HTTP_SESSION_ID_ATTR_NAME`**; **`createSession` defaults to `false`**) and **`OriginHandshakeInterceptor`**. Register with **`WebSocketHandlerRegistry.addInterceptors`** or XML `<websocket:handshake-interceptors>`. Handshake pipeline: [[How does the WebSocket handshake work in Spring]]. Session map: [[What is WebSocketSession]]. Registration: [[What is WebSocketConfigurer]].

```java
@Configuration
@EnableWebSocket
public class WebSocketConfig implements WebSocketConfigurer {

	@Override
	public void registerWebSocketHandlers(WebSocketHandlerRegistry registry) {
		registry.addHandler(new MyHandler(), "/myHandler")
				.addInterceptors(new HttpSessionHandshakeInterceptor());
	}
}
```

**Listing 1.** Conceptual: the built-in interceptor copies servlet-session data **before** `WebSocketSession` exists. Your own interceptor can refuse the upgrade (`return false`) after checking a header or principal.

`afterHandshake` observes the **HTTP** result (status/headers), not WebSocket frames. `HandshakeInterceptorChain`: a `false` from interceptor *n* runs `afterHandshake` only on interceptors **0..n-1**. The aborting interceptor itself is skipped. STOMP `ERROR` frames are a later layer ([[What is STOMP in Spring WebSocket]]).

```d2
direction: down
before: "beforeHandshake" {
  width: 240
  height: 40
  style.fill: "#e3f2fd"
}
upgrade: "doHandshake → 101" {
  width: 240
  height: 40
  style.fill: "#fff3e0"
}
after: "afterHandshake (success or failure)" {
  width: 300
  height: 40
  style.fill: "#e8f5e9"
}
abort: "HTTP abort; no session" {
  width: 240
  height: 40
  style.fill: "#fce4ec"
}

before -> upgrade: "true"
before -> abort: "false"
upgrade -> after
```

**Fig. 1.** `false` skips `HandshakeHandler.doHandshake`. `HandshakeInterceptorChain` then calls `afterHandshake` only on interceptors that already returned true, not on the one that aborted.

> [!warning]Abort is not a STOMP ERROR frame
> `return false` stops the **HTTP** upgrade; the client never gets a `WebSocketSession`. That interceptor’s `afterHandshake` is **not** called. A later STOMP `CONNECT` failure is a **different** layer. `HttpSessionHandshakeInterceptor` will **not** create an HTTP session unless you `setCreateSession(true)`.

> [!tip] Interview answer
> **`HandshakeInterceptor` runs around the HTTP WebSocket upgrade.** `beforeHandshake` can copy attributes onto the future `WebSocketSession` or return false to deny. `HttpSessionHandshakeInterceptor` is the stock “copy HttpSession.” It is not `@MessageExceptionHandler` and not STOMP security.
