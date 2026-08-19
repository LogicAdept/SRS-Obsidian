<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebSocket #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Simple broker heartbeat: `enableSimpleBroker("/topic").setHeartbeatValue(new long[]{10000, 20000})` — server ping every 10s, expect client every 20s. No response → close the session.

Idle load-balancer timeouts still kill the connection if not raised.

> [!warning] Unverified traps from the dump
> - Heartbeats are not a substitute for a relay broker when you have many nodes.

