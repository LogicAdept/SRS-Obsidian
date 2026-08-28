<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebSocket #SRS

# What is `SimpUserRegistry`?

> [!abstract] Short answer
> **`SimpUserRegistry`** (Framework 4.2) is the API for **who is connected** over STOMP: **`getUser(name)`**, **`getUsers()`** (snapshot copy), **`getUserCount()`**, **`findSubscriptions(matcher)`**. Each **`SimpUser`** has a unique name, sessions, and optional `Principal`. Default implementation **`DefaultSimpUserRegistry`** tracks **`AbstractSubProtocolEvent`s** (connect/subscribe/disconnect). It is **not** `WebSocketSession.getId()` and **not** a substitute for `convertAndSendToUser`.

## Registry of users, not a send API

`getUser` returns **`null`** if that name is not connected **on this registry**. `getUsers()` will not update after you hold the set. Implementations: **`DefaultSimpUserRegistry`** (local events) and **`MultiServerUserRegistry`** (local plus remote snapshots via **`UserRegistryMessageHandler`** broadcasts — `setUserRegistryBroadcast` on the relay). Cross-node: [[How do you scale Spring WebSocket across instances]]. Sending: [[How do you send a message to one user with Spring WebSocket]], [[What is SimpMessagingTemplate]]. User dest rewrite: [[What is the SendToUser annotation]]. Session id vs user: [[What is WebSocketSession]].

```java
SimpUser user = simpUserRegistry.getUser("alice");
if (user != null && user.hasSessions()) {
	Set<SimpSession> sessions = user.getSessions();
}
Set<SimpSubscription> matches = simpUserRegistry.findSubscriptions(
		subscription -> subscription.getDestination().equals("/user/queue/alerts"));
```

**Listing 1.** Conceptual lookup. Presence here does not send a MESSAGE frame; use the template. `SimpUser.getPrincipal()` may be missing for a user known only through a **remote** registry.

Names come from the handshake **Principal**. Anonymous sockets are not looked up as `"alice"`. Events: `SessionConnectEvent` / `SessionConnectedEvent` / `SessionDisconnectEvent` (disconnect can fire **more than once** — listeners must be idempotent).

```d2
direction: down
ev: "CONNECT / SUBSCRIBE / DISCONNECT events" {
  width: 300
  height: 40
  style.fill: "#e3f2fd"
}
reg: "SimpUserRegistry" {
  width: 220
  height: 40
  style.fill: "#fff3e0"
}
lookup: "getUser / findSubscriptions" {
  width: 260
  height: 40
  style.fill: "#e8f5e9"
}

ev -> reg
reg -> lookup
```

**Fig. 1.** Multi-server setups wrap this in `MultiServerUserRegistry` and gossip over the broker.

> [!warning]Registry is not delivery
> `getUser("alice") != null` does not mean a later `convertAndSendToUser("alice", …)` cannot fail (relay down, user left, other instance without broadcast). `WebSocketSession.getId()` is a connection id, not `SimpUser.getName()`. `getUsers()` is a **copy**.

> [!tip] Interview answer
> **`SimpUserRegistry` lists connected STOMP users and their sessions/subscriptions.** Default is event-driven in-process; cluster with `MultiServerUserRegistry` and registry broadcast. Look up users here; send with `SimpMessagingTemplate.convertAndSendToUser`. No Principal means no named user in the registry.
