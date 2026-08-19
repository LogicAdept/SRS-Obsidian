<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebSocket #Java/Spring/Security #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Base class in a Security dump for locking STOMP. Override `configureInbound` (`simpDestMatchers`, `anyMessage().authenticated()`) and `sameOriginDisabled()`. Used with `@EnableWebSocketMessageBroker`.

> [!warning] Unverified traps from the dump
> - Class name is legacy in some dumps; newer Security APIs may differ — treat as dump claim.

