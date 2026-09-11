<!--
reps: 0
priority: 0
-->
#Messaging/Tools/RabbitMQ #SRS

# How does a message flow through RabbitMQ

> [!abstract] Short answer
> The publisher sends the message to an exchange with a routing key. The exchange consults its bindings and routes the message into every matching queue — it never stores anything. Each queue holds the message until a consumer processes it and acknowledges, or until TTL, overflow, or dead-letter rules act on it.

## Step by step

1. The publisher opens a connection and channel and sends `basic.publish` to an exchange, carrying a routing key and message properties.
2. The exchange applies its type logic: exact match for direct, wildcard patterns for topic, broadcast for fanout, header matching for headers.
3. Every queue bound with a matching binding receives its own copy of the message, now in the `ready` state.
4. A subscribed consumer receives a `basic.deliver` and the message moves to the `unacked` state; after `basic.ack` the message is gone.
5. If nothing matches: the message is dropped, returned if `mandatory=true`, or diverted to an [[What is a RabbitMQ alternate exchange|alternate exchange]].

```d2
direction: right
pub: "basic.publish\nrouting key + properties" {
  width: 250
  height: 90
  style.fill: "#e3f2fd"
}
ex: "Exchange\ntype + bindings" {
  width: 210
  height: 80
  style.fill: "#fff3e0"
}
ready: "Queue: ready state" {
  width: 210
  height: 70
  style.fill: "#fff3e0"
}
unacked: "Queue: unacked state" {
  width: 220
  height: 70
  style.fill: "#ffebee"
}
gone: "acked → deleted" {
  width: 200
  height: 60
  style.fill: "#e8f5e9"
}
pub -> ex
ex -> ready: "copies"
ready -> unacked: "basic.deliver"
unacked -> gone: "basic.ack"
```

**Fig. 1.** State of a message along the flow: routing produces ready copies, delivery makes them unacked, an ack deletes them.

## Where the flow breaks

Publishes are fire-and-forget by default: `basic.publish` returning without error does not mean the broker accepted the message. Publisher confirms exist exactly for that gap — see [[What are publisher confirms in RabbitMQ]]. On the consumer side, an unacknowledged delivery is requeued when the channel dies, which is why handlers must tolerate redelivery, per [[What happens if a RabbitMQ consumer crashes before ack]].

```java
ch.confirmSelect();                       // put channel in confirm mode
ch.basicPublish("orders", "order.created",
        MessageProperties.PERSISTENT_TEXT_PLAIN, body);
ch.waitForConfirmsOrDie(5_000);          // broker accepted responsibility
```

**Listing 1.** A publish that actually checks broker acceptance instead of hoping.

> [!warning] The exchange stores nothing
> Interviewees often describe the exchange as a buffer. It is not: an exchange is a routing table, and an unroutable message either vanishes, comes back via `basic.return`, or goes to an alternate exchange — it never waits there for a future binding.

> [!tip] Interview answer
> Publish to an exchange with a routing key; the exchange matches bindings by its type and writes copies into matching queues; consumers get pushes, process, and ack, which deletes the message. Unroutable messages are dropped, returned, or diverted. Confirms cover the publish side, acks the consume side — the two are orthogonal.
