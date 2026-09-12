<!--
reps: 0
priority: 0
-->
#Patterns/Architecture/Microservices/CommunicationStyles #Messaging #SRS

# What is the messaging communication style between microservices

> [!abstract] Short answer
> Messaging style: services communicate asynchronously by sending messages over channels through a message broker - Kafka, RabbitMQ - instead of calling each other directly. The communication-style counterpart of request/response over RPI; it decouples the sender from the receiver in time and availability, and underlies choreography, event-driven integration and the outbox. One-way and pub/sub interaction styles are native to it; request/reply is possible but more work.

## Mechanism: channels, broker, delivery guarantees

A sender writes a message to a channel - a topic or queue hosted by a broker - and returns to its work; the broker stores and forwards it to consumers, buffering messages until they can process them. The taxonomy of asynchronous interaction styles: one-way notifications (send, no reply expected), request/async-response (send, reply arrives eventually on a reply channel), publish/subscribe (one message delivered to zero or more subscribers), and publish/async-response (publish, collect replies from some subscribers). The broker is infrastructure with its own HA requirements - it must be at least as available as the communication it carries. Semantics are at-least-once in practice: redeliveries after consumer failure are normal, so receivers deduplicate ([[What is the Idempotent Receiver pattern]] is the receiver-side pattern; [[Why must RabbitMQ consumers be idempotent]] shows it with a concrete broker). The hard case is request/reply: correlating a reply with its request needs correlation IDs and reply channels - doable, but it is the style's complexity bump.

```d2
direction: right
osvc: "Order Service
producer" {style.fill: "#e8f5e9"}
b: "Broker
topic: orders" {style.fill: "#fff3e0"}
inv: "Inventory Service
consumer" {style.fill: "#eceff1"}
eml: "Email Service
consumer" {style.fill: "#eceff1"}
an: "Analytics
consumer" {style.fill: "#eceff1"}
osvc -> b: publish OrderCreated
b -> inv: deliver
b -> eml: deliver
b -> an: deliver
```

**Fig. 1.** One published event, three consumers, zero live coupling - the Order Service neither knows nor waits for them.

The benefits: loose runtime coupling (sender and receiver do not need to be up at the same time), improved availability because the broker buffers while a consumer is down or slow, and native support for the fan-out of domain events that choreography needs. The costs: a broker becomes critical infrastructure that must be highly available and operated; the programming model is harder than an HTTP call - channels, serialization evolution, delivery semantics, consumer groups. The direct alternative is synchronous remote procedure invocation ([[What is the remote procedure invocation pattern between microservices]] compares the styles; [[Which interaction styles do you know in microservices]] catalogs one-to-one versus one-to-many and synchronous versus asynchronous). Reliability of the "publish after commit" step is its own pattern - [[How would you explain the transactional outbox pattern]] - because a broker write cannot join the database's ACID transaction.

> [!warning] Async is a contract change, not a transport swap
> Swapping a REST call for a message changes the caller's semantics: the work has not happened when the send returns - it may not happen for seconds, and the sender has no synchronous error to handle. UI flows that needed the result now need correlation, polling or push. Second trap: hidden synchronous chains inside async plumbing - service A publishes, consumer B synchronously calls C before acking, and the "async" path is as coupled as the RPC chain it replaced, plus indirection. Also budget for message evolution: producers and consumers deploy independently, so schemas must stay backward compatible.

> [!tip] Interview answer
> Messaging style is asynchronous inter-service communication through a broker: senders publish to channels and move on, the broker buffers and delivers to consumers - notifications, request/async-response, pub/sub. It buys loose coupling, temporal decoupling and availability via buffering, and powers choreography and event-driven design. The costs are operating the broker, harder request/reply correlation and at-least-once semantics, so consumers must be idempotent and I use the outbox to publish after commit.
