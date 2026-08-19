<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebSocket #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

API object for one upgraded connection in the handler model: send messages, inspect the session. Handshake dumps: after `101 Switching Protocols`, Spring keeps the session; `DefaultHandshakeHandler` is named as the upgrade processor.

> [!warning] Unverified traps from the dump
> - STOMP user mapping uses session ids and `SimpUserRegistry`; do not assume `WebSocketSession.getId()` equals the STOMP user name.

