<!--
reps: 0
priority: 0
-->
#Messaging #Patterns/Enterprise/Integration/Endpoints #SRS

# What is the Competing Consumers pattern?

> [!abstract] Short answer
> **Competing Consumers** are multiple consumers on **one point-to-point channel**, each message delivered to **exactly one** of them — the consumers compete, the messaging system arbitrates. It is the standard scale-out idiom: add consumers to add throughput.

## Many workers, one channel, no duplicates per message

When arrivals outpace one consumer, the answer is N consumers on the same channel: the system's implementation decides which one gets each message, and in effect they compete — each message is processed once by any one of them. The constraint is hard: this works only on **point-to-point** channels; multiple consumers on a publish-subscribe channel just produce more copies, not parallelism — that is fan-out, not load balancing. Real deployments add tuning the EIP text does not spell out: Kafka's consumer groups are the flagship implementation (a group competes over partitions — see [[What happens when there are more Kafka partitions than consumers]]), RabbitMQ delivers to whichever worker's prefetch window has room ([[How does Kafka handle a slow consumer]] covers the Kafka pacing analogue). Consequences to design for: per-message ordering is lost across consumers, redelivery can duplicate work ([[What is the Idempotent Receiver pattern]] becomes mandatory), and skewed processing times need prefetch/assignment tuning. The supervised variant where a component assigns messages to workers instead is the [[What is the Message Dispatcher pattern]].

```d2
direction: down
p: "Producers" {
  width: 150
  height: 50
  style.fill: "#e3f2fd"
}
q: "Point-to-Point channel\neach message -> one consumer" {
  width: 300
  height: 70
  style.fill: "#fff3e0"
}
c1: "Consumer 1" {
  width: 140
  height: 50
  style.fill: "#e8f5e9"
}
c2: "Consumer 2" {
  width: 140
  height: 50
  style.fill: "#e8f5e9"
}
c3: "Consumer 3" {
  width: 140
  height: 50
  style.fill: "#e8f5e9"
}
p -> q
q -> c1: "msg 1"
q -> c2: "msg 2"
q -> c3: "msg 3"```

**Fig. 1.** Three workers, three different messages: throughput scales, but which consumer gets which message is nobody's contract.

## Two arbitration styles

```text
Style           Who picks the consumer        Tuning knob
--------------  ----------------------------  ------------------------
Kafka group     group leader assigns          partitions, session timeouts
RabbitMQ        broker: next available        prefetch (fair dispatch)
```

**Listing 1.** Same EIP, different arbitrators: partition assignment versus prefetch-based push — the ordering guarantees differ accordingly.

> [!warning] Competing consumers break ordering and guarantee redelivery
> With N consumers, two messages that must apply in order can run in parallel and invert; and any consumer death re-delivers its unacked messages to a survivor. If sequence matters, partition by key; if processing has side effects, make it idempotent first — scaling workers multiplies both problems.

> [!tip] Interview answer
> Competing Consumers is N consumers on one point-to-point channel where each message goes to exactly one of them, giving horizontal scale-out. Kafka consumer groups and RabbitMQ prefetch-based dispatch are the flagship implementations. The costs are real: cross-consumer ordering disappears, redelivery duplicates work, so idempotency and key-based partitioning carry the correctness load.
