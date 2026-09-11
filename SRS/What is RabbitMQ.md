<!--
reps: 0
priority: 0
-->
#Messaging/Tools/RabbitMQ #SRS

# What is RabbitMQ

> [!abstract] Short answer
> RabbitMQ is an open-source message broker written in Erlang/OTP. It accepts messages from publishers, routes them through exchanges, and stores them in queues until consumers acknowledge them. Its native protocol is AMQP 0-9-1, and since RabbitMQ 4.0 it also supports AMQP 1.0 natively.

## What the broker actually does

RabbitMQ sits between applications and buffers data safely. A publisher opens a [[What is the difference between a RabbitMQ connection and a channel|connection and a channel]], publishes to an exchange, and the exchange routes copies to queues via bindings. A consumer subscribes to a queue, receives deliveries, and acknowledges them; only then does the broker drop the message. This is the classic [[What is the Message Broker pattern|message broker]] model, and it makes RabbitMQ a good fit for async work, buffering spikes, task queues, and RPC rather than for long-retention replay, which is the domain of Kafka.

```d2
direction: right
publisher: "Publisher\nAMQP 0-9-1 or 1.0" {
  width: 220
  height: 80
  style.fill: "#e3f2fd"
}
exchange: "Exchange\nroutes, does not store" {
  width: 240
  height: 90
  style.fill: "#fff3e0"
}
queue: "Queue\nholds until acked" {
  width: 220
  height: 90
  style.fill: "#fff3e0"
}
consumer: "Consumer\nack removes message" {
  width: 220
  height: 80
  style.fill: "#e8f5e9"
}
publisher -> exchange: "basic.publish"
exchange -> queue: "binding match"
queue -> consumer: "basic.deliver"
```

**Fig. 1.** The core path: publishers hand messages to an exchange, queues hold them, an ack releases them.

## Protocol surface and topology

The default protocol is AMQP 0-9-1, with MQTT, STOMP, the Stream protocol, and AMQP 1.0 available on the same broker. Topology — exchanges, queues, bindings, users, permissions — lives inside a [[What is a RabbitMQ virtual host|virtual host]]. See [[What protocols does RabbitMQ support]] for the protocol list and [[How does a message flow through RabbitMQ]] for the routing walk-through.

```java
ConnectionFactory cf = new ConnectionFactory();
try (Connection conn = cf.newConnection();
     Channel ch = conn.createChannel()) {
    ch.queueDeclare("orders", true, false, false, null);
    ch.basicPublish("", "orders", null, body); // default exchange
}
```

**Listing 1.** The minimal broker interaction: declare a queue and publish to it through the default exchange.

> [!warning] Not a distributed log
> A classic RabbitMQ queue deletes each message after the ack. Presenting RabbitMQ as "a durable event store like Kafka" is a popular lie — replayable history requires the Streams feature, which behaves completely differently from queues.

> [!tip] Interview answer
> RabbitMQ is an Erlang/OTP message broker implementing the AMQP model: publishers send to exchanges, exchanges route to queues by bindings, consumers acknowledge deliveries. It is strong at flexible routing, work queues, and protocol diversity, not at long-term message replay. That framing distinguishes it from log-based brokers such as Kafka.
