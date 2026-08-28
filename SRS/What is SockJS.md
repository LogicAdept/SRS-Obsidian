<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebSocket #SRS

# What is SockJS?

> [!abstract] Short answer
> **SockJS** is a **WebSocket emulation** protocol: try a real WebSocket, then fall back to **HTTP streaming** or **HTTP long polling**, still exposing a WebSocket-like API. Spring’s Servlet stack implements the **server** (and, since 4.1, a **Java client**). Enable with **`.withSockJS()`** on a handler or STOMP endpoint. It is **not** STOMP and **not** a native `WebSocket()` URL.

## Why it exists, how the client probes

Public proxies may **drop `Upgrade`** or kill idle sockets. SockJS’s answer is: same application code, different transports at runtime. The JS client (sockjs-client **1.0.x** in the Framework 6.2 reference) starts with **`GET …/info`**, then picks **`websocket`**, else streaming, else long polling. HTTP transport URLs look like `{endpoint}/{server-id}/{session-id}/{transport}`. Framing: `o` open, `a[…]` JSON array of messages, `h` heartbeat (default **25 s** without other traffic), `c` close. Handshake of the WebSocket transport is still RFC 6455: [[How does the WebSocket handshake work in Spring]]. Protocol vs REST: [[What is WebSocket]]. STOMP can sit **on top**: [[What is STOMP in Spring WebSocket]].

```java
@Configuration
@EnableWebSocket
public class WebSocketConfiguration implements WebSocketConfigurer {

	@Override
	public void registerWebSocketHandlers(WebSocketHandlerRegistry registry) {
		registry.addHandler(myHandler(), "/myHandler").withSockJS();
	}

	@Bean
	public WebSocketHandler myHandler() {
		return new MyHandler();
	}
}
```

**Listing 1.** Conceptual: same `WebSocketHandler`, extra HTTP endpoints. STOMP equivalent: `registry.addEndpoint("/portfolio").withSockJS()`. Outside MVC: **`SockJsHttpRequestHandler`**. XML: `<websocket:sockjs/>`.

A **browser `WebSocket` constructor** talks native WebSocket only; it will **not** walk SockJS `/info` and xhr URLs. Use **sockjs-client** (and a STOMP library if you enabled the broker). Java: **`SockJsClient`** with `WebSocketTransport` plus `RestTemplateXhrTransport` / `JettyXhrTransport`. Heartbeats: if STOMP negotiates its own, **SockJS heartbeats are disabled**. `sessionCookieNeeded` defaults **true** (`JSESSIONID`). Cross-origin XHR: SockJS adds CORS unless the response already has CORS or `suppressCors` is set.

```d2
direction: down
info: "GET /info" {
  width: 200
  height: 40
  style.fill: "#e3f2fd"
}
ws: "WebSocket transport" {
  width: 220
  height: 40
  style.fill: "#e8f5e9"
}
http: "xhr-streaming / xhr-polling" {
  width: 260
  height: 40
  style.fill: "#fff3e0"
}

info -> ws: "if Upgrade works"
info -> http: "else emulate"
```

**Fig. 1.** Application handlers still receive `WebSocketSession`. SockJS wrapping (`SockJsWebSocketHandler`) is infrastructure.

> [!warning]Native WebSocket URLs skip SockJS
> `new WebSocket(url)` against a `.withSockJS()` endpoint does not speak SockJS framing or `/info`. Clients that cannot upgrade still fail unless they use a **SockJS client**. SockJS also does **not** replace `@EnableWebSocketMessageBroker`.

> [!tip] Interview answer
> **SockJS is fallback transport: WebSocket first, then HTTP streaming/polling, same handler API.** Enable with `.withSockJS()`. It is not STOMP. The JS `WebSocket` API will not use those fallbacks; sockjs-client will. Default heartbeat is 25 seconds unless STOMP heartbeats take over.
