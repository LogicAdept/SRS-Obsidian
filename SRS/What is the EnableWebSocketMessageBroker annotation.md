<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebSocket #Java/Annotations #SRS

# What is the `@EnableWebSocketMessageBroker` annotation?

> [!abstract] Short answer
> **`@EnableWebSocketMessageBroker`** (Framework 4.0) on `@Configuration` **`@Import`s `DelegatingWebSocketMessageBrokerConfiguration`**: **broker-backed messaging over WebSocket** using a higher-level sub-protocol (STOMP in the reference). Customize by implementing **`WebSocketMessageBrokerConfigurer`**. Needs **`spring-messaging`** and **`spring-websocket`**. It is **not** `@EnableWebSocket`.

## Endpoints plus broker

Override at least:

1. **`registerStompEndpoints`** — HTTP URL for the WebSocket (or SockJS) handshake (`registry.addEndpoint("/portfolio")`, optional `.withSockJS()`).
2. **`configureMessageBroker`** — **`setApplicationDestinationPrefixes("/app")`** so those destinations hit **`@MessageMapping`** methods; **`enableSimpleBroker("/topic", "/queue")`** or **`enableStompBrokerRelay(...)`** for an external broker.

For the **simple broker**, `/topic` vs `/queue` is only a **convention** (pub-sub vs one consumer). An external broker has its own destination rules. STOMP overview: [[What is STOMP in Spring WebSocket]]. Prefixes: [[What is the difference between the app prefix and topic prefix]]. Broker setup: [[How do you configure a STOMP broker in Spring]]. Configurer: [[What is WebSocketMessageBrokerConfigurer]]. vs raw API: [[What is the difference between EnableWebSocket and EnableWebSocketMessageBroker]].

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

**Listing 1.** Conceptual (imports omitted): reference enable-STOMP shape. XML equivalent: `<websocket:message-broker>`.

Other configurer hooks: inbound/outbound **`MessageChannel`** (default **thread pool size 1** — customize in production), transport limits, `SimpMessagingTemplate` converters, `getPhase()` (Boot: a phase such as **0** so messaging beans start **before** the web server).

```d2
direction: down
ann: "@EnableWebSocketMessageBroker" {
  width: 280
  height: 40
  style.fill: "#e3f2fd"
}
ep: "STOMP endpoint / handshake" {
  width: 260
  height: 40
  style.fill: "#fff3e0"
}
app: "/app → @MessageMapping" {
  width: 240
  height: 40
  style.fill: "#e8f5e9"
}
broker: "simple broker or relay" {
  width: 240
  height: 40
  style.fill: "#fce4ec"
}

ann -> ep
ann -> app
ann -> broker
```

**Fig. 1.** Handshake path, application prefix, and broker prefixes are three separate registrations.

> [!warning]Annotation alone is not a working broker
> `@EnableWebSocketMessageBroker` on an empty `@Configuration` imports infrastructure but **does not** add `/portfolio` or `/app`. You still implement the configurer (or XML). Client STOMP `login`/`passcode` headers are **ignored/overridden** on the server in the documented browser example.

> [!tip] Interview answer
> **`@EnableWebSocketMessageBroker` is the STOMP-over-WebSocket switch: import broker configuration, register a handshake endpoint, set `/app` for controllers and `/topic`/`/queue` for the broker.** Use `WebSocketMessageBrokerConfigurer`, not `WebSocketConfigurer`. Simple broker vs relay is `enableSimpleBroker` vs `enableStompBrokerRelay`.
