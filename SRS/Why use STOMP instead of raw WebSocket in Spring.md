<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebSocket #Messaging #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Raw sockets send text or binary with no destination model. STOMP adds pub/sub destinations, subscriptions, and typed commands so `@MessageMapping` can route like `@RequestMapping` for HTTP.

Dumps: without STOMP you have no broker prefixes, no `@SendTo`, no `SimpMessagingTemplate.convertAndSend` semantics.

> [!warning] Unverified traps from the dump
> - STOMP is not required for a simple echo handler; it is required for the message-broker stack.

