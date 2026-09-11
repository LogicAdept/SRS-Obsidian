<!--
reps: 0
priority: 0
-->
#Messaging #Patterns/Enterprise/Integration/Messages/EventMessage #SRS

# What is the Event Message pattern?

> [!abstract] Short answer
> An **Event Message** announces that **something happened**: the subject creates an event object, wraps it in a message, and publishes it; interested observers react. It is reliable asynchronous event notification — delivery is guaranteed, and the notification is the entire contract.

## Timing matters more than content

Unlike a command, an event does not tell the receiver what to do, and unlike a document, its content is usually secondary — many events are effectively empty, their mere occurrence being the information. Timing is the opposite of a document: the subject should publish the event as soon as the change occurs, and observers should process it quickly while it is still relevant. This changes the reliability calculus: guaranteed persistence is usually **not** helpful for events, because they are frequent and stale events lose value fast; a short expiration is usually more useful, so stale notifications are dropped instead of processed — see [[What is the Message Expiration pattern]]. Event Messages are the natural payload of [[What is the Publish-Subscribe Channel pattern]], and their semantics are contrasted with commands in [[What is the difference between a command and an event]].

```d2
direction: right
subj: "Subject\nstate changed" {
  width: 180
  height: 60
  style.fill: "#e3f2fd"
}
ch: "Pub-sub channel\nOrderPlaced event" {
  width: 220
  height: 65
  style.fill: "#fff3e0"
}
o1: "Observer A\nreact now" {
  width: 170
  height: 60
  style.fill: "#e8f5e9"
}
o2: "Observer B" {
  width: 150
  height: 55
  style.fill: "#e8f5e9"
}
subj -> ch
ch -> o1
ch -> o2```

**Fig. 1.** One occurrence, several observers, no instructions — each observer decides what the event means for it.

## Minimal, occurrence-first payload

```java
// Event body: what happened, when, to what -- not what to do
String json = "{\"event\":\"OrderPlaced\","
            + "\"orderId\":\"O-42\","
            + "\"occurredAt\":\"2026-09-11T09:15:00Z\"}";
TextMessage event = session.createTextMessage(json);
producer.setDeliveryMode(DeliveryMode.NON_PERSISTENT); // speed over durability
producer.setTimeToLive(30_000);                        // stale = useless
producer.publish(pricesTopic, event);
```

**Listing 1.** The event names the occurrence; observers decide the reaction. A short TTL matches the "quickly or not at all" contract.

> [!warning] Events are facts, not disguised commands
> An event body that reads like an imperative ("retry payment", "send email") couples the publisher to every subscriber's behavior and turns a fact into gossip about duties. Observers derive their own actions from the fact; if coordination of actions is really required, that is a saga or process-manager conversation, not an event payload.

> [!tip] Interview answer
> An Event Message reliably notifies observers that something happened. Its content is typically thin — often just an identifier and a timestamp — and its value decays quickly, so short expiration usually beats durable persistence. Events ride publish-subscribe channels, observers react independently, and unlike commands they never instruct the receiver what to do.
