<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebSocket #Messaging #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

`enableSimpleBroker` is an in-memory broker in the app JVM: subscriptions and fan-out for `/topic` and `/queue`. Fine for one instance.

Production dumps: `enableStompBrokerRelay("/topic")` toward RabbitMQ or ActiveMQ (`setRelayHost`, port 61613, login). The relay forwards STOMP; the external broker does cross-node fan-out, durable subscriptions, acks.

> [!warning] Unverified traps from the dump
> - Two Boot instances with only a simple broker do not share subscriptions.

