<!--
reps: 0
priority: 0
-->
#Messaging/Tools/RabbitMQ #SRS

# What protocols does RabbitMQ support

> [!abstract] Short answer
> AMQP 0-9-1 and AMQP 1.0 are core protocols on port 5672 since 4.0; MQTT, STOMP, and the Stream protocol are shipped plugins that enable extra listeners — MQTT on 1883, STOMP on 61613, streams on 5552. HTTP API on 15672 is management, not messaging.

## The protocol menu

Each protocol serves a niche. AMQP 0-9-1 is the native, semantics-rich default with exchanges, queues, bindings, and acks. AMQP 1.0, native since 4.0 without any plugin, serves interop with other brokers and cloud services. MQTT targets constrained IoT devices with pub/sub and keepalives; its QoS 2 is unsupported — published QoS 2 is downgraded to QoS 1 for MQTT 3.x clients and rejected for 5.0 clients. STOMP is a simple text protocol proxied over AMQP 0-9-1. The Stream protocol is a dedicated binary protocol for high-throughput reads of streams, including offset-based consumption — see [[What are RabbitMQ streams]] for the data structure it serves.

```d2
direction: right
clients: "clients" {
  width: 140
  height: 60
  style.fill: "#e3f2fd"
}
core: "5672\nAMQP 0-9-1 + 1.0" {
  width: 200
  height: 80
  style.fill: "#fff3e0"
}
p1: "1883\nMQTT plugin" {
  width: 160
  height: 80
  style.fill: "#ffebee"
}
p2: "61613\nSTOMP plugin" {
  width: 170
  height: 80
  style.fill: "#ffebee"
}
p3: "5552\nStream plugin" {
  width: 170
  height: 80
  style.fill: "#ffebee"
}
clients -> core
clients -> p1
clients -> p2
clients -> p3
```

**Fig. 1.** One broker, several listeners: core protocols share port 5672, plugin protocols open their own.

## TLS and the management port

Every listener has a TLS twin one port up: 5671 for AMQPS, 8883 for MQTT, 61614 for STOMP, 5551 for streams, 15671 for management. The management UI and HTTP API port does not speak any messaging protocol — a frequent confusion in setups that try to connect a client to 15672.

```bash
rabbitmq-plugins enable rabbitmq_mqtt rabbitmq_stomp
```

**Listing 1.** Enabling the MQTT and STOMP plugins opens their default listeners on the next restart.

Protocol identity is one half of [[What is AMQP]]; the other half is 0-9-1's broker model, which the other plugins borrow through mapping.

> [!warning] Plugin protocols are not feature-complete AMQP
> MQTT and STOMP clients get topic-ish access mapped onto queues and exchanges, with real semantic gaps — MQTT has no competing-consumer prefetch vocabulary, and STOMP maps destinations to AMQP topologies. Building an architecture around "RabbitMQ speaks everything identically" breaks on these limits.

> [!tip] Interview answer
> Core: AMQP 0-9-1 and, since 4.0, AMQP 1.0 on 5672. Plugins: MQTT 3.1/3.1.1/5.0 for IoT with QoS 0/1 only, STOMP for simple text clients, and the Stream protocol for high-throughput streaming on 5552. Management is HTTP on 15672, not a messaging protocol. TLS twins exist for all of them.
