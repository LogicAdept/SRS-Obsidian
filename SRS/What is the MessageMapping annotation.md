<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebSocket #Java/Annotations #SRS

# What is the `@MessageMapping` annotation?

> [!abstract] Short answer
> **`@MessageMapping`** (Framework 4.0, `org.springframework.messaging.handler.annotation`) maps a **message destination** to a `@Controller` method — STOMP **SEND** (and other messages) after the **application prefix** is stripped. Client **`SEND /app/greeting`** with `setApplicationDestinationPrefixes("/app")` hits **`@MessageMapping("/greeting")`**. It is **not** `@RequestMapping`: `@GetMapping` never sees STOMP frames. Also used for RSocket responders; STOMP is the WebSocket case.

## Destination mapping, not HTTP

Supported on **type and method**. Patterns are Ant-style (`/thing/**`, `/thing/{id}`) plus **`@DestinationVariable`**. Type-level mapping is a shared prefix. Arguments: `Message`, headers / `StompHeaderAccessor`, `@Payload` (optional — unmatched args are the payload; JSON via `MessageConverter`; `@Validated` allowed), `@Header`/`@Headers`, **`Principal`** from the **HTTP handshake**. Return: serialized onto **`brokerChannel`**. Default outbound destination is the inbound destination with **`/app` replaced by `/topic`** (so `/app/greeting` → `/topic/greeting`). Customize with [[What is the SendTo annotation]] / [[What is the SendToUser annotation]]. Async: `CompletableFuture` / `CompletionStage`. Prefixes: [[What is the difference between the app prefix and topic prefix]]. STOMP: [[What is STOMP in Spring WebSocket]]. Template instead of a return: [[What is SimpMessagingTemplate]].

```java
@Controller
public class GreetingController {

	@MessageMapping("/greeting")
	public String handle(String greeting) {
		return greeting;
	}
}
```

**Listing 1.** Conceptual: payload is the `String` (implicit `@Payload`). Put mapping annotations on the **interface** if you proxy the controller.

`@SubscribeMapping` is a specialization that matches **SUBSCRIBE** only ([[What is SubscribeMapping]]). Exceptions: `@MessageExceptionHandler` ([[How do you handle STOMP errors in Spring]]).

```d2
direction: down
send: "STOMP SEND /app/greeting" {
  width: 260
  height: 40
  style.fill: "#e3f2fd"
}
map: "@MessageMapping /greeting" {
  width: 260
  height: 40
  style.fill: "#fff3e0"
}
out: "broker /topic/greeting" {
  width: 240
  height: 40
  style.fill: "#e8f5e9"
}

send -> map
map -> out
```

**Fig. 1.** Handshake URL `/portfolio` is not the mapping. Destinations live in STOMP headers.

> [!warning]Not an HTTP mapping
> `@GetMapping("/greeting")` does not receive `SEND /app/greeting`. Repeating `/app` on the annotation after `setApplicationDestinationPrefixes("/app")` looks up `/app/greeting` **after** the prefix was already stripped — the method misses.

> [!tip] Interview answer
> **`@MessageMapping` is STOMP’s `@RequestMapping`: destination after the `/app` prefix, payload converted, return goes to the broker (default `/topic` + rest of the path).** `@SendTo` / `@SendToUser` override the outbound destination. Use `SimpMessagingTemplate` when you need to send from a service or HTTP method.
