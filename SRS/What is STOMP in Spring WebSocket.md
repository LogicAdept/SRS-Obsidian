<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebSocket #Messaging #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Raw WebSocket is a bidirectional pipe with no routing, subscriptions, or message types. STOMP (Simple Text Oriented Messaging Protocol) is the sub-protocol dumps put on top: destinations like `/topic` and `/queue`, SEND/SUBSCRIBE frames, headers.

Spring wires STOMP through `@EnableWebSocketMessageBroker`. Clients talk destinations; the broker fans out. Think transport (WebSocket) vs messaging layer (STOMP).

> [!warning] Unverified traps from the dump
> - Without STOMP you still can use `TextWebSocketHandler` and raw frames — that is a different Spring programming model (`@EnableWebSocket`).

