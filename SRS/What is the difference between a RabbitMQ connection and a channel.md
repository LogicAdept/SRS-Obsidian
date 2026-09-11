<!--
reps: 0
priority: 0
-->
#Messaging/Tools/RabbitMQ #SRS

# What is the difference between a RabbitMQ connection and a channel

> [!abstract] Short answer
> A connection is the TCP (or TLS) session between client and broker, authenticated and carrying an address to one vhost. A channel is a lightweight virtual session multiplexed over that connection, where every AMQP operation — declare, publish, consume, ack — actually happens.

## Why two levels

Opening TCP connections is expensive and firewalls dislike hundreds of them, so AMQP 0-9-1 multiplexes independent streams over one connection. Each channel has its own numbering space, and errors are channel-scoped: a failed declare raises a channel exception and closes only that channel, while the connection and other channels survive. Delivery tags are also per channel, so a delivery must be acked on the channel that received it — the rule behind [[What is RabbitMQ consumer acknowledgement]].

```d2
direction: down
conn: "TCP connection\nauth, vhost, heartbeats" {
  width: 280
  height: 80
  style.fill: "#e3f2fd"
}
ch1: "channel 1\npublish" {
  width: 170
  height: 70
  style.fill: "#fff3e0"
}
ch2: "channel 2\nconsume + ack" {
  width: 190
  height: 70
  style.fill: "#fff3e0"
}
ch3: "channel 3\nadmin/declare" {
  width: 190
  height: 70
  style.fill: "#fff3e0"
}
conn -> ch1
conn -> ch2
conn -> ch3
```

**Fig. 1.** One authenticated connection carries several independent channels; each owns its own publish or consume work.

## Operating rules

Connections and channels are both long-lived; opening a channel per publish is a roundtrip per operation and an anti-pattern, and it also destroys the [[What is RabbitMQ prefetch]] budget you carefully tuned. Channels are not thread-safe — standard practice is one channel per thread and separate connections for publishing versus consuming so broker flow control on a fast publish path cannot stall consumer acks, per [[Why use separate RabbitMQ connections for publishing and consuming]]. When the connection dies, every channel on it dies with it and all unacked deliveries are requeued.

```java
Connection conn = cf.newConnection();
Channel pubCh = conn.createChannel();   // thread A
Channel conCh = conn.createChannel();   // thread B, its own channel
```

**Listing 1.** Two threads, two channels, one connection; sharing one channel across both threads would corrupt frame state.

> [!warning] A channel error is not a connection error
> Publishing to a nonexistent exchange closes the channel with 404, not the connection — but repeatedly ignoring channel closures and reusing the dead channel object is a classic client bug. Catch the exception, recreate the channel, and re-declare what the operation needed.

> [!tip] Interview answer
> A connection is the authenticated TCP session to one vhost; channels are multiplexed lightweight sessions inside it where the real protocol work happens. Errors and delivery tags are channel-scoped, channels are not thread-safe, and high-throughput apps run separate publish and consume connections.
