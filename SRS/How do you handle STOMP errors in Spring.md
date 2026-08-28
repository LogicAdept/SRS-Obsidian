<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebSocket #Java/Annotations #SRS

# How do you handle STOMP errors in Spring?

> [!abstract] Short answer
> Two layers. **Application exceptions** from `@MessageMapping` / `@SubscribeMapping`: **`@MessageExceptionHandler`** (same arguments and return types as `@MessageMapping`). Official private reply: **`@SendToUser(destinations = "/queue/errors", broadcast = false)`** so only the calling session gets a **MESSAGE**, not a broadcast. **Protocol / unhandled processing errors**: `StompSubProtocolHandler` sends a STOMP **ERROR** frame (message header) unless you **`registry.setErrorHandler(...)`**. STOMP **requires closing the connection after ERROR**.

## Catch in the controller, or customize ERROR frames

`@MessageExceptionHandler` lives on the `@Controller` (or globally on **`@ControllerAdvice`**). List exception types on the annotation or as a method argument. Return a payload like any mapping method. **`@SendTo("/topic/errors")` publishes to every subscriber** of that topic — it is **not** a private ERROR frame. Mapping: [[What is the MessageMapping annotation]]. Annotation details: [[What is MessageExceptionHandler for STOMP]]. User dest: [[What is the SendToUser annotation]].

```java
@Controller
public class MyController {

	@MessageMapping("/action")
	public void handleAction() throws Exception {
		throw new MyBusinessException();
	}

	@MessageExceptionHandler
	@SendToUser(destinations = "/queue/errors", broadcast = false)
	public ApplicationError handleException(MyBusinessException exception) {
		return appError;
	}
}
```

**Listing 1.** Conceptual: Framework 6.2 user-destination sample. Client subscribes to `/user/queue/errors`.

Default **without** a `StompSubProtocolErrorHandler`: ERROR frame with a **message** header describing the error. Customize in **`registerStompEndpoints`**: `registry.setErrorHandler(handler)` (4.2). Handler may return **`null`** to **suppress** ERROR (and the forced close) and instead notify via a **user destination**. Relay/broker failures use `handleErrorMessageToClient`. STOMP 1.2: ERROR SHOULD include `message`; then the server **MUST** close.

```d2
direction: down
ex: "@MessageMapping throws" {
  width: 240
  height: 40
  style.fill: "#e3f2fd"
}
meh: "@MessageExceptionHandler" {
  width: 260
  height: 40
  style.fill: "#fff3e0"
}
msg: "MESSAGE to /user/queue/errors" {
  width: 280
  height: 40
  style.fill: "#e8f5e9"
}
err: "STOMP ERROR then close" {
  width: 240
  height: 40
  style.fill: "#fce4ec"
}

ex -> meh: "handled"
meh -> msg
ex -> err: "unhandled / protocol"
```

**Fig. 1.** A handled business exception stays a messaging return. An ERROR frame ends the socket.

> [!warning]Topic errors are public
> `@SendTo("/topic/errors")` is a **broadcast**. It does not send a STOMP ERROR frame to the offender only, and it does not keep the failure off other clients. HTTP `@ExceptionHandler` does not run for STOMP SEND.

> [!tip] Interview answer
> **Handle `@MessageMapping` failures with `@MessageExceptionHandler` and `@SendToUser(..., broadcast=false)` so the caller gets a MESSAGE on `/user/queue/errors`.** Protocol ERROR frames close the connection; customize or suppress them with `StompEndpointRegistry.setErrorHandler`. `@ControllerAdvice` makes the handler global. `@SendTo("/topic/errors")` is not private.
