<!--
reps: 0
priority: 0
-->
#Messaging/Tools/RabbitMQ #SRS

# What is the difference between ack nack and reject in RabbitMQ

> [!abstract] Short answer
> `basic.ack` confirms success and deletes. `basic.reject` and `basic.nack` both requeue or dead-letter one message, but since RabbitMQ 4.3 they differ semantically for poison handling: reject signals a processing failure and increments x-delivery-count, nack signals "not processed" and does not. Nack also supports bulk via multiple=true; reject does not.

## The API surface

`basic.reject(delivery_tag, requeue)` is the AMQP 0-9-1 method for a single delivery. `basic.nack` is a RabbitMQ extension adding `multiple=true` — negative-acknowledge everything up to the tag, mirroring bulk acks. Both take requeue: true puts the message back (near its original position), false sends it to the DLX if configured or drops it. Requeued messages land "at their original position if possible, otherwise closer to the head".

## The 4.3 poison-counting split

The modern docs draw a semantic line: reject means the consumer *failed* to process, so the queue's delivery-count grows and delivery limits approach; nack means the consumer *did not process it*, leaving the count untouched. This matters only for quorum-queue poison handling — `x-delivery-limit` counts failed deliveries, and unlimited explicit nack-returns are allowed without counting. Client crashes and consumer timeouts still count as failures, per the quorum-queue counting table. The poison-loop context lives in [[What is a poison message in RabbitMQ]] and the retry designs in [[How do you implement retries in RabbitMQ]].

```d2
direction: down
ack: "basic.ack\nsuccess → delete" {
  width: 210
  height: 80
  style.fill: "#e8f5e9"
}
rej: "basic.reject\nfailure → count + 1" {
  width: 240
  height: 90
  style.fill: "#ffebee"
}
nk: "basic.nack\nnot processed → no count" {
  width: 250
  height: 90
  style.fill: "#fff3e0"
}
dlx: "requeue=false → DLX" {
  width: 200
  height: 70
  style.fill: "#fff3e0"
}
rej -> dlx
nk -> dlx
```

**Fig. 1.** Same requeue/DLX outcomes, different accounting: reject counts toward the delivery limit, nack does not.

```java
// failed processing: counts toward x-delivery-limit
ch.basicReject(tag, false);
// deferring work without punishing the message
ch.basicNack(tag, false, true);
```

**Listing 1.** Same two parameters, different poison-accounting semantics in 4.3+.

> [!warning] "Nack is just bulk reject" is outdated
> That was true through 3.13 and early 4.x — the current docs explicitly split the semantics. An interview answer that stops at "multiple=true" misses the delivery-limit interaction, which is exactly the follow-up about poison messages.

> [!tip] Interview answer
> Ack deletes after success. Reject and nack both requeue or dead-letter; nack adds bulk via multiple, reject is single-message. Since 4.3, reject counts as a failed delivery toward quorum queues' x-delivery-limit while nack does not, so they are no longer interchangeable under poison handling — and requeue=false on either is the DLX trigger behind [[What is a RabbitMQ dead letter exchange]].
