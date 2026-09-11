<!--
reps: 0
priority: 0
-->
#Messaging #Patterns/Enterprise/Integration/Channels/DatatypeChannel #SRS

# What is the Datatype Channel pattern?

> [!abstract] Short answer
> A **Datatype Channel** carries messages of exactly **one data type**, so the receiver learns the type from the channel it reads: a separate channel per type (`orders.xml`, `orders.json`) instead of one mixed channel where every consumer has to sniff the payload.

## Type comes from the channel, not from inspection

The sender knows the data type and therefore selects the channel designated for that type; the receiver, knowing which channel the data arrived on, already knows how to process it. This turns an implicit runtime check into an explicit topology decision: adding a new type means adding a new channel, not adding an `if` to every consumer. Messaging systems help to different degrees — JMS `ObjectMessage` carries Java classes but couples consumers to the sender's classpath, while RabbitMQ and Kafka headers carry only a type marker string, so channel/queue-per-type remains the strongest guarantee. See [[What happens when a message of the wrong type arrives on a Datatype Channel]] for the failure mode and [[What is the Message Channel pattern]] for the base idea.

```d2
direction: right
in: "Sender" {
  width: 150
  height: 55
  style.fill: "#e3f2fd"
}
chA: "Channel: order.v1\n(all messages: Order)" {
  width: 240
  height: 70
  style.fill: "#e8f5e9"
}
chB: "Channel: invoice.v1\n(all messages: Invoice)" {
  width: 240
  height: 70
  style.fill: "#e8f5e9"
}
oa: "Order consumer\ncasts without checking" {
  width: 200
  height: 70
  style.fill: "#fff3e0"
}
ib: "Invoice consumer" {
  width: 170
  height: 55
  style.fill: "#fff3e0"
}
in -> chA -> oa
in -> chB -> ib```

**Fig. 1.** Each channel is a de-facto type contract; consumers bind to the channel that matches the type they understand.

## Where the guarantee really lives

```java
// The channel name carries the contract; the payload confirms it
Destination orderChannel = session.createQueue("orders.order.v1");
ObjectMessage m = session.createObjectMessage(new Order("A-1", 3));
m.setJMSType("order.v1"); // belt and suspenders: header marker too
producer.send(orderChannel, m);
```

**Listing 1.** A JMS producer targets the `orders.order.v1` channel and also stamps `JMSType`; the channel choice is the primary contract, the header is a cross-check for brokers that route on headers.

> [!warning] Brokers rarely enforce payload types
> RabbitMQ and Kafka deliver opaque bytes — nothing at the broker rejects an `Invoice` published to `orders.order.v1`. The datatype guarantee is a **convention enforced by producers and verified by consumers**, so consumers must still validate or fail fast, moving bad payloads to an [[What is the Invalid Message Channel pattern|invalid channel]]-style quarantine rather than crashing on a cast.

> [!tip] Interview answer
> A Datatype Channel is one channel per data type, so all messages on a channel have the same type and the receiver can infer the type from the channel. It replaces runtime type sniffing with routing discipline. In brokers that treat payloads as opaque bytes the guarantee is conventional, so consumers still validate and quarantine mismatches instead of trusting the channel blindly.
