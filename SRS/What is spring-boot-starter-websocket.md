<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebSocket #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Boot starter dumps add for WebSocket. Brings the web-socket stack so `@EnableWebSocket` or the STOMP config can run without listing `spring-websocket` by hand.

> [!warning] Unverified traps from the dump
> - The starter does not choose STOMP vs raw handlers; your `@Enable*` config does.

