<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebSocket #Messaging #SRS

# How do you scale Spring WebSocket across instances?

> [!abstract] Short answer
> **You cannot scale pub/sub with the simple broker.** Each instance keeps its own in-memory subscriptions. Use **`enableStompBrokerRelay`** to a full STOMP broker (RabbitMQ, ActiveMQ, …). **Every app instance** opens TCP to that broker; a broadcast from instance A reaches WebSocket clients on instance B **through the broker**. Each client WebSocket still terminates on **one** JVM (plus one relay TCP per client, plus one shared **system** connection).

## Broker first, then the load balancer

Framework 6.2 Performance page: multiple application instances work with a **full-featured broker**, not `enableSimpleBroker`. Relay details: [[What is a simple broker versus a STOMP broker relay]]. Configure: [[How do you configure a STOMP broker in Spring]]. User destinations that stay local need **`setUserDestinationBroadcast`** and **`setUserRegistryBroadcast`** on the relay so other nodes can resolve `/user/` and share **`SimpUserRegistry`**. Heartbeats do not replace a relay ([[How do you keep a Spring WebSocket connection alive]]). STOMP: [[What is STOMP in Spring WebSocket]].

The HTTP/WebSocket handshake must reach a node that speaks Upgrade. Reverse proxies have to **forward `Upgrade` and `Connection`** (WebSocket intro). A given socket stays on that node for its lifetime — that is TCP, not “simple-broker clustering.” Sticky routing does **not** copy in-memory simple-broker subscriptions to the next instance.

Also size **`clientInboundChannel` / `clientOutboundChannel`** (6.2: default pools are **twice the processor count**) and **`sendTimeLimit` / `sendBufferSizeLimit`**. Relay stats: TCP count should be **client sessions + 1** system connection (`WebSocketMessageBrokerStats`).

```java
@Override
public void configureMessageBroker(MessageBrokerRegistry registry) {
	registry.setApplicationDestinationPrefixes("/app");
	registry.enableStompBrokerRelay("/topic", "/queue")
			.setRelayHost("broker.internal")
			.setRelayPort(61613)
			.setUserDestinationBroadcast("/topic/unresolved-user")
			.setUserRegistryBroadcast("/topic/user-registry");
}
```

**Listing 1.** Conceptual: shared broker plus optional user-registry gossip. Requires Netty TCP client libraries.

```d2
direction: down
a: "App instance A\nWebSocket clients" {
  width: 240
  height: 50
  style.fill: "#e3f2fd"
}
b: "App instance B\nWebSocket clients" {
  width: 240
  height: 50
  style.fill: "#e3f2fd"
}
br: "STOMP broker (Rabbit/ActiveMQ)" {
  width: 280
  height: 40
  style.fill: "#fff3e0"
}

a -> br
b -> br
```

**Fig. 1.** Simple broker would be two disconnected subscription maps. The broker is the fan-out bus.

> [!warning]Sticky sessions do not cluster a simple broker
> Pinning a browser to one instance keeps **that** socket alive. It does **not** deliver `/topic` messages published on another instance. Idle proxies that drop long-lived connections still kill sockets even with a relay — that is transport, not broker topology.

> [!tip] Interview answer
> **Scale STOMP by replacing the simple broker with `enableStompBrokerRelay` to RabbitMQ/ActiveMQ.** Each instance connects; the broker broadcasts. For `/user` across nodes, set user-destination and user-registry broadcast destinations. The load balancer must pass WebSocket Upgrade; it cannot make in-memory simple broker shared.
