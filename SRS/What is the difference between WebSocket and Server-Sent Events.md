<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebSocket #Java/Spring/Framework/WebFlux #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

WebSocket: full duplex, client and server both send on one connection. SSE (WebFlux dump): server-to-client stream (`TEXT_EVENT_STREAM`, `Flux.interval`). HTTP dumps: REST is client-initiated, half-duplex, new TCP per request.

Use WebSocket when the client must push as often as the server; SSE when the server only streams down.

> [!warning] Unverified traps from the dump
> - SSE is server-to-client only; WebSocket is duplex. Do not treat an SSE Flux as a drop-in WebSocket.

