<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebSocket #Java/Annotations #SRS

# What is the `@SendTo` annotation?

> [!abstract] Short answer
> **`@SendTo`** (Framework 4.0, `org.springframework.messaging.handler.annotation`) sets the **broker destination(s)** for a message-handling method’s **return value**. `@MessageMapping("/hello")` + `@SendTo("/topic/greetings")` publishes to **every subscriber** of `/topic/greetings`. It is a convenience over **`SimpMessagingTemplate.convertAndSend`**. Without `@SendTo`, the default is still a **broadcast**: inbound `/app/…` rewritten as **`/topic/…`**.

## Broadcast destination, not a private reply

Allowed on **method and class**; class-level is the default; **method-level wins**. You may list **several** destinations. You may combine with **`@SendToUser`** on the same method (two outgoing messages). Does **not** make a `/topic` payload private because the JSON contains a user id. Private replies: [[What is the SendToUser annotation]]. Mapping: [[What is the MessageMapping annotation]]. Template: [[What is SimpMessagingTemplate]]. Prefixes: [[What is the difference between the app prefix and topic prefix]]. `@SubscribeMapping` plus `@SendTo` **overrides** the direct-to-client default and sends through the broker ([[What is SubscribeMapping]]).

```java
@Controller
public class GreetingController {

	@MessageMapping("/hello")
	@SendTo("/topic/greetings")
	public Greeting greet(HelloMessage hello) {
		return new Greeting("Hello, " + hello.getName());
	}
}
```

**Listing 1.** Conceptual: every client subscribed to `/topic/greetings` gets the `Greeting`. You can return `void` and call `SimpMessagingTemplate` instead.

The `@SendTo` javadoc notes that if the **incoming** message already names a reply destination, that can take precedence in a generic request/reply setup. STOMP-over-WebSocket apps normally set `@SendTo` explicitly or accept the `/topic` default.

```d2
direction: down
ret: "method return value" {
  width: 220
  height: 40
  style.fill: "#e3f2fd"
}
st: "@SendTo /topic/greetings" {
  width: 260
  height: 40
  style.fill: "#fff3e0"
}
all: "all subscribers" {
  width: 200
  height: 40
  style.fill: "#e8f5e9"
}

ret -> st
st -> all
```

**Fig. 1.** `@SendTo` is broker fan-out. `@SendToUser` prepends `/user/{username}`.

> [!warning]Topic is public
> `@SendTo("/topic/messages")` on a “private chat” handler delivers to **every** subscriber of that topic. Putting a user id in the payload does not restrict delivery. Default without `@SendTo` is **also** a `/topic` broadcast, not “no send.”

> [!tip] Interview answer
> **`@SendTo` publishes the return value to one or more broker destinations — usually `/topic/...` for everyone subscribed.** Skip it and Spring still broadcasts on `/topic` plus the rest of the inbound path. For one user, `@SendToUser` or `convertAndSendToUser`. The annotation is sugar over `SimpMessagingTemplate`.
