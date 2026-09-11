<!--
reps: 0
priority: 0
-->
#Messaging #Patterns/Enterprise/Integration #SRS

# What is the Polling Consumer pattern?

> [!abstract] Short answer
> A **Polling Consumer** consumes **when the application decides**: it makes an explicit receive call, processes the result, and polls again — the synchronous style of consumption, with the application in control of timing and pacing.

## The application asks, the channel answers

Also called a synchronous receiver: the receiving thread blocks until a message arrives (or times out). Messaging APIs support the spectrum — a blocking `receive()`, `receive(ms)` with timeout, and `receiveNoWait()` that returns immediately when nothing is available; the difference only matters when the consumer polls faster than messages arrive. The pattern's strengths are control and simplicity: consume at a chosen rate, batch, prioritize work between polls, easy threading model, trivially testable. Its costs are latency (the message waits for the next poll) and waste (empty polls burn broker calls), which is why production polling usually uses long timeouts or adaptive intervals, and why push-style consumption exists as the alternative — the [[What is the Event-Driven Consumer pattern]]. Kafka's consumer is poll-based by design — its `poll()` loop returns batches and manages offsets, see [[How does Kafka handle a slow consumer]] for the backpressure story; JMS `MessageConsumer.receive` is the classic implementation. Pair with [[What is the Selective Consumer pattern]] when only a subset of messages is wanted.

```d2
direction: down
app: "Application\nown scheduling" {
  width: 210
  height: 60
  style.fill: "#e8f5e9"
}
p1: "receive(1000)" {
  width: 160
  height: 45
  style.fill: "#fff3e0"
}
p2: "process message" {
  width: 170
  height: 45
  style.fill: "#fff3e0"
}
p3: "receive() again..." {
  width: 180
  height: 45
  style.fill: "#fff3e0"
}
ch: "Channel" {
  width: 130
  height: 45
  style.fill: "#e3f2fd"
}
app -> p1 -> p2 -> p3
p3 -> p1: "loop"
p1 -> ch: "ask"```

**Fig. 1.** Consumption happens on the application's clock, not the broker's.

## The three receive variants

```java
Message m1 = consumer.receive();          // blocks until one arrives
Message m2 = consumer.receive(1000);      // waits up to 1s, then null
Message m3 = consumer.receiveNoWait();    // returns now (often null)
```

**Listing 1.** Same consumer object, three pacing knobs: blocking, bounded, and non-blocking — the entire control surface of the pattern.

> [!warning] Polling is not free and not prompt
> Tight empty polls waste broker resources (each call is work), while long sleeps add latency to every message; the failure mode is tuning polling to the average and falling over on the peak. And a blocking receive pins a thread per consumer — hundreds of pollers mean hundreds of parked threads that the platform must schedule around.

> [!tip] Interview answer
> A Polling Consumer pulls messages explicitly — the application calls receive, processes, and calls again, deciding its own pace. It is simple, testable, and backpressures naturally, at the cost of latency and empty-poll overhead; APIs offer blocking, timeout, and no-wait variants. Kafka consumers are poll-based for exactly this control, while JMS push listeners are the opposite style.
