<!--
reps: 0
priority: 0
-->
#Messaging #Patterns/Enterprise/Integration/Endpoints #SRS

# What is the Message Dispatcher pattern?

> [!abstract] Short answer
> A **Message Dispatcher** is a component that **consumes from a channel and hands each message to a performer** — a worker object it creates or selects from a pool — so multiple workers process messages concurrently while the dispatcher owns the channel.

## The application controls the arbitration

Where competing consumers let the messaging system arbitrate between independent clients, the dispatcher moves arbitration **inside the application**: one endpoint consumes, then assigns each message to a performer — newly created, or taken from a pool — which processes it, possibly in its own thread. The dispatcher can be smart about assignment: all performers may handle all messages, or it can match messages to specialized performers based on message properties (type, priority, required capability). This is the in-process parallelism pattern: the channel still sees one consumer, so broker-side load balancing and redelivery semantics stay simple, while concurrency, pools, and specialist routing become ordinary code. The price is that the dispatcher is a component you now own and monitor — its pool sizing and queueing are your problem. Compare the alternatives: letting the broker do the arbitration is the [[What is the Competing Consumers pattern]]; registering callbacks directly is the [[What is the Event-Driven Consumer pattern]]; a stateful router across channels is the [[What is the Message Router pattern]].

```d2
direction: down
ch: "Channel\nsingle consumer" {
  width: 220
  height: 65
  style.fill: "#e3f2fd"
}
d: "Message Dispatcher\nassign per message" {
  width: 230
  height: 70
  style.fill: "#fff3e0"
}
w1: "Performer 1" {
  width: 140
  height: 50
  style.fill: "#e8f5e9"
}
w2: "Performer 2" {
  width: 140
  height: 50
  style.fill: "#e8f5e9"
}
w3: "Performer 3\n(specialist)" {
  width: 160
  height: 55
  style.fill: "#e8f5e9"
}
ch -> d
d -> w1
d -> w2
d -> w3: "matches type"```

**Fig. 1.** One consumer on the channel; parallelism, pooling, and specialist matching live behind the dispatcher.

## Dispatcher responsibilities in one view

```text
Responsibility        Design knob
--------------------  ----------------------------------------
Consume               channel + consumer style underneath
Assign                round-robin / least-busy / by message type
Pool                  fixed size, elastic, per-specialist pools
Concurrency           thread per performer vs executor
Backpressure          bounded hand-off queue, block or spillover
```

**Listing 1.** Every row is application code the dispatcher owner maintains — which is the pattern's cost and its flexibility.

> [!warning] The dispatcher is a self-inflicted single point
> It holds the channel: if its pool deadlocks or its hand-off queue overflows, consumption stops for everything behind it — a broker outage you wrote yourself. Bound the hand-off explicitly, monitor queue depth and assignment latency, and prefer broker-side competing consumers when dispatching adds no real value.

> [!tip] Interview answer
> A Message Dispatcher consumes from a channel and distributes messages to performer objects — created on demand or pooled, possibly matched to specialists by message properties — giving in-process parallelism while the channel sees a single consumer. The broker-side alternative is competing consumers. The dispatcher's trade: full control over assignment and pooling, plus full responsibility for its queues and pool health.
