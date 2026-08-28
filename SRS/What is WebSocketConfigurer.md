<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebSocket #SRS

# What is `WebSocketConfigurer`?

> [!abstract] Short answer
> **`WebSocketConfigurer`** (Framework 4.0) is the callback **`@EnableWebSocket`** looks for. Implement **`registerWebSocketHandlers(WebSocketHandlerRegistry)`** and call **`registry.addHandler(handler, paths…)`** (optional SockJS, interceptors, handshake handler, allowed origins). It is **not** `WebSocketMessageBrokerConfigurer`.

## One method, a registry of handlers

`DelegatingWebSocketConfiguration` injects all `WebSocketConfigurer` beans and invokes them in order. The registry’s `addHandler` returns a **`WebSocketHandlerRegistration`** for `.withSockJS()`, `.addInterceptors(...)`, `.setHandshakeHandler(...)`, `.setAllowedOrigins(...)`.

```java
@Configuration
@EnableWebSocket
public class WebSocketConfiguration implements WebSocketConfigurer {

	@Override
	public void registerWebSocketHandlers(WebSocketHandlerRegistry registry) {
		registry.addHandler(new MyHandler(), "/myHandler")
				.addInterceptors(new HttpSessionHandshakeInterceptor());
	}
}
```

**Listing 1.** Conceptual (`MyHandler` omitted): map a handler and copy HTTP session attributes into the WebSocket session. Handler types: [[What is TextWebSocketHandler]]. Enable annotation: [[What is the EnableWebSocket annotation]]. Handshake: [[How does the WebSocket handshake work in Spring]]. SockJS: [[What is SockJS]]. STOMP’s interface: [[What is WebSocketMessageBrokerConfigurer]].

A `@Configuration` can **be** the configurer (common) or you can expose a separate `@Bean` configurer; all are collected. XML: `<websocket:handlers>` / `<websocket:mapping>`.

Same-origin is the default for WebSocket and SockJS (4.1.5+). Allow-all is origin `*`.

```d2
direction: down
cfg: "WebSocketConfigurer" {
  width: 240
  height: 40
  style.fill: "#e3f2fd"
}
reg: "WebSocketHandlerRegistry" {
  width: 240
  height: 40
  style.fill: "#fff3e0"
}
path: "path → WebSocketHandler" {
  width: 240
  height: 40
  style.fill: "#e8f5e9"
}

cfg -> reg
reg -> path
```

**Fig. 1.** The interface does not configure `/app` prefixes or a message broker.

> [!warning]Wrong configurer for STOMP
> Implementing `WebSocketConfigurer` never calls `registerStompEndpoints`. `@MessageMapping` methods stay unused. Use [[What is the EnableWebSocketMessageBroker annotation]] plus `WebSocketMessageBrokerConfigurer`. Decorating handlers (logging, 1011 on uncaught errors) is already added by Java/XML WebSocket config.

> [!tip] Interview answer
> **`WebSocketConfigurer` is how `@EnableWebSocket` learns handler URL mappings.** `registerWebSocketHandlers` plus `addHandler`. Interceptors and SockJS hang off that registration. For STOMP destinations you implement a different interface.
