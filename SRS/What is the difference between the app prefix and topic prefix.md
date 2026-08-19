<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebSocket #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

`/app` is for application handlers: client sends `/app/chat.send`, Spring strips `/app`, matches `@MessageMapping("/chat.send")`.

`/topic` and `/queue` go to the broker for subscriptions and broadcast. Return `@SendTo("/topic/public")` is broker fan-out, not another controller call.

`/topic` vs `/queue` is convention (pub-sub vs point-to-point) on the simple broker; an external broker may treat prefixes differently.

> [!warning] Unverified traps from the dump
> - Subscribing to an /app destination will not receive traffic published with @SendTo to /topic.

