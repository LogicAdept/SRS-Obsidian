<!--
reps: 0
priority: 0
-->
#Messaging #Patterns/Enterprise/Integration #SRS

# What is the Messaging Bridge pattern?

> [!abstract] Short answer
> A **Messaging Bridge** connects **two messaging systems** and replicates messages between corresponding channels, so messages available in one system become available in the others. Internally it is a pair of channel adapters whose "application" side is the other messaging system.

## Bridging channels, not merging brokers

There is usually no practical way to fuse two complete messaging systems, so the bridge connects individual corresponding channels: for each channel pair, one endpoint consumes from system A and republishes to system B, and the bridge also transforms the message format of one system into that of the other. The bridge acts as a map from one channel set to the other. This shows up in practice as Kafka MirrorMaker between two Kafka clusters, a JMS bridge between two broker vendors, or a connector shipping a RabbitMQ queue into Kafka for analytics. Related building blocks: the replication leg reuses the [[What is the Channel Adapter pattern]], and the format hop is a [[What is the Message Translator pattern]] job; both sit on plain [[What is the Message Channel pattern]]s.

```d2
direction: right
qa: "orders.work\nin system A" {
  width: 190
  height: 65
  style.fill: "#e3f2fd"
}
br: "Bridge\nconsume + translate\n+ republish" {
  width: 210
  height: 80
  style.fill: "#fff3e0"
}
qb: "orders.work\nin system B" {
  width: 190
  height: 65
  style.fill: "#e8f5e9"
}
qa -> br -> qb
br -> qa: "reverse pair\n(bidirectional bridge)" {
  style.stroke-dash: 4
}```

**Fig. 1.** Each bridged channel pair is independent; a bidirectional bridge is just a second pair running the other way.

## What the bridge must preserve

```text
Concern            Handled by the bridge how?
-----------------  --------------------------------------------
Message format     translate A's envelope into B's headers/props
Ordering           per-channel, if it consumes and republishes in order
Delivery           confirm B accepted before acking A (at-least-once)
Loops              drop messages that came from B (mark origin header)
```

**Listing 1.** Ack-then-forward ordering is the safety rule: never acknowledge the source before the copy is durably accepted at the target, or the bridge becomes a message shredder during outages.

> [!warning] Bidirectional bridges can create message loops
> If A forwards to B and B forwards back to A, a message without an origin marker will ping-pong forever, multiplying copies. Bridges must stamp origin and skip already-bridged messages — and during an outage, a bridge without the "confirm before ack" rule can duplicate or drop whole batches.

> [!tip] Interview answer
> A Messaging Bridge connects two messaging systems by replicating messages between corresponding channels — effectively paired channel adapters where the non-messaging side is the other broker, plus format translation. Kafka MirrorMaker or a JMS-to-Kafka connector are typical instances. The classic pitfalls are message loops in bidirectional setups and acknowledging the source before the target has durably stored the copy.
