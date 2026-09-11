<!--
reps: 0
priority: 0
-->
#Messaging/Tools/RabbitMQ #SRS

# Does RabbitMQ support message priority

> [!abstract] Short answer
> Yes, on two levels. Classic queues support classic priorities bounded by `x-max-priority` (1–10 recommended) set at declaration; quorum queues gained strict priorities 0–31 in RabbitMQ 4.3, always enabled, with no x-max-priority argument. Publishers set the priority message property; higher dispatches first.

## How priorities dispatch

The standard FIFO behaviour changes: the queue dispatches the highest-priority ready messages first, FIFO within the same priority. On classic queues, priorities above the declared `x-max-priority` are clamped, the argument is immutable after declaration, and the queue allocates resources per level, which is why the docs recommend 1–10 levels. On quorum queues before 4.3 priorities mapped onto two internal buckets with a 2:1 dispatch ratio; 4.3 made them strict over 32 levels, clamped, with priority 4 as the default for messages that set nothing (classic defaults to 0).

```d2
direction: down
ready: "ready messages\nA(1), B(3), C(2)" {
  width: 220
  height: 90
  style.fill: "#e3f2fd"
}
order: "dispatch order\nB(3), C(2), A(1)" {
  width: 220
  height: 90
  style.fill: "#e8f5e9"
}
head: "head-of-line waiting\nA waits for B and C" {
  width: 250
  height: 80
  style.fill: "#ffebee"
}
ready -> order
order -> head
```

**Fig. 1.** Priority reorders dispatch and therefore delays low-priority messages — head-of-line blocking moves to the low end.

## When not to use them

Priorities are opt-in and complicate reasoning: competing consumers, requeues, and prefetch all interact with dispatch order, and the docs explicitly ask teams to consider separate queues per priority class instead — the single giant queue with priorities is a known anti-pattern. Legitimate uses are genuinely urgent work jumping a bulk backlog, not queue-level QoS policy. The dispatch-order context is in [[How do competing consumers work in RabbitMQ]], and the type-specific limits in [[What RabbitMQ queue types exist]].

```java
Map<String, Object> args = Map.of("x-max-priority", 5);
ch.queueDeclare("jobs", true, false, false, args);
AMQP.BasicProperties p = new AMQP.BasicProperties.Builder()
        .priority(4).build();
ch.basicPublish("", "jobs", p, body);
```

**Listing 1.** Declare the ceiling once; publishers then pick any value up to that ceiling.

> [!warning] Priorities do not exist on streams
> Streams have no message-priority feature at all, and answers claiming quorum queues "never support priorities" are outdated since 4.3. Mixing the two facts — streams lack it, quorum has it now — is exactly the precision interviewers probe.

> [!tip] Interview answer
> Yes: classic queues via x-max-priority plus the priority property, 1–10 recommended levels, immutable after declare; quorum queues since 4.3 with strict 0–31 priorities enabled by default. Dispatch is highest-first, FIFO within a level, and the docs prefer separate queues over deep priority ladders.
