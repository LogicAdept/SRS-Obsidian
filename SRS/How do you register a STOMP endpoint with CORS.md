<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebSocket #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

`registry.addEndpoint("/ws").setAllowedOrigins("*").withSockJS()` in dumps. Production: restrict to trusted origins, not `*`.

> [!warning] Unverified traps from the dump
> - Allowed origins on the handshake are not Spring Security authorization of `/app` destinations.

