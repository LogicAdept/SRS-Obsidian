<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebSocket #Java/Annotations #SRS

# What is `@SubscribeMapping`?

> [!abstract] Short answer
> **`@SubscribeMapping`** (Framework 4.0, `org.springframework.messaging.simp.annotation`) is a **`@MessageMapping` specialization** that matches **STOMP SUBSCRIBE** only. Same method arguments as `@MessageMapping`. **Default return path is different:** the payload goes **straight to that client** on **`clientOutboundChannel`**, **not** through the broker as a broadcast. Add **`@SendTo`** or **`@SendToUser`** to send to the broker instead.

## One-shot reply, not a stored `/topic` subscription

Typical split: broker owns `/topic` and `/queue` (repeated broadcasts); controllers own `/app`. A client **SUBSCRIBE `/app/positions`** can receive initial UI data **once**, without the broker storing that subscription for later fan-out. Subscriptions usually have **no body**. Combine with **type-level `@MessageMapping`**. Do **not** map broker and controllers to the **same** destination prefix — inbound handling is parallel with **no order guarantee**. To know when a **broker** subscription is stored, use a STOMP **receipt** (simple broker does **not** support receipts) or an `ExecutorChannelInterceptor` on `brokerChannel`. Mapping: [[What is the MessageMapping annotation]]. Broker vs `/app`: [[What is the difference between the app prefix and topic prefix]]. Override outbound: [[What is the SendTo annotation]]. STOMP: [[What is STOMP in Spring WebSocket]].

```java
@Controller
public class PortfolioController {

	@SubscribeMapping("/positions")
	public Positions getPositions() {
		return loadPositions();
	}
}
```

**Listing 1.** Conceptual: client **SUBSCRIBE `/app/positions`** (after the application prefix). If you also `@SendTo("/topic/positions")`, the return is brokered and broadcast.

On controller **interfaces**, put `@SubscribeMapping` on the interface, not only the impl (AOP proxies).

```d2
direction: down
sub: "SUBSCRIBE /app/positions" {
  width: 260
  height: 40
  style.fill: "#e3f2fd"
}
m: "@SubscribeMapping" {
  width: 220
  height: 40
  style.fill: "#fff3e0"
}
direct: "clientOutboundChannel (this client)" {
  width: 280
  height: 40
  style.fill: "#e8f5e9"
}
broker: "brokerChannel if @SendTo" {
  width: 260
  height: 40
  style.fill: "#fce4ec"
}

sub -> m
m -> direct
m -> broker
```

**Fig. 1.** Default is request-reply to the subscriber. `/topic` subscriptions never need this annotation.

> [!warning]Same prefix as the broker races
> If both the simple broker and a `@SubscribeMapping` method claim `/topic/...`, either may run first. For initial data, subscribe to an **`/app`** destination. `@SubscribeMapping` on a SEND frame does not match.

> [!tip] Interview answer
> **`@SubscribeMapping` handles SUBSCRIBE, not SEND.** The return goes back to that client unless you add `@SendTo`. Use it for one-time snapshot data on `/app`. Repeated broadcasts stay on `/topic` with the broker. Simple broker has no STOMP receipts.
