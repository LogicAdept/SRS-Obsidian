<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebSocket #Networking/Web/Protocols/WebSocket #SRS

# How does the WebSocket handshake work in Spring?

> [!abstract] Short answer
> The client sends an **HTTP GET** with **`Upgrade: websocket`**, **`Connection: Upgrade`**, **`Sec-WebSocket-Key`**, and **`Sec-WebSocket-Version: 13`**. A compliant server answers **`101 Switching Protocols`** and **`Sec-WebSocket-Accept`**. In Spring, that HTTP request hits **`WebSocketHttpRequestHandler`** (often via **`DispatcherServlet`**). **`HandshakeInterceptor.beforeHandshake`** may abort; **`HandshakeHandler.doHandshake`** (`DefaultHandshakeHandler` / `AbstractHandshakeHandler`) validates the request and delegates the upgrade to a container **`RequestUpgradeStrategy`**. Success yields a **`WebSocketSession`** and **`WebSocketHandler.afterConnectionEstablished`**.

## RFC 6455 first, then Spring’s objects

`Sec-WebSocket-Accept` is Base64(SHA-1(key + GUID `258EAFA5-E914-47DA-95CA-C5AB0DC85B11`)). Any non-101 status leaves **HTTP** in charge. Protocol overview: [[What is WebSocket]].

Spring’s **`HandshakeHandler`** copies handshake **attributes** onto the session (the original map is not reused). **`DefaultHandshakeHandler`** (4.0) is the Servlet bean; **`AbstractHandshakeHandler`** (4.2) does the real work: check `Upgrade` / `Connection`, version, origin hook, sub-protocol (`SubProtocolCapable` or `setSupportedProtocols`), extensions, **`determineUser`** (default `ServerHttpRequest.getPrincipal()`), then **`RequestUpgradeStrategy`**. Interceptors: [[What is a HandshakeInterceptor for WebSocket]]. Session: [[What is WebSocketSession]]. Mapping: [[What is WebSocketConfigurer]], [[What is the EnableWebSocket annotation]].

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

**Listing 1.** Conceptual: register a path; interceptors run **before** the upgrade. `.setHandshakeHandler(...)` swaps in a custom `DefaultHandshakeHandler` (custom origin, `RequestUpgradeStrategy`, sub-protocols). XML: `<websocket:handshake-interceptors>`.

Same-origin is the **registry** default since Framework **4.1.5** (`OriginHandshakeInterceptor` / `setAllowedOrigins`). **`AbstractHandshakeHandler.isValidOrigin`** itself treats origins as valid unless you override it. SockJS uses the same handshake URL plus extra HTTP transports: [[What is SockJS]].

```d2
direction: down
get: "HTTP GET Upgrade" {
  width: 220
  height: 40
  style.fill: "#e3f2fd"
}
hi: "HandshakeInterceptor.beforeHandshake" {
  width: 300
  height: 40
  style.fill: "#fff3e0"
}
hh: "HandshakeHandler.doHandshake" {
  width: 280
  height: 40
  style.fill: "#e8f5e9"
}
up: "RequestUpgradeStrategy → 101" {
  width: 260
  height: 40
  style.fill: "#fce4ec"
}
sess: "WebSocketSession + handler" {
  width: 260
  height: 40
  style.fill: "#f3e5f5"
}

get -> hi
hi -> hh
hh -> up
up -> sess
```

**Fig. 1.** `beforeHandshake` returning **`false`** never reaches `doHandshake`. STOMP CONNECT frames happen **after** this HTTP upgrade.

> [!warning]Upgrade-stripping proxies never see 101
> A proxy or load balancer that drops **`Upgrade`** keeps the exchange as ordinary HTTP. SockJS is the documented fallback, not a retry of the same native WebSocket URL. Nginx / cloud fronts need an explicit WebSocket pass-through.

> [!tip] Interview answer
> **Handshake is HTTP Upgrade to 101, then one TCP socket.** Spring runs interceptors, then `DefaultHandshakeHandler` plus a server `RequestUpgradeStrategy`. Attributes from the interceptor land on `WebSocketSession`. Origin checks are a registry interceptor (same-origin since 4.1.5), not “the handler always rejects foreign Origin.”
