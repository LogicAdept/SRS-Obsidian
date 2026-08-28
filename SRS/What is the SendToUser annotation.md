<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebSocket #Java/Annotations #SRS

# What is the `@SendToUser` annotation?

> [!abstract] Short answer
> **`@SendToUser`** (Framework 4.0, `org.springframework.messaging.simp.annotation`) sends the method return value to **user destinations**: Spring **prepends `/user/{username}`** (name from the **input message headers**). The client subscribes to a generic **`/user/queue/...`**; `UserDestinationMessageHandler` rewrites that to a **session-unique** queue. Default **`broadcast = true`**: all of that user’s sessions. **`broadcast = false`**: only the session that sent the handled message.

## User prefix, then unique queue

Example: `@SendToUser("/queue/position-updates")` plus a client SUBSCRIBE **`/user/queue/position-updates`**. Internally that becomes something like `/queue/position-updates-user123`. Configure **`/app` and broker prefixes** so the **simple broker does not eat `/user`**. Unauthenticated session: `@SendToUser` behaves like **`broadcast = false`** (that session only). Combine with `@SendTo` on the same method. Class-level default; method-level overrides. How-to: [[How do you send a message to one user with Spring WebSocket]]. Public broadcast: [[What is the SendTo annotation]]. Template: [[What is SimpMessagingTemplate]]. Registry: [[What is SimpUserRegistry]]. Mapping: [[What is the MessageMapping annotation]].

```java
@Controller
public class PortfolioController {

	@MessageMapping("/trade")
	@SendToUser("/queue/position-updates")
	public TradeResult executeTrade(Trade trade, Principal principal) {
		return tradeResult;
	}

	@MessageExceptionHandler
	@SendToUser(destinations = "/queue/errors", broadcast = false)
	public ApplicationError handleException(MyBusinessException ex) {
		return appError;
	}
}
```

**Listing 1.** Conceptual: trade result to all of the user’s sessions; errors only to the session that failed. If `destinations` is empty, a default is derived from the inbound destination.

```d2
direction: down
ann: "@SendToUser /queue/…" {
  width: 260
  height: 40
  style.fill: "#e3f2fd"
}
uh: "UserDestinationMessageHandler" {
  width: 280
  height: 40
  style.fill: "#fff3e0"
}
q: "session-unique /queue/…-user…" {
  width: 280
  height: 40
  style.fill: "#e8f5e9"
}

ann -> uh
uh -> q
```

**Fig. 1.** The client never subscribes to the rewritten unique name; it uses `/user/queue/…`.

> [!warning]Broadcast true hits every session of that user
> Two browser tabs as the same Principal both get the message unless `broadcast = false`. `@SendTo("/topic/...")` is **everyone on the topic**, not “the user in the payload.” Named `convertAndSendToUser("alice", …)` still needs **alice** to be the handshake Principal (or a session id + `sessionId` header).

> [!tip] Interview answer
> **`@SendToUser` replies on `/user/{name}/…`; the client subscribes to `/user/queue/…`.** Default broadcasts to all of that user’s sessions; `broadcast=false` is this socket only. Unauthenticated connections are treated as session-only. It is not `@SendTo("/topic")`.
