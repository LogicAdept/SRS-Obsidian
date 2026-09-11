<!--
reps: 0
priority: 0
-->
#Patterns/Enterprise/Integration/Channels/InvalidMessageChannel #SRS

# What happens if a receiver puts an invalid message back on the original channel

> [!abstract] Short answer
> It will be delivered again — to the same receiver or one just like it — which rebuilds the same failure forever. Ignoring the message clutters the channel and hurts throughput; consuming and silently discarding it hides a problem someone needs to see. The pattern's answer is to move it off the channel and park it where it is visible.

## Why requeue and drop are both wrong

The book's channel chapter states the two forbidden behaviors directly: the receiver must not leave improper messages on the working channel, and it must not make them disappear by consuming and discarding them. Requeueing recreates the failure deterministically — a structurally invalid payload fails the same check on every redelivery, which is the poison-loop mechanics covered in [[Why should you not retry a structurally invalid message]]. The outcome only differs by how the broker eventually caps the loop: RabbitMQ redelivers with the redelivered flag set and a quorum queue applies its delivery-limit before dead-lettering ([[What is a poison message in RabbitMQ]]), Jakarta Messaging increments `JMSXDeliveryCount` and the provider eventually gives up in a provider-dependent way, and Azure Service Bus increments the delivery count on every abandon until `MaxDeliveryCount` dead-letters the message. All of those caps are Dead Letter Channel machinery catching what the receiver should have decided itself — the pattern split is in [[What is the difference between Invalid Message Channel and Dead Letter Channel]].

```d2
direction: down
bad: "Invalid message\ndelivered again" {
  width: 250
  height: 70
  style.fill: "#ffebee"
}
rq: "Requeue / abandon" {
  width: 220
  height: 60
  style.fill: "#fff3e0"
}
loop: "Same receiver,\nsame failure, forever" {
  width: 260
  height: 70
  style.fill: "#ffebee"
}
cap: "Broker cap reached\n(DLC machinery)" {
  width: 260
  height: 70
  style.fill: "#fff3e0"
}
park: "Move to Invalid Message Channel\nonce, on first detection" {
  width: 310
  height: 75
  style.fill: "#e8f5e9"
}
bad -> rq
rq -> loop: "uncapped"
loop -> cap
bad -> park: "pattern behavior"
```

**Fig. 1.** Requeueing delegates the decision to a broker counter; parking makes the receiver own it immediately.

> [!warning] Drop hides evidence, requeue hides intent
> Silently discarding looks cheaper, but it erases the payload that would have told you the sender's contract changed. Even a fully automated invalid-flow still keeps the message — that is the difference between a quarantine and a shredder.

> [!tip] Interview answer
> Requeueing hands the message straight back to a receiver with the same expectations, so the failure repeats until some broker delivery cap finally dead-letters it; dropping hides the problem entirely. The receiver should take the message off the working channel once, park it on the invalid channel intact, and let the error handler decide — that keeps the happy path clean and the evidence alive.
