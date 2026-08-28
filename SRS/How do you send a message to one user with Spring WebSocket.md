<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebSocket #SRS

# How do you send a message to one user with Spring WebSocket?

> [!abstract] Short answer
> Use **user destinations**. The client **SUBSCRIBE `/user/queue/position-updates`**. The server sends with **`@SendToUser("/queue/position-updates")`** or **`simpMessagingTemplate.convertAndSendToUser(username, "/queue/position-updates", payload)`**. `UserDestinationMessageHandler` turns that into a **per-session** queue. **`convertAndSend("/topic/…")` is not private**, even if the JSON contains a user id.

## Subscribe generic `/user/…`, send by name

`convertAndSendToUser` expects the **authenticated WebSocket user name** (Principal from the handshake). If the session is **not** authenticated, you may pass the **session id** as the “user” **and** set the **`sessionId` header** on an overload that takes headers. Unresolved users (other app instance) need **`userDestinationBroadcast`**. Set **application and broker prefixes** so `/user` is not handled as a normal broker dest. Annotation: [[What is the SendToUser annotation]]. Template: [[What is SimpMessagingTemplate]]. Who is connected: [[What is SimpUserRegistry]]. Scale: [[How do you scale Spring WebSocket across instances]]. Do not use [[What is the SendTo annotation]] for privacy.

```java
@Service
public class TradeServiceImpl {

	private final SimpMessagingTemplate messagingTemplate;

	public TradeServiceImpl(SimpMessagingTemplate messagingTemplate) {
		this.messagingTemplate = messagingTemplate;
	}

	public void afterTradeExecuted(Trade trade) {
		this.messagingTemplate.convertAndSendToUser(
				trade.getUserName(), "/queue/position-updates", trade.getResult());
	}
}
```

**Listing 1.** Official sending-from-a-service shape. Bean name **`brokerMessagingTemplate`** if you must `@Qualifier`. Client subscribe destination is **`/user` + `/queue/position-updates`**.

External brokers: use destinations the broker can **auto-delete** when the session ends (Rabbit example: `/user/exchange/amq.direct/…`). `@SendToUser(broadcast = false)` limits to the **calling** session when the user has several tabs.

```d2
direction: down
client: "SUBSCRIBE /user/queue/…" {
  width: 260
  height: 40
  style.fill: "#e3f2fd"
}
send: "convertAndSendToUser(name, /queue/…)" {
  width: 300
  height: 40
  style.fill: "#fff3e0"
}
uniq: "unique /queue/…-user{session}" {
  width: 280
  height: 40
  style.fill: "#e8f5e9"
}

client -> uniq
send -> uniq
```

**Fig. 1.** Lookup is by user name (or session id), not by a field inside the payload.

> [!warning]No Principal means no named user
> `convertAndSendToUser("alice", "/queue/private", body)` delivers only if a session is registered as **alice**. A missing Principal does not throw in the service method; the destination stays **unresolved**. Putting `"alice"` in JSON and `convertAndSend("/topic/private")` still broadcasts.

> [!tip] Interview answer
> **One user: client subscribes to `/user/queue/…`; server uses `@SendToUser` or `convertAndSendToUser(username, "/queue/…", payload)`.** Spring rewrites to a unique queue. `/topic` is public. You need a handshake Principal (or session id + header). Multi-node needs user-destination broadcast.
