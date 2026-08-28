<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebSocket #SRS

# What is `WebSocketMessageBrokerConfigurer`?

> [!abstract] Short answer
> **`WebSocketMessageBrokerConfigurer`** (Framework 4.0) customizes **`@EnableWebSocketMessageBroker`**. Methods are **`default`**: you override what you need. The two you almost always override are **`registerStompEndpoints`** and **`configureMessageBroker`**. It does **not** register a raw **`TextWebSocketHandler`**.

## Callbacks on the STOMP stack

| Method | Role |
| --- | --- |
| `registerStompEndpoints` | Handshake URL(s), optional SockJS |
| `configureMessageBroker` | `/app` prefix, simple broker or relay |
| `configureWebSocketTransport` | Message size / send limits |
| `configureClientInboundChannel` / `Outbound` | Client `MessageChannel` thread pools (**default size 1**) |
| `configureMessageConverters` | Payload converters for `@MessageMapping` / `SimpMessagingTemplate`; `true` keeps defaults |
| `addArgumentResolvers` / `addReturnValueHandlers` | Extra controller types (does **not** replace built-ins) |
| `getPhase` | `SmartLifecycle` phase; **`null`** lets others decide, else first non-null wins (Boot: **0** so beans start before the web server) |

```java
@Configuration
@EnableWebSocketMessageBroker
public class MyConfiguration implements WebSocketMessageBrokerConfigurer {

	@Override
	public void registerStompEndpoints(StompEndpointRegistry registry) {
		registry.addEndpoint("/portfolio").withSockJS();
	}

	@Override
	public void configureMessageBroker(MessageBrokerRegistry registry) {
		registry.setApplicationDestinationPrefixes("/app");
		registry.enableSimpleBroker("/topic", "/queue");
	}
}
```

**Listing 1.** Conceptual (imports omitted): javadoc-style STOMP setup (relay variant uses `enableStompBrokerRelay`). Enable annotation: [[What is the EnableWebSocketMessageBroker annotation]]. STOMP: [[What is STOMP in Spring WebSocket]]. Sending: [[What is SimpMessagingTemplate]]. Raw handlers: [[What is WebSocketConfigurer]].

Boot’s **`WebSocketMessagingAutoConfiguration`** also implements this interface **when** `DelegatingWebSocketMessageBrokerConfiguration` is already a bean: Jackson `MappingJackson2MessageConverter` plus inbound/outbound executors. It does **not** replace your endpoint registration.

```d2
direction: down
ifc: "WebSocketMessageBrokerConfigurer" {
  width: 300
  height: 40
  style.fill: "#e3f2fd"
}
stomp: "registerStompEndpoints" {
  width: 260
  height: 40
  style.fill: "#fff3e0"
}
broker: "configureMessageBroker" {
  width: 260
  height: 40
  style.fill: "#e8f5e9"
}

ifc -> stomp
ifc -> broker
```

**Fig. 1.** Handshake and broker are separate overrides. Skipping both leaves imported infrastructure with no public STOMP URL.

> [!warning]Default channels are size 1
> Inbound and outbound client channels use a **pool of 1** unless you `configureClientInboundChannel` / `Outbound`. Fine for a demo; production STOMP needs a real executor. `addArgumentResolvers` **adds** resolvers; it does not wipe Spring’s.

> [!tip] Interview answer
> **`WebSocketMessageBrokerConfigurer` is the STOMP configuration SPI for `@EnableWebSocketMessageBroker`.** Register the handshake endpoint and the broker prefixes. Other methods tune transport, converters, and channel thread pools. It is not `WebSocketConfigurer` and it will not map a `TextWebSocketHandler`.
