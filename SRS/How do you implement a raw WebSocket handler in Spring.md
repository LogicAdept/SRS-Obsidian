<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebSocket #Java/Spring/Framework/WebMvc #SRS

# How do you implement a raw WebSocket handler in Spring?

> [!abstract] Short answer
> **Extend `TextWebSocketHandler` or `BinaryWebSocketHandler`**, override **`handleTextMessage` / `handleBinaryMessage`**, and **`session.sendMessage(...)`**. Map it with **`@EnableWebSocket`** + **`WebSocketConfigurer.registerWebSocketHandlers`**: `registry.addHandler(handler, "/myHandler")`. That is the **raw WebSocket API** — **no** `/app` prefix, **no** `@MessageMapping` (those are STOMP). Include the config in the **`DispatcherServlet`** context, or use **`WebSocketHttpRequestHandler`** outside MVC.

## Handler, then URL mapping

`TextWebSocketHandler` (4.0): text only; **binary frames close with `CloseStatus.NOT_ACCEPTABLE`**. Other lifecycle methods default empty. JSR-356 sessions **do not allow concurrent sends** — wrap with **`ConcurrentWebSocketSessionDecorator`** if several threads write.

Java config example from the Framework reference: `@Bean` the handler, then `addHandler(myHandler(), "/myHandler")`. A handshake interceptor (for example `HttpSessionHandshakeInterceptor`) can copy HTTP session attributes onto `WebSocketSession`. Logging and **`ExceptionWebSocketHandlerDecorator`** (close **1011** on uncaught errors) are added by default with this config.

```java
public class MyHandler extends TextWebSocketHandler {

    @Override
    protected void handleTextMessage(WebSocketSession session, TextMessage message) {
        session.sendMessage(new TextMessage(message.getPayload()));
    }
}
```

**Listing 1.** Conceptual Framework handler. STOMP broker: [[How do you configure a STOMP broker in Spring]]. Handshake: [[What is a HandshakeInterceptor for WebSocket]]. MVC front controller: [[What is Spring MVC DispatcherServlet]].

```java
@Configuration
@EnableWebSocket
public class WebSocketConfiguration implements WebSocketConfigurer {

    @Override
    public void registerWebSocketHandlers(WebSocketHandlerRegistry registry) {
        registry.addHandler(myHandler(), "/myHandler")
                .setAllowedOrigins("https://mydomain.com");
    }

    @Bean
    public WebSocketHandler myHandler() {
        return new MyHandler();
    }
}
```

**Listing 2.** Conceptual mapping. Default since 4.1.5 is **same-origin only**. Browser client: `new WebSocket("ws://host/myHandler")` (path must match the registry). `*` allows all origins.

```d2
direction: down
http: "HTTP Upgrade\nDispatcherServlet" {
  width: 260
  height: 50
  style.fill: "#e3f2fd"
}
h: "TextWebSocketHandler\nhandleTextMessage" {
  width: 280
  height: 55
  style.fill: "#e8f5e9"
}
stomp: "STOMP /app + @MessageMapping\n(not this API)" {
  width: 300
  height: 55
  style.fill: "#fff3e0"
}

http -> h
```

**Fig. 1.** Raw handler vs message broker. Do not mix `/app` into this mapping unless you actually enable STOMP.

> [!warning] `new MyHandler()` vs a Spring bean
> `addHandler(new MyHandler(), "/x")` is **not** the scanned `@Component`. Need DI? Register a **`@Bean`** (as the docs do) and pass **that** instance into `addHandler`.

> [!warning] Concurrent `sendMessage`
> Overlapping sends on one JSR-356 session fail. Synchronize or use **`ConcurrentWebSocketSessionDecorator`**.

> [!warning] Origins
> Browsers are same-origin by default. `setAllowedOrigins("*")` opens every origin; list explicit `https://` hosts in production.

> [!tip] Interview answer
> **Raw WebSocket in Spring is `TextWebSocketHandler` plus `@EnableWebSocket` and `registry.addHandler(handler, "/path")`.** The browser talks `ws:` to that path. STOMP (`/app`, `@MessageMapping`) is a different stack on top of WebSocket, not this handler.
