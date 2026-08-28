<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebSocket #Java/Annotations #SRS

# What is `@MessageExceptionHandler` for STOMP?

> [!abstract] Short answer
> **`@MessageExceptionHandler`** (Framework 4.0, `org.springframework.messaging.handler.annotation`) handles exceptions thrown from **message-handling methods** (`@MessageMapping`, `@SubscribeMapping`) in that **handler class** (or globally from **`@ControllerAdvice`**). Exception types go in **`value`** or as a **method argument** (empty `value` uses the argument types). Signatures and returns match **`@MessageMapping`**. It is **not** MVC `@ExceptionHandler` for HTTP.

## Messaging analogue of `@ExceptionHandler`

Reference: typically scoped to the `@Controller` (and hierarchy) that declared it; put the method on **`@ControllerAdvice`** to apply across controllers — same idea as MVC, **different annotation**. Returns become outbound messages (`brokerChannel` / `@SendTo` / `@SendToUser`). Official error-to-caller pattern: **`@SendToUser(destinations = "/queue/errors", broadcast = false)`**. How-to: [[How do you handle STOMP errors in Spring]]. Mapping: [[What is the MessageMapping annotation]]. Private dest: [[What is the SendToUser annotation]]. Public dest: [[What is the SendTo annotation]].

```java
@Controller
public class MyController {

	@MessageExceptionHandler
	public ApplicationError handleException(MyException exception) {
		return appError;
	}
}
```

**Listing 1.** Conceptual: Framework 6.2 annotated-controllers sample. You can write `@MessageExceptionHandler(MyException.class)` instead of (or in addition to) the argument type.

This does **not** replace **STOMP ERROR** frames from `StompSubProtocolHandler` (malformed frames, unhandled processing). Those close the connection unless `StompEndpointRegistry.setErrorHandler` suppresses them. `@ExceptionHandler` on a Web MVC controller never sees a STOMP SEND.

```d2
direction: down
map: "@MessageMapping method" {
  width: 240
  height: 40
  style.fill: "#e3f2fd"
}
ann: "@MessageExceptionHandler" {
  width: 260
  height: 40
  style.fill: "#fff3e0"
}
out: "same return pipeline as mapping" {
  width: 280
  height: 40
  style.fill: "#e8f5e9"
}

map -> ann: "throws"
ann -> out
```

**Fig. 1.** Global coverage is `@ControllerAdvice` + `@MessageExceptionHandler`, not `@ExceptionHandler`.

> [!warning]Not MVC ExceptionHandler
> `@ExceptionHandler` in a `@RestControllerAdvice` handles **HTTP**. STOMP needs **`@MessageExceptionHandler`**. Pairing it with `@SendTo("/topic/errors")` still **broadcasts** the payload; use `@SendToUser` + `broadcast = false` for the calling session.

> [!tip] Interview answer
> **`@MessageExceptionHandler` catches exceptions from `@MessageMapping` methods, with the same argument and return model.** Scope is that controller unless you put it on `@ControllerAdvice`. Reply with `@SendToUser("/queue/errors")`, not HTTP `@ExceptionHandler` and not a public `/topic` unless you mean to broadcast.
