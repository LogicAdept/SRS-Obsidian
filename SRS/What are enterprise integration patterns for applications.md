<!--
reps: 0
priority: 0
-->
#Patterns/Enterprise/Integration #SRS

# What are enterprise integration patterns for applications

> [!abstract] Short answer
> Enterprise Integration Patterns (EIP) is a catalogue of 65 technology-independent design patterns for asynchronous messaging between applications, collected by Gregor Hohpe and Bobby Woolf and published in the 2003 book of the same name. The patterns are grouped into message construction, channels, routing, transformation, endpoints, and system management, and frameworks like Apache Camel and Spring Integration implement them by name.

## The catalogue at a glance

The patterns assume the Messaging integration style and then cover the full path of a message:

* **Message Construction** - the shape and intent of a message: Message, Command Message, Document Message, Event Message, Request-Reply, Return Address, Correlation Identifier, Message Sequence, Message Expiration, Format Indicator.
* **Messaging Channels** - how messages travel: Message Channel, Point-to-Point Channel, Publish-Subscribe Channel, Datatype Channel, Invalid Message Channel, Dead Letter Channel, Guaranteed Delivery, Channel Adapter, Messaging Bridge, Message Bus.
* **Message Routing** - who receives what: Pipes-and-Filters, Message Router, Content-Based Router, Message Filter, Dynamic Router, Recipient List, Splitter, Aggregator, Resequencer, Scatter-Gather, Routing Slip, Process Manager, Message Broker.
* **Message Transformation** - reshaping content between systems: Message Translator, Envelope Wrapper, Content Enricher, Content Filter, Claim Check, Normalizer, Canonical Data Model.
* **Messaging Endpoints** - how applications produce and consume: Messaging Gateway, Transactional Client, Polling Consumer, Event-Driven Consumer, Competing Consumers, Selective Consumer, Durable Subscriber, Idempotent Receiver, Service Activator.
* **System Management** - keeping the messaging system healthy: Control Bus, Detour, Wire Tap, Message History, Message Store, Smart Proxy, Test Message, Channel Purger.

```d2
direction: right
cons: "Construction\nCommand? Event?\nReply handling" {
  width: 220
  height: 90
  style.fill: "#e3f2fd"
}
chan: "Channels\npoint-to-point,\npub-sub, DLQ" {
  width: 220
  height: 90
  style.fill: "#fff3e0"
}
route: "Routing\nrouters, splitter,\naggregator" {
  width: 220
  height: 90
  style.fill: "#e8f5e9"
}
trans: "Transformation\ntranslator,\nnormalizer" {
  width: 220
  height: 90
  style.fill: "#fff3e0"
}
endp: "Endpoints\nconsumers, gateways,\nidempotent receiver" {
  width: 230
  height: 90
  style.fill: "#e3f2fd"
}
mgmt: "System management\nwire tap, control bus,\nmessage store" {
  width: 240
  height: 90
  style.fill: "#ffebee"
}
cons -> chan
chan -> route
route -> trans
trans -> endp
endp -> mgmt: "operated by"
```

**Fig. 1.** The six working areas of the catalogue follow a message from construction through transport, routing, and transformation to endpoint code and the tooling that keeps it running.

## Why the vocabulary matters

The patterns were harvested from integration projects, not invented, and the authors publish the pattern statements under an open license. Because the names are technology-neutral, they transfer directly: a Dead Letter Channel is a dead-letter topic in Kafka, a Publish-Subscribe Channel is a fanout exchange in RabbitMQ, and Competing Consumers describes a consumer group. Apache Camel, Spring Integration, and Mule implement the catalogue so routes can literally be written in EIP terms, and the same names cover brokers like ActiveMQ, Kafka, and RabbitMQ plus cloud services such as SQS, EventBridge, and Google Pub/Sub.

Single patterns deserve their own cards: [[What is the Competing Consumers pattern]] and [[What is the Event-Driven Consumer pattern]] cover the endpoint side, [[What is the Guaranteed Delivery pattern]] the channel side, and [[What is the partitioned consumer pattern]] the Kafka-style refinement where partitions replace competition. On the message side, [[What is the difference between a command and an event]] separates Command Message from Event Message. Integration itself is not only messaging - [[How would you explain transaction log tailing for integration]] is the database-first alternative that still lands in this vocabulary.

```java
// Conceptual Apache Camel route: Pipes-and-Filters plus a Content-Based Router
from("jms:orders")
    .unmarshal().json()                      // Message Translator
    .choice()                                // Content-Based Router
        .when().jsonpath("$.type == 'vip'").to("jms:orders.vip")
        .otherwise().to("jms:orders.standard")
    .end();
```

**Listing 1.** The EIP names describe the route: unmarshalling is a Message Translator, and the `choice` block is a Content-Based Router.

> [!warning] The vocabulary is not an implementation contract
> An EIP name maps onto each broker differently: ordering, TTLs, and redelivery semantics differ between Kafka, RabbitMQ, and JMS brokers, so a "Guaranteed Delivery" configuration on one platform is not automatically equivalent on another. Interview answers that recite names without broker semantics sound rehearsed.

> [!tip] Interview answer
> EIP is the 2003 Hohpe and Woolf catalogue of 65 messaging design patterns, organized into message construction, channels, routing, transformation, endpoints, and system management. Its value is a shared, technology-neutral vocabulary - Splitter, Content-Based Router, Dead Letter Channel, Idempotent Receiver - that maps onto brokers and frameworks like Camel, Spring Integration, Kafka, and RabbitMQ. When I design an integration I name the parts in EIP terms first, then choose the technology for each.
