<!--
reps: 0
priority: 0
-->
#Messaging #Patterns/Enterprise/Integration/Messaging/DurableSubscriber #SRS

# What is the Durable Subscriber pattern?

> [!abstract] Short answer
> A **Durable Subscriber** asks the messaging system to **keep pub-sub messages published while it is disconnected** and deliver them on reconnect — the subscription, not the connection, is the long-lived thing.

## Persistence keyed to the subscriber's identity

On a plain publish-subscribe channel, a message published while a subscriber is offline is gone for good — pub-sub is broadcast to whoever is listening. A durable subscription changes exactly that window: the broker saves messages for the named inactive subscription and delivers the backlog when the subscriber reconnects; while connected, behavior is identical to a non-durable subscription. JMS expresses it as a named durable subscription (`createDurableConsumer`/`unsubscribe`); RabbitMQ achieves the same by the queue being the durable, always-present entity that bindings feed; Kafka generalizes it entirely — consumer groups persist offsets, so a group "subscribes durably" to a topic by default. Backlogs have a price: the broker retains data per subscription, so an absent subscriber is a growing liability — pair durability with retention limits and [[What is the Message Expiration pattern]] so a week-old event does not land on a freshly reconnected observer. On the delivery side this composes with [[What is the Guaranteed Delivery pattern]]; the channel semantics it extends are [[What is the Publish-Subscribe Channel pattern]].

```d2
direction: down
pub: "Publisher\nkeeps publishing" {
  width: 200
  height: 60
  style.fill: "#e3f2fd"
}
ps: "Pub-Sub Channel" {
  width: 190
  height: 55
  style.fill: "#fff3e0"
}
online: "Active subscriber\ngets copies live" {
  width: 220
  height: 65
  style.fill: "#e8f5e9"
}
off: "Durable subscriber\nDISCONNECTED" {
  width: 220
  height: 65
  style.fill: "#ffebee"
}
backlog: "Broker retains\nits messages" {
  width: 210
  height: 65
  style.fill: "#fff3e0"
}
pub -> ps
ps -> online
ps -> backlog: "while offline"
backlog -> off: "reconnect:\ndrain backlog" {
  style.stroke-dash: 4
}```

**Fig. 1.** Only the durable subscriber's stream is preserved during absence; the active subscriber never notices a difference.

## Identity is the contract

```java
// JMS: the subscription name is the durable identity
MessageConsumer durable = session.createDurableConsumer(
        topic, "billing-events");      // broker retains while offline
// ...
session.unsubscribe("billing-events"); // only when truly done forever
```

**Listing 1.** The name binds reconnects to the retained backlog; forgetting `unsubscribe` leaves the broker storing messages nobody will ever read.

> [!warning] Absent subscribers stockpile data
> A durable subscription that stays offline accumulates a backlog the broker must store, order, and eventually deliver in a burst — the reconnect stampede can overwhelm the very subscriber that was away. Retention policies and expiration bound the liability, and monitoring per-subscription backlog is not optional: an unwatched durable subscription is a slow leak in the broker.

> [!tip] Interview answer
> A Durable Subscriber keeps receiving pub-sub messages it missed while disconnected: the broker retains messages for the named subscription and delivers the backlog on reconnect; connected behavior is unchanged. JMS durable subscriptions, RabbitMQ's durable queues under an exchange, and Kafka's consumer-group offsets are the same idea at different depths. The duty is backlog governance — retention, expiration, and monitoring per subscription.
