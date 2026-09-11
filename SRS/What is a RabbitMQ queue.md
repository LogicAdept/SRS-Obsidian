<!--
reps: 0
priority: 0
-->
#Messaging/Tools/RabbitMQ #SRS

# What is a RabbitMQ queue

> [!abstract] Short answer
> A queue is a named, FIFO buffer that receives copies of routed messages and delivers each copy to at most one consumer at a time. Messages stay there in the ready state, then become unacked after delivery, and are deleted on ack. Queue types are classic (non-replicated), quorum (Raft-replicated), and stream (append-only log).

## States and delivery

The queue orders messages by enqueue time and pushes deliveries to subscribed consumers in that order; polling via `basic.get` reads the same head. Each message sits in exactly one of two states — ready or unacked — and the management UI breaks queue length down this way. Multiple consumers on one queue get round-robin deliveries, each message to a single consumer; this is the work-queue mode described in [[How do competing consumers work in RabbitMQ]].

```d2
direction: down
enqueue: "publish routed here" {
  width: 230
  height: 70
  style.fill: "#e3f2fd"
}
ready: "ready\nin FIFO order" {
  width: 200
  height: 80
  style.fill: "#fff3e0"
}
unacked: "unacked\ndelivered, awaiting ack" {
  width: 250
  height: 80
  style.fill: "#ffebee"
}
acked: "deleted" {
  width: 170
  height: 60
  style.fill: "#e8f5e9"
}
enqueue -> ready
ready -> unacked: "basic.deliver"
unacked -> ready: "nack/requeue\nor channel close"
unacked -> acked: "basic.ack"
```

**Fig. 1.** A message cycles between ready and unacked; only an ack removes it, a requeue returns it to the ready side.

## Types and lifetime

The type is chosen at declaration via `x-queue-type`: classic, quorum, or stream — see [[What RabbitMQ queue types exist]]. Durable survives restarts of the definition and persistent contents; transient queues are deleted on boot. Exclusive queues die with their declaring connection. Length limits, TTL, and overflow behaviour are optional x-arguments or policies — see [[What is message TTL and queue max-length in RabbitMQ]].

```java
Map<String, Object> args = Map.of("x-queue-type", "quorum");
ch.queueDeclare("orders",       // name
                true,           // durable
                false,          // exclusive
                false,          // auto-delete
                args);
```

**Listing 1.** Declaring a durable quorum queue; the same call declares a classic queue when the type argument is absent.

> [!warning] Queue length counts ready messages only
> `message_count` from `queue.declare-ok` and the UI's ready count exclude unacked deliveries, so a "queue is almost empty" claim can hide thousands of unacked messages stuck with slow or dead consumers. Check both states before judging backlog.

> [!tip] Interview answer
> A RabbitMQ queue is a durable-or-not FIFO buffer with two message states, ready and unacked, that deletes on ack and redelivers on requeue. Competing consumers share it round-robin, types select between classic, quorum, and stream, and TTL, max length, and DLX bindings tune its lifetime and failure path.
