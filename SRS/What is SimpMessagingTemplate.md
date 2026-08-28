<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebSocket #SRS

# What is `SimpMessagingTemplate`?

> [!abstract] Short answer
> **`SimpMessagingTemplate`** (Framework 4.0) is the bean that **sends** to the STOMP **`brokerChannel`** from **any** component — service, scheduler, HTTP `@RequestMapping`, or a `@MessageMapping` that needs more than a return value. **`convertAndSend("/topic/…", payload)`** broadcasts. **`convertAndSendToUser(user, "/queue/…", payload)`** targets user destinations. `@SendTo` / `@SendToUser` are sugar over this template. Default bean name: **`brokerMessagingTemplate`**.

## Fire-and-forget onto the broker channel

Inject **by type**. Qualify with `@Qualifier("brokerMessagingTemplate")` if another `SimpMessagingTemplate` exists. Constructor takes the `MessageChannel`. User prefix defaults to **`/user/`**. `convertAndSendToUser` uses **`UserDestinationResolver`**. Unauthenticated: pass **session id** as user **and** set **`sessionId`** in headers. User send: [[How do you send a message to one user with Spring WebSocket]]. Annotations: [[What is the SendTo annotation]], [[What is the SendToUser annotation]]. Mapping: [[What is the MessageMapping annotation]]. Who is online: [[What is SimpUserRegistry]]. STOMP: [[What is STOMP in Spring WebSocket]].

```java
@Controller
public class GreetingController {

	private final SimpMessagingTemplate template;

	public GreetingController(SimpMessagingTemplate template) {
		this.template = template;
	}

	@RequestMapping(path = "/greetings", method = RequestMethod.POST)
	public void greet(String greeting) {
		this.template.convertAndSend("/topic/greetings", greeting);
	}
}
```

**Listing 1.** Conceptual: HTTP POST publishes to WebSocket subscribers — no client SEND required. Subscribe to `BrokerAvailabilityEvent` when using a **relay**; handle **`MessageDeliveryException`**. Simple broker is available for the process lifetime.

`send(Message)` uses an existing destination header, or the configured default destination, or throws **`IllegalStateException`**.

```d2
direction: down
any: "HTTP / service / @MessageMapping" {
  width: 280
  height: 40
  style.fill: "#e3f2fd"
}
tmpl: "SimpMessagingTemplate" {
  width: 240
  height: 40
  style.fill: "#fff3e0"
}
ch: "brokerChannel" {
  width: 200
  height: 40
  style.fill: "#e8f5e9"
}

any -> tmpl
tmpl -> ch
```

**Fig. 1.** The template does not open a new WebSocket. It publishes on the in-app broker channel.

> [!warning]Topic convertAndSend is public
> User targeting is **`convertAndSendToUser`**, and the client must subscribe under **`/user/…`**. Sending to `/topic` because the payload has a user id is still a broadcast. If the relay is down, sending can fail — listen for broker availability.

> [!tip] Interview answer
> **`SimpMessagingTemplate` is how any Spring bean publishes STOMP messages: `convertAndSend` for topics, `convertAndSendToUser` for one user.** `@SendTo` is the annotation form. Inject `brokerMessagingTemplate` by type. It is not `TextWebSocketHandler.sendMessage`.
