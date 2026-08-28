<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebSocket #Java/Annotations #SRS

# What is the `@EnableWebSocket` annotation?

> [!abstract] Short answer
> **`@EnableWebSocket`** (Framework 4.0, `org.springframework.web.socket.config.annotation`) on an **`@Configuration`** class **`@Import`s `DelegatingWebSocketConfiguration`**, which collects every **`WebSocketConfigurer`** and calls **`registerWebSocketHandlers`**. That is how you map a **`WebSocketHandler`** (usually **`TextWebSocketHandler`** / **`BinaryWebSocketHandler`**) to an HTTP handshake path. It does **not** start a STOMP broker.

## Handler mapping, not destinations

`DelegatingWebSocketConfiguration` extends `WebSocketConfigurationSupport` and `@Autowired`s configurers. XML equivalent: `<websocket:handlers>`. Typical MVC setup lives in the **`DispatcherServlet`** config; you can also hang a handler off **`WebSocketHttpRequestHandler`** outside MVC.

```java
@Configuration
@EnableWebSocket
public class WebSocketConfiguration implements WebSocketConfigurer {

	@Override
	public void registerWebSocketHandlers(WebSocketHandlerRegistry registry) {
		registry.addHandler(myHandler(), "/myHandler")
				.addInterceptors(new HttpSessionHandshakeInterceptor());
	}

	@Bean
	public WebSocketHandler myHandler() {
		return new MyHandler();
	}
}
```

**Listing 1.** Conceptual (`MyHandler` omitted). `.withSockJS()` is optional on the registration. Handshake: [[How does the WebSocket handshake work in Spring]]. Handler: [[What is TextWebSocketHandler]]. Session: [[What is WebSocketSession]]. Configurer: [[What is WebSocketConfigurer]]. Contrast: [[What is the difference between EnableWebSocket and EnableWebSocketMessageBroker]].

JSR-356 sessions **do not allow concurrent sends**. Wrap **`WebSocketSession`** with **`ConcurrentWebSocketSessionDecorator`** if several threads write. Default decorator stack already adds logging and **`ExceptionWebSocketHandlerDecorator`** (uncaught exception → close **1011**).

Server knobs: **`ServletServerContainerFactoryBean`** (Jakarta) for buffer sizes; Jetty via **`DefaultHandshakeHandler`** + **`JettyRequestUpgradeStrategy`**. Allowed origins default to **same-origin** (4.1.5+).

```d2
direction: down
ann: "@EnableWebSocket" {
  width: 220
  height: 40
  style.fill: "#e3f2fd"
}
imp: "DelegatingWebSocketConfiguration" {
  width: 280
  height: 40
  style.fill: "#fff3e0"
}
reg: "WebSocketHandlerRegistry.addHandler" {
  width: 280
  height: 40
  style.fill: "#e8f5e9"
}

ann -> imp
imp -> reg
```

**Fig. 1.** The annotation only imports infrastructure. **No configurer and no `addHandler` means no endpoint.**

> [!warning]Not the STOMP switch
> **`@EnableWebSocketMessageBroker`** is the other annotation. Putting `@EnableWebSocket` on a class that only implements `WebSocketMessageBrokerConfigurer` does **not** register STOMP endpoints. Annotation with an **empty** `@Configuration` body also maps nothing.

> [!tip] Interview answer
> **`@EnableWebSocket` imports handler mapping for the raw WebSocket API.** Implement `WebSocketConfigurer`, `addHandler` on a path, extend `TextWebSocketHandler`. SockJS and origin checks are registration options. For `@MessageMapping` and a broker, you want `@EnableWebSocketMessageBroker` instead.
