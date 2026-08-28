<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebSocket #Java/Annotations #SRS

# What is the difference between `@EnableWebSocket` and `@EnableWebSocketMessageBroker`?

> [!abstract] Short answer
> **`@EnableWebSocket`** (Framework 4.0) imports **`DelegatingWebSocketConfiguration`** and turns on the **raw `WebSocketHandler` API**: map a `TextWebSocketHandler` / `BinaryWebSocketHandler` to a path, talk in **frames** on **`WebSocketSession`**. **`@EnableWebSocketMessageBroker`** imports **`DelegatingWebSocketMessageBrokerConfiguration`** and turns on **broker-backed messaging** (typically **STOMP**): handshake URL, `/app` vs `/topic`/`/queue`, `@MessageMapping`, simple broker or STOMP relay. They are **two `@Import` stacks**, not aliases.

## Two enable annotations, two configurers

| | `@EnableWebSocket` | `@EnableWebSocketMessageBroker` |
| --- | --- | --- |
| **Configurer** | [[What is WebSocketConfigurer]] | [[What is WebSocketMessageBrokerConfigurer]] |
| **You register** | `WebSocketHandler` paths | STOMP endpoints + broker |
| **Application code** | `handleTextMessage(session, message)` | `@MessageMapping` / `SimpMessagingTemplate` |
| **Modules** | `spring-websocket` | `spring-websocket` **and** `spring-messaging` |

STOMP still uses the WebSocket handler API **indirectly**. A `WebSocketMessageBrokerConfigurer` does **not** register your `TextWebSocketHandler`. The starter ([[What is spring-boot-starter-websocket]]) puts both modules on the classpath; **your `@Enable*` class chooses the model**. Details: [[What is the EnableWebSocket annotation]], [[What is the EnableWebSocketMessageBroker annotation]].

```java
@Configuration
@EnableWebSocket
class RawConfig implements WebSocketConfigurer {
	@Override
	public void registerWebSocketHandlers(WebSocketHandlerRegistry registry) {
		registry.addHandler(new EchoHandler(), "/echo");
	}
}

@Configuration
@EnableWebSocketMessageBroker
class StompConfig implements WebSocketMessageBrokerConfigurer {
	@Override
	public void registerStompEndpoints(StompEndpointRegistry registry) {
		registry.addEndpoint("/portfolio");
	}
	@Override
	public void configureMessageBroker(MessageBrokerRegistry config) {
		config.setApplicationDestinationPrefixes("/app");
		config.enableSimpleBroker("/topic", "/queue");
	}
}
```

**Listing 1.** Conceptual: pick **one** primary stack. Both annotations can exist in one JVM, but that is two message models, not “STOMP on top of your echo handler.”

```d2
direction: down
raw: "@EnableWebSocket\nWebSocketHandler frames" {
  width: 280
  height: 50
  style.fill: "#e3f2fd"
}
stomp: "@EnableWebSocketMessageBroker\nSTOMP + broker destinations" {
  width: 300
  height: 50
  style.fill: "#fff3e0"
}

raw -> stomp: "not a substitute"
```

**Fig. 1.** Name the stack in an interview. SockJS (`.withSockJS()`) is an option on **either** handshake, not a third enable annotation.

> [!warning]Same-origin default is not STOMP-specific
> Since Framework **4.1.5**, WebSocket **and** SockJS accept **same-origin** only unless you call `setAllowedOrigins` / `setAllowedOriginPatterns`. That applies to **both** enable annotations. `*` allows all origins.

> [!tip] Interview answer
> **`@EnableWebSocket` is the low-level handler API; `@EnableWebSocketMessageBroker` is STOMP plus a broker.** Implement `WebSocketConfigurer` vs `WebSocketMessageBrokerConfigurer`. The Boot starter does not pick for you. If you only remember one, say which model you mean.
