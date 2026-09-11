<!--
reps: 0
priority: 0
-->
#Messaging/Tools/RabbitMQ #SRS

# How do you make a RabbitMQ message survive a broker restart

> [!abstract] Short answer
> Stack four things: a durable queue, persistent delivery mode on the message, publisher confirms (so you know the broker actually took responsibility), and manual consumer acks. For node-loss survival, use a quorum queue so a restart or crash of one node does not remove the data at all.

## The survival checklist

Durability of the queue definition comes from the `durable` declare flag; content survival needs `delivery_mode=2`. Publisher confirms close the asynchronous gap — without them, a crash between accepting the socket write and persisting loses the message silently, and the publisher never knows. Manual acks close the consumer-side gap so unprocessed deliveries survive as ready messages. For replication, declare `x-queue-type: quorum`, where confirms wait for a Raft majority — the strongest combination. The durability/persistence split itself is in [[What is the difference between a durable queue and a persistent message in RabbitMQ]].

```d2
direction: down
dq: "durable queue" {
  width: 180
  height: 70
  style.fill: "#e3f2fd"
}
pm: "persistent publish" {
  width: 190
  height: 70
  style.fill: "#e3f2fd"
}
cf: "publisher confirm" {
  width: 180
  height: 70
  style.fill: "#fff3e0"
}
qq: "quorum type (optional, for node loss)" {
  width: 290
  height: 70
  style.fill: "#ffebee"
}
ma: "manual consumer acks" {
  width: 220
  height: 70
  style.fill: "#e8f5e9"
}
dq -> pm
pm -> cf
cf -> qq
qq -> ma
```

**Fig. 1.** Each layer removes one silent-loss window; skip any and a crash can eat the message invisibly.

```java
ch.confirmSelect();
Map<String, Object> args = Map.of("x-queue-type", "quorum");
ch.queueDeclare("orders", true, false, false, args);
ch.basicPublish("", "orders", MessageProperties.PERSISTENT_TEXT_PLAIN, body);
ch.waitForConfirmsOrDie(5_000);
```

**Listing 1.** The durable-plus-confirmed publish path; the consumer side uses manual acks with bounded prefetch.

## What still escapes

A confirmed classic-queue publish waits for the disk write batch — the broker itself treats that as responsibility transfer, so the remaining loss window is effectively broker-internal; the residual risks are unconfirmed publishes, auto-ack consumers, and single-node classic queues under node failure. En masse, the production-checklist answer is quorum queues plus confirms, and monitoring confirm latency. The guarantees taxonomy is in [[What delivery guarantees does RabbitMQ provide]].

> [!warning] Restart and node loss are different scenarios
> Durable plus persistent survives a broker *restart*. A node that dies permanently takes a classic queue's data with it regardless of flags — only quorum replication (or streams) covers node loss. Conflating the two scenarios in an interview answer hides the whole HA dimension.

> [!tip] Interview answer
> Durable queue declaration, delivery_mode 2 on the message, publisher confirms to know the broker took over, and manual acks on consume; quorum queues add Raft replication so node loss does not delete data. Anything less leaves a silent-loss window between socket write and disk.
