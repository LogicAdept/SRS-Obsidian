<!--
reps: 0
priority: 0
-->
#Patterns/Enterprise/Integration/Channels/InvalidMessageChannel #Java/Spring/Integration #SRS

# How does a Spring Integration filter discard-channel implement Invalid Message Channel?

> [!abstract] Short answer
> A Spring Integration **filter** is a **yes/no** gate (`MessageSelector.accept`). Messages that return **false** are **dropped** (warning log since 6.1) unless you set **`discard-channel`**. That channel receives the **same `Message`**, not an `ErrorMessage`. That is the EIP **Invalid Message Channel**: the receiver parks an **improper payload** for operators. It is **not** `errorChannel` and **not** silent `NullChannel` drop.

## Reject vs route vs throw

Filter does not choose among many outputs like a router; it only decides **whether** to send to `output-channel`. `discard-channel` turns a reject into a **second destination** — a tiny boolean router ([[What is the Invalid Message Channel pattern]], [[What is the difference between Invalid Message Channel and an error channel]]).

`throwExceptionOnRejection` defaults **false**. If **true**, the filter still **sends to discard-channel first** (when configured), then throws **`MessageRejectedException`**. That is for **failover** among several selective consumers on one point-to-point channel (the dispatcher must see a failure). It is **not** a quiet quarantine.

No discard channel and `throwExceptionOnRejection=false`: drop + **WARN**. Explicit **`NullChannel`** as discard channel: drop **without** that warning.

```xml
<int:filter input-channel="orders.raw" ref="positiveAmount"
            output-channel="orders.validated"
            discard-channel="orders.rejected"/>
```

**Listing 1.** Official shape. Rejected messages are the **original** `Message` on `orders.rejected`.

```java
@Bean
public IntegrationFlow orders() {
	return IntegrationFlow.from("orders.raw")
			.filter(OrderCommand.class, o -> o.amount().signum() > 0,
					e -> e.discardChannel("orders.rejected"))
			.channel("orders.validated")
			.get();
}
```

**Listing 2.** Conceptual. DSL `FilterEndpointSpec.discardChannel`; same `Message` on the discard flow.

```d2
direction: down
in: "orders.raw" {
  width: 140
  height: 40
  style.fill: "#fff3e0"
}
f: "MessageFilter\nselector" {
  width: 180
  height: 50
  style.fill: "#e3f2fd"
}
ok: "orders.validated" {
  width: 180
  height: 40
  style.fill: "#e8f5e9"
}
bad: "orders.rejected\n(original Message)" {
  width: 220
  height: 50
  style.fill: "#fce4ec"
}
in -> f
f -> ok: "accept"
f -> bad: "discard-channel"
```

**Fig. 1.** Invalid Message Channel is the **payload as received**, parked — not an exception wrapper.

> [!warning] Discard then throw is not a quiet IMC
> `throwExceptionOnRejection=true` **plus** discard-channel still **throws** after the send. Downstream error handling / the caller may treat it as a failure even though the message already landed on the reject channel.

> [!warning] No discard-channel is not a quarantine
> Default reject is **drop** (plus a 6.1+ warning). Operational “we must see bad orders” requires an explicit **discard-channel** (or `discardFlow`), not hoping logs are enough.

> [!tip] Interview answer
> Filter `discard-channel` is how SI implements Invalid Message Channel: rejected messages go to a side channel as the original `Message`. Leave `throwExceptionOnRejection` false for a quiet park. `errorChannel` is a different contract — exception payload, async only.
