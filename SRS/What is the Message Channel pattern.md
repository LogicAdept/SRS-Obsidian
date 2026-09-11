<!--
reps: 0
priority: 0
-->
#Messaging #Patterns/Enterprise/Integration/Channels #SRS

# What is the Message Channel pattern?

> [!abstract] Short answer
> A **Message Channel** is a named pipe inside a messaging system: a sender **writes** a message to the channel, a receiver **reads** from it, and the two never call each other directly. The channel decouples sender from receiver in time, location, and threading.

## How a channel separates producers from consumers

Applications never fling data into the messaging system "in general" — every message is added to a specific channel, and receivers read from a specific channel. The sender does not know which application will pick the message up; it only knows that whatever reads from that channel is interested in that kind of information. This is why channels are usually named and scoped by purpose (`orders.incoming`, `payments.settlement`), not by audience. A channel can be **point-to-point** (one consumer gets each message) or **publish-subscribe** (every subscriber gets a copy) — the same physical queue/topic configuration options express these two semantics in JMS, RabbitMQ, and Kafka. Compare [[What is the Publish-Subscribe Channel pattern]] and the type-per-channel idea in [[What is the Datatype Channel pattern]].

```d2
direction: right
sender: "Sender app" {
  width: 170
  height: 60
  style.fill: "#e3f2fd"
}
ch: "Message Channel\norders.incoming" {
  width: 220
  height: 70
  style.fill: "#fff3e0"
}
r1: "Receiver app" {
  width: 170
  height: 60
  style.fill: "#e8f5e9"
}
sender -> ch: "write"
ch -> r1: "read"```

**Fig. 1.** The channel is the only coupling point: both sides know the channel, not each other.

## Channel semantics in real systems

```java
// JMS: the channel is a Destination (queue or topic)
Queue orders = session.createQueue("orders.incoming");
MessageProducer producer = session.createProducer(orders);
producer.send(session.createTextMessage("{"sku":"A-1","qty":3}"));

MessageConsumer consumer = session.createConsumer(orders);
TextMessage msg = (TextMessage) consumer.receive(1000);
```

**Listing 1.** The same `Destination` object is the sender's target and the receiver's source; neither side references the other.

> [!warning] A channel is not a synchronous call
> Code that sends on a channel and then expects a return value in the same thread has silently reinvented RPC on top of messaging. One-way fire-and-forget is the default; if you need an answer, pair two channels explicitly with [[What is the Request-Reply pattern]] and [[What is the Return Address pattern]], and do not assume the message is even consumed yet.

> [!tip] Interview answer
> A Message Channel is the basic EIP building block: a logical address inside the messaging system that senders write to and receivers read from. It decouples producers from consumers — they share a channel name and message format instead of network endpoints. Channels differ in delivery semantics: point-to-point delivers each message to exactly one consumer, publish-subscribe delivers a copy to every subscriber.
