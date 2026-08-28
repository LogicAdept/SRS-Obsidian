<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebSocket #Messaging #SRS

# What is STOMP in Spring WebSocket?

> [!abstract] Short answer
> **STOMP** (Simple Text Oriented Messaging Protocol) is a **frame-based messaging sub-protocol** Spring runs **on top of WebSocket** (or TCP). Raw WebSocket has **no destinations, subscriptions, or SEND/SUBSCRIBE**. STOMP adds **COMMAND + headers + body** (`SEND`, `SUBSCRIBE`, `MESSAGE`, …) and a **`destination`** header. Spring’s app then acts as the STOMP broker: route `/app` to **`@MessageMapping`**, or `/topic`/`/queue` to a **simple broker** or **STOMP broker relay**.

## Transport vs messaging

RFC 6455 frames are opaque. Client and server may negotiate a sub-protocol with **`Sec-WebSocket-Protocol`**. STOMP was built so scripting clients could talk to brokers; payloads may be text or binary even though the framing is text-oriented. A server **must not** send unsolicited `MESSAGE` frames — each one matches a client `SUBSCRIBE` `id`. Destination meaning is **opaque in the spec**; `/topic/…` (pub-sub) vs `/queue/…` (one consumer) is a **common convention**.

Enablement: **`@EnableWebSocketMessageBroker`** ([[What is the EnableWebSocketMessageBroker annotation]]). Config: [[How do you configure a STOMP broker in Spring]]. Prefixes: [[What is the difference between the app prefix and topic prefix]]. Brokers: [[What is a simple broker versus a STOMP broker relay]]. Raw pipe: [[What is WebSocket]], [[What is TextWebSocketHandler]], [[What is the difference between EnableWebSocket and EnableWebSocketMessageBroker]].

```
SEND
destination:/app/greeting
content-type:text/plain

hello^@
```

**Listing 1.** Conceptual STOMP frame (body ends with NUL). Spring strips `/app` and maps `/greeting` to `@MessageMapping`. Browser clients typically use a STOMP JS library over the handshake URL from `registerStompEndpoints`.

```d2
direction: down
ws: "WebSocket (frames)" {
  width: 240
  height: 40
  style.fill: "#e3f2fd"
}
stomp: "STOMP SEND / SUBSCRIBE / MESSAGE" {
  width: 300
  height: 40
  style.fill: "#fff3e0"
}
app: "/app → @MessageMapping" {
  width: 240
  height: 40
  style.fill: "#e8f5e9"
}
broker: "/topic /queue → broker" {
  width: 260
  height: 40
  style.fill: "#fce4ec"
}

ws -> stomp
stomp -> app
stomp -> broker
```

**Fig. 1.** Handshake URL is not a destination. Destinations live in STOMP headers after the socket is up.

> [!warning]STOMP is not `@EnableWebSocket`
> Without STOMP you still have **`TextWebSocketHandler`** and raw frames. That is a **different** annotation and configurer. Putting STOMP JS on a raw `/echo` handler will not create `/topic` subscriptions.

> [!tip] Interview answer
> **STOMP is the messaging sub-protocol Spring puts on WebSocket: destinations, SEND/SUBSCRIBE, a broker.** `/app` hits controllers; `/topic`/`/queue` hit the simple broker or an external relay. Raw WebSocket has none of that. Login/passcode on the JS CONNECT are ignored — identity is HTTP/session, not those headers.
