<!--
reps: 0
priority: 0
-->
#Messaging #Patterns/Enterprise/Integration/Messaging #SRS

# What is the Resequencer pattern?

> [!abstract] Short answer
> A **Resequencer** is a **stateful filter** that buffers out-of-order messages and republishes them **in the required order**, so downstream steps that need in-sequence delivery get it even when routes, retries, or concurrency scrambled the stream.

## Restore order without changing content

Messages take different routes through a mesh of routers; some arrive early, some crawl, redeliveries shuffle further. Steps that need sequence — referential updates, ordered document processing — cannot tolerate the shuffle. The resequencer holds arrivals in an internal buffer until it can release a continuous run in the specified order, and it must publish onto an **order-preserving output channel**, otherwise the effort is undone at the next hop. Like most routers it does not modify message contents; the order information comes from headers (sequence position — the fields of a [[What is the Message Sequence pattern]]). Two operational variants exist: stream reordering with gaps tolerated only briefly, and batch reordering that waits for the full set. Where the out-of-order-ness is *per-partition parallelism* rather than routing scatter, Kafka offers per-partition ordering and in-key sequencing — see [[What ordering guarantees does Kafka provide for messages]]; the buffer's memory profile and its interplay with a [[What is the Splitter pattern]]'s totals are the practical design space.

```d2
direction: down
in: "Arrivals\n2, 1, 4, 3" {
  width: 170
  height: 60
  style.fill: "#e3f2fd"
}
rs: "Resequencer\nbuffer + release in order" {
  width: 250
  height: 75
  style.fill: "#fff3e0"
}
out: "Order-preserving channel\n1, 2, 3, 4" {
  width: 250
  height: 70
  style.fill: "#e8f5e9"
}
d: "Downstream\nin-sequence processing" {
  width: 220
  height: 60
  style.fill: "#e3f2fd"
}
in -> rs -> out -> d```

**Fig. 1.** The buffer absorbs arrival jitter; the output channel must preserve what the buffer restored.

## Ordering fields drive the buffer

```java
from("audit.chaos")
    .resequence(header("seq-pos")).stream()   // release on continuous runs
        .capacity(1000)                        // buffer bound
        .timeout(5000)                         // gap policy
    .to("audit.ordered");
```

**Listing 1.** A stream resequencer over a position header: bounded buffer, explicit gap timeout — the two knobs that decide latency versus completeness.

> [!warning] A missing sequence number stalls the release
> If position 3 died in a dead letter queue, a strict resequencer holds 4, 5, 6... forever — head-of-line blocking by design. Every resequencer needs a gap policy (timeout-and-skip, alert-and-park) and a buffer bound, or one lost message turns into a full stream outage.

> [!tip] Interview answer
> A Resequencer buffers related messages that arrive out of order and republishes them in the required sequence — typically by a position header — without modifying content. It is a stateful filter: bounded buffer, gap policy, and an order-preserving output channel are mandatory, because a single missing number otherwise head-of-line blocks the whole stream.
