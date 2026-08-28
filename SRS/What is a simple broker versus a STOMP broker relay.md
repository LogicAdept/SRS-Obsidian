<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebSocket #Messaging #SRS

# What is a simple broker versus a STOMP broker relay?

> [!abstract] Short answer
> **`enableSimpleBroker`** is Spring’s **in-memory** broker: it stores subscriptions and broadcasts to matching clients in **this JVM**. It supports path/Ant destinations and (with a **`TaskScheduler`**) STOMP heartbeats. It does **not** do acks/receipts as a full broker would, and it **cannot cluster**. **`enableStompBrokerRelay`** opens **TCP** to an external STOMP broker (RabbitMQ, ActiveMQ, …): one **system** connection for app-originated messages plus **one TCP connection per WebSocket client**. The external broker is what fans out **across instances**.

## In-process loop vs TCP relay

Simple broker: `SimpleBrokerMessageHandler` — good to start; “simple sending loop”; not suitable for clustering (Framework 6.2 External Broker + Performance pages). Relay: `StompBrokerRelayMessageHandler` forwards STOMP both ways. Needs **`reactor-netty`** and **`netty-all`**. Defaults: host **`127.0.0.1`**, port **`61613`**, client and system **`guest`/`guest`**. Relay **overwrites** client CONNECT `login`/`passcode`. Heartbeats on the **system** connection: **10 s** send and receive; reconnect every **5 s**. Configure: [[How do you configure a STOMP broker in Spring]]. Scale: [[How do you scale Spring WebSocket across instances]]. Keepalive: [[How do you keep a Spring WebSocket connection alive]]. Protocol: [[What is STOMP in Spring WebSocket]].

```java
registry.enableSimpleBroker("/topic", "/queue");

registry.enableStompBrokerRelay("/topic", "/queue")
		.setRelayHost("broker.internal")
		.setRelayPort(61613);
```

**Listing 1.** Conceptual: pick **one**. Relay prefixes must match what **that** broker documents. Simple-broker `/topic` vs `/queue` is only a **convention**.

| | Simple broker | STOMP broker relay |
| --- | --- | --- |
| Where subscriptions live | This process | External broker |
| Multi-instance pub/sub | No | Yes (each app connects) |
| Acks / receipts / extra STOMP | Subset | Broker’s full STOMP |
| App → broker | In-JVM | Shared **system** TCP |

Multi-node **user** destinations also need **`setUserDestinationBroadcast`** / **`setUserRegistryBroadcast`** on the relay registration — otherwise `/user/` routing stays local.

```d2
direction: down
simple: "enableSimpleBroker\nin-memory" {
  width: 240
  height: 50
  style.fill: "#e3f2fd"
}
relay: "enableStompBrokerRelay\nTCP to Rabbit/ActiveMQ" {
  width: 280
  height: 50
  style.fill: "#fff3e0"
}

simple -> relay: "upgrade to cluster"
```

**Fig. 1.** Two Boot instances with only a simple broker never share `/topic` subscribers.

> [!warning]Relay login is not browser identity
> `systemLogin`/`clientLogin` default to **guest**. JS `login`/`passcode` on CONNECT are **ignored**. Authenticate the **HTTP handshake**. Missing Netty dependencies fail TCP setup, not `@MessageMapping` mapping.

> [!tip] Interview answer
> **Simple broker is in-memory fan-out in one JVM; the STOMP relay TCP-forwards to RabbitMQ/ActiveMQ.** Clustered pub/sub needs the relay. Simple broker plus two instances means two separate subscription maps. Heartbeats and `/app` prefixes are orthogonal to that choice.
