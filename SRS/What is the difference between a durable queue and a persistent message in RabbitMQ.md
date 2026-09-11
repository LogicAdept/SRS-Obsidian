<!--
reps: 0
priority: 0
-->
#Messaging/Tools/RabbitMQ #SRS

# What is the difference between a durable queue and a persistent message in RabbitMQ

> [!abstract] Short answer
> Durability is a queue (and exchange) definition property: the metadata and structure survive a broker restart. Persistence is a per-message property (`delivery_mode=2`): the payload is written toward disk. Surviving a restart needs both — one alone guarantees nothing about your data.

## The matrix that decides survival

A durable queue with transient messages recovers empty — the broker discards transient messages during recovery, even from durable queues. Persistent messages in a non-durable queue vanish too: the queue itself is deleted on boot, taking its contents with it. Persistent messages on a durable queue recover — subject to the publish actually having been accepted, which is what publisher confirms establish, per [[What are publisher confirms in RabbitMQ]].

```d2
direction: down
cell1: "durable queue\npersistent msg\nsurvives" {
  width: 220
  height: 90
  style.fill: "#e8f5e9"
}
cell2: "durable queue\ntransient msg\ndiscarded" {
  width: 220
  height: 90
  style.fill: "#ffebee"
}
cell3: "transient queue\npersistent msg\ngone with queue" {
  width: 230
  height: 90
  style.fill: "#ffebee"
}
cell4: "transient queue\ntransient msg\ngone" {
  width: 210
  height: 90
  style.fill: "#ffebee"
}
```

**Fig. 1.** Only the durable-queue/persistent-message corner survives a restart — every other cell loses data.

## The publish-time mechanics

Persistence is set on the message properties: `delivery_mode=2` (Java `MessageProperties.PERSISTENT_TEXT_PLAIN`), transient being 1. Quorum queues and streams blur the line slightly — they are always durable and always store to their log, but the delivery-mode distinction still governs whether the message survives recovery. The consumer-side complement is manual acks; see [[How do you make a RabbitMQ message survive a broker restart]] for the full survival checklist.

```java
import com.rabbitmq.client.MessageProperties;
ch.basicPublish("", "orders",
        MessageProperties.PERSISTENT_TEXT_PLAIN, body);
```

**Listing 1.** `delivery_mode=2` marks the message persistent; it is a property of the publish, not the queue.

> [!warning] Persistent is not "written to disk at publish time"
> Classic queues batch writes; a confirmed publish is the guarantee, not the flag. And on a non-durable queue the flag is meaningless decoration. Saying "I set persistent so messages survive" without durable queues and confirms fails the follow-up question every time.

> [!tip] Interview answer
> Durable is topology: the queue's definition is reloaded after restart. Persistent is data: delivery_mode 2 on the message. Survival needs both plus confirmed publishes; transient messages in durable queues are discarded at recovery, and persistent messages die with a non-durable queue.
