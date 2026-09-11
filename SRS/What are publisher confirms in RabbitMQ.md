<!--
reps: 0
priority: 0
-->
#Messaging/Tools/RabbitMQ #SRS

# What are publisher confirms in RabbitMQ

> [!abstract] Short answer
> Publisher confirms are the broker's acknowledgement of publishes: after `confirm.select`, the channel counts messages and the broker returns `basic.ack` (or `basic.nack` on internal failure) once it has accepted responsibility — persisted for persistent messages on durable queues, majority-accepted for quorum queues. Without confirms, publishing is fire-and-forget.

## Mechanism

`confirm.select` puts the channel in confirm mode (mutually exclusive with AMQP transactions). Both sides count from 1; the broker's ack carries the sequence number of the handled message, with `multiple=true` batch-confirming everything up to it. For unroutable messages the confirm follows the `basic.return` when the publish was also mandatory. Confirms can arrive out of publish order because they depend on per-queue persistence timing — applications should not order on them. They are much faster than AMQP transactions, which the docs note cost about 250x throughput.

```d2
direction: down
pub: "basic.publish (confirmed channel)" {
  width: 260
  height: 80
  style.fill: "#e3f2fd"
}
accept: "broker routes, persists\n(classic: disk batch; quorum: majority)" {
  width: 320
  height: 100
  style.fill: "#fff3e0"
}
ack: "basic.ack seq N (or multiple)" {
  width: 250
  height: 80
  style.fill: "#e8f5e9"
}
nack: "basic.nack (internal error only)" {
  width: 280
  height: 80
  style.fill: "#ffebee"
}
pub -> accept
accept -> ack
accept -> nack
```

**Fig. 1.** The confirm path: acceptance — including persistence — precedes the ack; nack is reserved for internal queue failures.

## Operational rules

Wait asynchronously: batch publishes and track outstanding sequence numbers, or handle acks as a stream — a blocking wait per message kills throughput. An unconfirmed publish after a timeout is an *unknown* outcome: the broker may have persisted it; republish only with an idempotent consumer, per [[Why must RabbitMQ consumers be idempotent]]. The confirm is the last piece of the survival stack in [[How do you make a RabbitMQ message survive a broker restart]] and the routing side is [[What does the RabbitMQ mandatory flag do]].

```java
ch.confirmSelect();
ch.basicPublish("", "orders", MessageProperties.PERSISTENT_TEXT_PLAIN, body);
ch.waitForConfirmsOrDie(5_000);   // production: async ConfirmListener
```

**Listing 1.** The synchronous shape for clarity; real publishers track outstanding confirms asynchronously.

> [!warning] A confirm is not a delivery receipt
> Confirms mean "the broker took responsibility for the message", not "a consumer processed it". Presenting confirms as end-to-end delivery guarantees confuses publisher-side and consumer-side mechanisms, which the docs stress are entirely orthogonal.

> [!tip] Interview answer
> Confirms are the broker-side ack for publishes: enable with confirm.select, get sequence-numbered basic.acks after acceptance — disk for persistent messages, majority for quorum queues — with basic.nack only on internal queue errors. They replace costly AMQP transactions; unconfirmed publishes after timeout are unknown outcomes needing idempotent republish.
