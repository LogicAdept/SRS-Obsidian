<!--
reps: 0
priority: 0
-->
#Networking/Web/Protocols/WebSocket #Java/Spring/Framework/WebSocket #SRS

# What is WebSocket?

> [!abstract] Short answer
> **WebSocket** is **RFC 6455**: a **full-duplex** message protocol on **one TCP connection**. The session **starts as HTTP** (`Upgrade: websocket`) and, after **`101 Switching Protocols`**, both sides send **frames** (text UTF-8, binary, or control) without a new HTTP request per message. URI schemes are **`ws`** (plain) and **`wss`** (TLS). It is **not** REST: one handshake URL, then an event-driven stream with **no built-in routing semantics**.

## Protocol, then Spring’s two stacks

RFC 6455 splits the connection into an **opening handshake** and **data transfer**. After a successful handshake, each side may send independently. A **message** is one or more **frames**. Spring’s Servlet stack maps that onto **`WebSocketHandler`** (raw API) or **STOMP** (sub-protocol negotiated with `Sec-WebSocket-Protocol`). Handshake details: [[How does the WebSocket handshake work in Spring]]. Raw handler: [[What is TextWebSocketHandler]]. Session: [[What is WebSocketSession]]. Sub-protocol: [[What is STOMP in Spring WebSocket]]. Enablement: [[What is the difference between EnableWebSocket and EnableWebSocketMessageBroker]].

HTTP/REST models **many URLs** and request-response. WebSocket usually has **one connect URL**; afterward every application message uses that TCP socket. The protocol does **not** define how to route a payload — client and server must agree (STOMP, or your own convention).

Spring’s “when to use it” bar is **low latency + high frequency + high volume**. News feeds that refresh every few minutes can stay on AJAX, HTTP streaming, or long polling. Collaboration, games, and trading sit closer to real-time. Restrictive **proxies** may drop `Upgrade` or idle long-lived sockets; that is why [[What is SockJS]] exists. A reverse proxy or cloud front door must be told to forward the upgrade.

```
GET /chat HTTP/1.1
Host: server.example.com
Upgrade: websocket
Connection: Upgrade
Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==
Sec-WebSocket-Version: 13
```

**Listing 1.** RFC 6455 client opening handshake (non-normative sample, `Origin` omitted). Server reply is **`101 Switching Protocols`** plus `Sec-WebSocket-Accept` (SHA-1 of the key concatenated with GUID `258EAFA5-E914-47DA-95CA-C5AB0DC85B11`, then Base64). Any status **other than 101** means the handshake failed and **HTTP semantics still apply**.

```d2
direction: down
http: "HTTP GET + Upgrade" {
  width: 240
  height: 40
  style.fill: "#e3f2fd"
}
sw: "101 Switching Protocols" {
  width: 240
  height: 40
  style.fill: "#fff3e0"
}
duplex: "one TCP socket, frames both ways" {
  width: 280
  height: 40
  style.fill: "#e8f5e9"
}

http -> sw
sw -> duplex
```

**Fig. 1.** After 101 the connection is no longer a sequence of HTTP request-response pairs.

> [!warning]Low-level transport has no application routing
> A raw `TextWebSocketHandler` sees **frames**, not destinations. `@MessageMapping` exists only on the **STOMP / message-broker** stack. Putting `spring-boot-starter-websocket` on the classpath does not pick a model.

> [!tip] Interview answer
> **WebSocket is RFC 6455: HTTP Upgrade to 101, then full-duplex frames on one TCP connection (`ws` / `wss`).** It is not REST and it does not define message meaning. In Spring you either implement `WebSocketHandler` or enable STOMP. Proxies that strip `Upgrade` need SockJS or a correctly configured front end.
