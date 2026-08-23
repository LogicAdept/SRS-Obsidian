<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebSocket #Messaging #SRS

# Why use STOMP instead of raw WebSocket in Spring?

> [!abstract] Short answer
> **Raw WebSocket** is a low-level, full-duplex transport with **no message semantics**. **STOMP** is a messaging **sub-protocol** over WebSocket that adds destinations, subscriptions, and frame commands so Spring can route with **`@MessageMapping`**, talk to brokers, and apply Spring Security — the way HTTP enables Spring MVC over TCP.

## What raw WebSocket lacks

The WebSocket protocol (RFC 6455) opens one TCP connection and then carries opaque text or binary frames. Spring’s reference stresses that **until client and server agree on message meaning, a framework cannot route or process messages**. With only a raw socket you typically implement a single **`WebSocketHandler`** per connection and invent your own framing, topics, and ack model.

Clients and servers can negotiate a higher-level protocol via the **`Sec-WebSocket-Protocol`** header. Without that, every app invents its own convention.

## What STOMP adds for Spring apps

Using **STOMP as a sub-protocol** lets Spring Framework (and Spring Security) provide a richer programming model. Documented benefits:

- No need to invent a custom messaging protocol and message format
- Existing STOMP clients (including Spring’s Java client)
- Optional integration with message brokers (RabbitMQ, ActiveMQ, …) for subscriptions and broadcast
- Many **`@Controller`** classes with routing on the **STOMP destination header**, instead of one raw **`WebSocketHandler`**
- Security rules based on STOMP destinations and message types

That stack is what enables broker prefixes, **`@SendTo`**, and **`SimpMessagingTemplate`**-style publish semantics in a Spring WebSocket application.

```d2
direction: right
raw: "Raw WebSocket\nopaque frames" {
  width: 200
  height: 70
  style.fill: "#fce4ec"
}
stomp: "STOMP sub-protocol\ndestinations + commands" {
  width: 240
  height: 70
  style.fill: "#e8f5e9"
}
app: "@MessageMapping\nbroker / @SendTo" {
  width: 200
  height: 70
  style.fill: "#e3f2fd"
}

raw -> stomp -> app
```

**Fig. 1.** STOMP sits above WebSocket so Spring can route and broker messages.

```java
@Controller
public class ChatController {

    @MessageMapping("/chat")
    @SendTo("/topic/messages")
    public ChatMessage send(ChatMessage message) {
        return message;
    }
}
```

**Listing 1.** Conceptual STOMP mapping — destination-based routing is unavailable on a bare `WebSocketHandler` echo.

> [!warning] STOMP is not mandatory for every socket
> A **simple echo** or binary stream can use a raw **`WebSocketHandler`**. You need the **STOMP / message-broker stack** when you want destination routing, pub/sub brokers, and the annotation model. Choosing STOMP just to “use WebSockets” adds protocol and broker complexity you may not need. See [[What is STOMP in Spring WebSocket]] and [[What is SockJS]].

> [!tip] Interview answer
> Raw WebSocket only moves bytes; STOMP adds messaging semantics so Spring can route with @MessageMapping, use brokers, and secure destinations. Prefer STOMP when you need pub/sub and controllers; keep a plain WebSocketHandler for simple duplex streams.
