<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebSocket #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

SockJS is a fallback when the browser or a proxy cannot complete a WebSocket upgrade. Server: `.withSockJS()` on `addEndpoint(...)`. It registers HTTP fallbacks (`/info`, XHR streaming, XHR polling).

Omit it and those clients hang with no useful error. Client libraries: `sockjs-client` plus a STOMP client.

> [!warning] Unverified traps from the dump
> - SockJS is not STOMP. You can have SockJS transport under STOMP, or raw WebSocket without SockJS.
> - Native `new WebSocket('ws://...')` will not hit SockJS fallback URLs.

