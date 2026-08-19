<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebSocket #Networking/Web/Protocols/WebSocket #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Client HTTP GET with `Upgrade: websocket`, `Connection: Upgrade`, `Sec-WebSocket-Key`. Server `101 Switching Protocols` and `Sec-WebSocket-Accept`. Then one TCP connection stays open for both directions.

Spring: `DefaultHandshakeHandler` validates and creates `WebSocketSession`. Initial connection is HTTP, then upgraded — same story as protocol dumps vs REST polling.

> [!warning] Unverified traps from the dump
> - Proxies that strip Upgrade never reach 101; SockJS is the dump workaround.

