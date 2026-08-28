<!--
reps: 0
priority: 0
-->
#Java/Spring/Boot #Java/Spring/Framework/WebSocket #SRS

# What is `spring-boot-starter-websocket`?

> [!abstract] Short answer
> **`spring-boot-starter-websocket`** is Boot’s starter for **Spring MVC WebSocket**. On Boot **3.5** it pulls **`spring-boot-starter-web`**, **`spring-websocket`**, and **`spring-messaging`**. That is classpath and embedded-server WebSocket wiring — **not** a choice between raw handlers and STOMP. You still add **`@EnableWebSocket`** or **`@EnableWebSocketMessageBroker`**.

## What Boot actually auto-configures

Boot reference: WebSocket auto-configuration for **embedded Tomcat, Jetty, and Undertow**. A **WAR on a standalone container** is assumed to already have server WebSocket support. **`WebSocketServletAutoConfiguration`** (1.0+) installs the matching server initializer when Servlet + Jakarta WebSocket APIs and a servlet web app are present.

**`WebSocketMessagingAutoConfiguration`** (1.3+) is **`@ConditionalOnClass(WebSocketMessageBrokerConfigurer)`**. Its Jackson/converter inner config is **`@ConditionalOnBean(DelegatingWebSocketMessageBrokerConfiguration)`** — it runs **after** you enable the message-broker annotation, and does **not** call `registerStompEndpoints` for you.

Reactive apps are a **different** story: **`spring-boot-starter-webflux`** plus the Jakarta WebSocket API, not this starter.

```xml
<dependency>
	<groupId>org.springframework.boot</groupId>
	<artifactId>spring-boot-starter-websocket</artifactId>
</dependency>
```

**Listing 1.** Official Boot module name. Then a `@Configuration` from [[What is the difference between EnableWebSocket and EnableWebSocketMessageBroker]].

```d2
direction: down
st: "spring-boot-starter-websocket" {
  width: 280
  height: 40
  style.fill: "#e3f2fd"
}
deps: "starter-web + spring-websocket\n+ spring-messaging" {
  width: 280
  height: 50
  style.fill: "#fff3e0"
}
you: "@EnableWebSocket or\n@EnableWebSocketMessageBroker" {
  width: 280
  height: 50
  style.fill: "#e8f5e9"
}

st -> deps
deps -> you
```

**Fig. 1.** The starter is dependencies plus server customizers. Application mapping is still your config class. Raw: [[What is the EnableWebSocket annotation]]. STOMP: [[What is the EnableWebSocketMessageBroker annotation]].

> [!warning]Starter does not enable STOMP
> Adding the dependency without **`@EnableWebSocketMessageBroker`** (and a configurer) yields **no** `/app` broker. Without **`@EnableWebSocket`** and `addHandler`, there is **no** raw `/echo` either. Messaging auto-config only **decorates** converters/executors once the broker configuration bean exists.

> [!tip] Interview answer
> **`spring-boot-starter-websocket` brings `spring-websocket`, `spring-messaging`, and web, plus embedded-container WebSocket setup.** It does not pick STOMP versus `WebSocketHandler`. That is `@EnableWebSocket` or `@EnableWebSocketMessageBroker` in your configuration.
