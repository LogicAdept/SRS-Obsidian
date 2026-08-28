<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebSocket #Messaging #SRS

# How do you configure a STOMP broker in Spring?

> [!abstract] Short answer
> Put **`@EnableWebSocketMessageBroker`** on `@Configuration` and implement **`WebSocketMessageBrokerConfigurer`**. **`registerStompEndpoints`**: `addEndpoint("/portfolio")` (optional `.withSockJS()`, origins). **`configureMessageBroker`**: **`setApplicationDestinationPrefixes("/app")`** so SEND to `/app/…` hits **`@MessageMapping`**; **`enableSimpleBroker("/topic", "/queue")`** or **`enableStompBrokerRelay("/topic", "/queue")`**. XML twin: `<websocket:message-broker>`.

## Two methods, three prefixes

Handshake path (`/portfolio`) is the **HTTP/WebSocket URL**. `/app` and `/topic` are **STOMP destination prefixes**, not that URL. Flow: [[What is the difference between the app prefix and topic prefix]]. Simple vs relay: [[What is a simple broker versus a STOMP broker relay]]. Annotation: [[What is the EnableWebSocketMessageBroker annotation]]. SPI: [[What is WebSocketMessageBrokerConfigurer]]. CORS on the endpoint: [[How do you register a STOMP endpoint with CORS]]. Protocol: [[What is STOMP in Spring WebSocket]].

```java
@Configuration
@EnableWebSocketMessageBroker
public class WebSocketConfiguration implements WebSocketMessageBrokerConfigurer {

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

**Listing 1.** Conceptual (imports omitted): Framework 6.2 enable-STOMP Java config. Relay instead of simple: `enableStompBrokerRelay("/topic", "/queue")` plus `reactor-netty` / `netty-all`. Prefixes without a trailing slash get one appended; **`@MessageMapping` must not repeat `/app`**.

Default return from a `@MessageMapping` method is a broker destination with **`/app` replaced by `/topic`**. Override with **`@SendTo`**. User queues use prefix `/user/` ([[What is SimpMessagingTemplate]]).

```d2
direction: down
ep: "registerStompEndpoints\n/portfolio handshake" {
  width: 280
  height: 50
  style.fill: "#e3f2fd"
}
app: "setApplicationDestinationPrefixes /app" {
  width: 300
  height: 40
  style.fill: "#fff3e0"
}
br: "enableSimpleBroker or enableStompBrokerRelay" {
  width: 320
  height: 40
  style.fill: "#e8f5e9"
}

ep -> app
ep -> br
```

**Fig. 1.** Empty `@EnableWebSocketMessageBroker` imports infrastructure but maps **no** handshake and **no** prefixes.

> [!warning]Simple broker is one JVM
> `enableSimpleBroker` keeps subscriptions **in memory**. A second app instance does not see them. For cluster fan-out use the relay ([[How do you scale Spring WebSocket across instances]]). `setAllowedOrigins("*")` is handshake CORS, not `/app` authorization.

> [!tip] Interview answer
> **Configure STOMP with `@EnableWebSocketMessageBroker`: handshake in `registerStompEndpoints`, `/app` plus simple broker or relay in `configureMessageBroker`.** `/portfolio` is the socket URL; `/app/greeting` is a STOMP destination. Simple broker is in-process; relay is RabbitMQ/ActiveMQ over TCP.
