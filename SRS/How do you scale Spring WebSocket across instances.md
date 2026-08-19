<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebSocket #Messaging #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Replace the simple broker with `enableStompBrokerRelay` to RabbitMQ/ActiveMQ so nodes share destinations.

Load balancer: HTTP/1.1, forward `Upgrade` and `Connection`, long `proxy_read_timeout` (dumps: 3600s). Default 60s idle timeout kills the socket. Missing upgrade headers break the handshake.

> [!warning] Unverified traps from the dump
> - Sticky sessions help raw sockets; a shared STOMP broker is what dumps name for multi-node pub/sub.

