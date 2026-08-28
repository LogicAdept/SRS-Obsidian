<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebSocket #SRS

# How do you keep a Spring WebSocket connection alive?

> [!abstract] Short answer
> Idle **proxies** and container **idle timeouts** close sockets that look dead. Spring’s answers are **heartbeats**, not a second broker. **Simple broker:** set a **`TaskScheduler`** and **`setHeartbeatValue`** (STOMP `heart-beat`). **Relay:** system TCP heartbeats default **10 s** send and receive. **SockJS:** server `h` frames every **25 s** unless STOMP heartbeats were negotiated (then SockJS beats are **off**). Heartbeats **do not** fan out across instances.

## STOMP beats, SockJS beats, container idle

STOMP 1.2: CONNECT/CONNECTED `heart-beat:cx,cy` — 0 means none; otherwise negotiated intervals use MAX of the two sides. Simple broker javadoc: heartbeat **`{serverWrite, clientWrite}`** milliseconds; **`0,0`** if no scheduler; setting **`setTaskScheduler`** also defaults to **`10000,10000`**. Official example: `{10000, 20000}` — server writes every 10 s, expects the client every 20 s. Inject the built-in scheduler with **`@Lazy`** to avoid a config cycle. Relay: **`setSystemHeartbeatSendInterval` / `ReceiveInterval`** (default 10000; 0 disables); lost broker TCP **reconnects every 5 s**. SockJS: [[What is SockJS]]. Broker choice: [[What is a simple broker versus a STOMP broker relay]]. Scale: [[How do you scale Spring WebSocket across instances]]. STOMP: [[What is STOMP in Spring WebSocket]].

```java
@Autowired
public void setMessageBrokerTaskScheduler(@Lazy TaskScheduler taskScheduler) {
	this.messageBrokerTaskScheduler = taskScheduler;
}

@Override
public void configureMessageBroker(MessageBrokerRegistry registry) {
	registry.enableSimpleBroker("/queue/", "/topic/")
			.setHeartbeatValue(new long[] {10000, 20000})
			.setTaskScheduler(this.messageBrokerTaskScheduler);
}
```

**Listing 1.** Conceptual: Framework 6.2 simple-broker heartbeat sample. Also consider Jetty **`setIdleTimeout(Duration.ofSeconds(600))`** on `JettyRequestUpgradeStrategy`, and **`setTimeToFirstMessage`** so a connected socket that never sends STOMP is closed.

`WebSocketStompClient` (server-as-client) needs a `TaskScheduler` for heartbeats (default 10 s write / 10 s read inactivity). SockJS task-scheduler stats appear on **`WebSocketMessageBrokerStats`**.

```d2
direction: down
idle: "idle proxy / container timeout" {
  width: 280
  height: 40
  style.fill: "#fce4ec"
}
stomp: "STOMP heart-beat" {
  width: 240
  height: 40
  style.fill: "#e3f2fd"
}
sock: "SockJS h frames (25s)" {
  width: 240
  height: 40
  style.fill: "#fff3e0"
}

stomp -> idle: "keeps TCP looking live"
sock -> idle: "if no STOMP beats"
```

**Fig. 1.** If STOMP negotiates heartbeats, SockJS heartbeats are disabled. Neither mechanism copies subscriptions to another app instance.

> [!warning]Beats are not a cluster bus
> `{10000, 20000}` will not deliver `/topic` messages from another JVM. That is **`enableStompBrokerRelay`**. Missing **`TaskScheduler`** leaves simple-broker heartbeats at **0,0**. A reverse proxy that still closes idle Upgrade connections will win unless **that** idle timeout is raised too.

> [!tip] Interview answer
> **Keep the socket alive with STOMP heartbeats (simple broker needs a TaskScheduler) or SockJS 25 s heartbeats, and do not let the proxy drop idle Upgrade connections.** Server/client intervals are the two-number `heart-beat` pair. Relay system connection uses 10 s by default. Heartbeats are health checks, not multi-node pub/sub.
