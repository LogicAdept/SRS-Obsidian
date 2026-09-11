<!--
reps: 0
priority: 0
-->
#Messaging #Patterns/Enterprise/Integration/Messages #SRS

# What is the Message pattern?

> [!abstract] Short answer
> A **Message** is the atomic data record of a messaging system: a **header** the infrastructure uses to route and manage the data, and a **body** holding the data itself, which the messaging system transmits as-is. Everything sent through channels travels as one or more messages.

## Header versus body — who owns what

The header describes the data: its origin, destination, format, message id, expiration, correlation id — fields the messaging system and middleware read. The body is the application's payload, generally ignored by the messaging system and transmitted unchanged. This split keeps infrastructure concerns out of application data and vice versa; routing, dead-lettering, and filtering decisions should hang off headers, while business code owns the body. Concrete header fields vary by platform (JMS `JMSMessageID` / `JMSDestination` / `JMSType`, AMQP properties, Kafka record headers) but the division of labor is stable. Specializations of the Message pattern differ only in what the body carries — command, document, or event — see [[What is the Command Message pattern]], and the comparison in [[What is the difference between a command and an event]].

```d2
direction: right
hdr: "Header\nmessage id, destination,\ncorrelation id, expiration" {
  width: 260
  height: 90
  style.fill: "#e3f2fd"
}
body: "Body\napplication payload\n(opaque to the broker)" {
  width: 260
  height: 90
  style.fill: "#e8f5e9"
}
msg: "Message" {
  width: 150
  height: 50
  style.fill: "#fff3e0"
}
msg -> hdr
msg -> body```

**Fig. 1.** Two parts, two owners: middleware reads the header, applications read the body.

## A message as the API sees it

```java
TextMessage m = session.createTextMessage("{"sku":"A-1","qty":3}");
m.setStringProperty("eventType", "order.created"); // business metadata
m.setJMSType("order.created.v1");                  // format marker
m.setJMSCorrelationID(correlationId);
producer.send(ordersChannel, m); // JMSMessageID/JMSDestination set by the system
```

**Listing 1.** Application code stamps properties; the provider fills the transport-level header fields on send.

> [!warning] Do not park business data in headers
> Headers are for the messaging system and cross-cutting middleware decisions. Once business payload starts living in header fields, every consumer, router, and tool has to parse application semantics out of infrastructure metadata — and header size limits bite (Kafka headers are not size-bounded but brokers and clients choke on megabyte headers; JMS properties are primitively typed).

> [!tip] Interview answer
> The Message pattern defines the envelope of all messaging: a header with system-managed fields — ids, destinations, expiration — and a body with the application data that the messaging system passes through untouched. Command, Document, and Event Messages are just different body semantics on this envelope. The design rule is: routing and middleware decisions read headers, business code reads bodies.
