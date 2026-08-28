<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebSocket #Messaging #SRS

# What is the difference between the app prefix and topic prefix?

> [!abstract] Short answer
> **`setApplicationDestinationPrefixes("/app")`** marks STOMP destinations that go to **annotated controllers**. Spring **strips** the matching prefix; `@MessageMapping("/greeting")` matches a client SEND to **`/app/greeting`**, not `/app/greeting` on the annotation. **`enableSimpleBroker("/topic", "/queue")`** (or relay prefixes) marks destinations the **broker** owns: `SUBSCRIBE /topic/…`, broadcasts, **`@SendTo("/topic/…")`**. They are **not** the WebSocket handshake path.

## Two filters on `destination`

Inbound STOMP frames become Spring `Message`s on **`clientInboundChannel`**. Prefix `/app` → `@MessageMapping` / `@SubscribeMapping`. Prefix `/topic` or `/queue` → simple broker or relay. A `@MessageMapping` return value, if you omit `@SendTo`, is sent to the broker with **`/app` replaced by `/topic`** (so `/app/greeting` in → `/topic/greeting` out). HTTP `@PostMapping` can also send on **`brokerChannel`** via `SimpMessagingTemplate`. Config: [[How do you configure a STOMP broker in Spring]]. Mapping: [[What is the MessageMapping annotation]]. Broadcast: [[What is the SendTo annotation]]. Broker types: [[What is a simple broker versus a STOMP broker relay]]. STOMP: [[What is STOMP in Spring WebSocket]].

On the **simple broker**, `/topic` vs `/queue` has **no special implementation meaning** — convention for many subscribers vs one consumer. An **external** broker defines its own destination syntax; check that product’s STOMP page. Prefixes without a trailing slash get a slash appended. User destinations use **`/user/`** (separate prefix).

```java
registry.setApplicationDestinationPrefixes("/app");
registry.enableSimpleBroker("/topic", "/queue");

@Controller
public class GreetingController {
	@MessageMapping("/greeting")
	@SendTo("/topic/greeting")
	public String handle(String greeting) {
		return greeting;
	}
}
```

**Listing 1.** Conceptual: client SEND `/app/greeting`, SUBSCRIBE `/topic/greeting`. Subscribing to `/app/greeting` does **not** receive `@SendTo("/topic/greeting")` traffic.

```d2
direction: down
send: "SEND /app/greeting" {
  width: 240
  height: 40
  style.fill: "#e3f2fd"
}
ctrl: "@MessageMapping /greeting" {
  width: 240
  height: 40
  style.fill: "#fff3e0"
}
topic: "broker /topic/greeting" {
  width: 240
  height: 40
  style.fill: "#e8f5e9"
}

send -> ctrl
ctrl -> topic
```

**Fig. 1.** Handshake URL `/portfolio` never appears in these destination strings.

> [!warning]Subscribe to `/app` and you miss broadcasts
> Application prefix traffic is for **controllers**, not the subscription registry. `@SendTo` / simple-broker publish goes to **broker** prefixes. Putting `/app` on `@MessageMapping` as well as `setApplicationDestinationPrefixes` double-strips and misses the method.

> [!tip] Interview answer
> **`/app` is “call a `@MessageMapping`”; `/topic` or `/queue` is “broker subscriptions and fan-out.”** Spring removes `/app` before matching. Default return rewrites `/app` to `/topic`. Simple broker treats `/topic` vs `/queue` as names only; Rabbit/ActiveMQ do not.
