<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebFlux #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

(1) blocking in the chain (JDBC, `Thread.sleep`, synchronized); (2) `.block()` on the event loop; (3) unbounded buffers → OOM; (4) no `limitRate()` on large DB results; (5) forgetting to subscribe so nothing runs; (6) `Hooks.onOperatorDebug()` in production; (7) shared mutable state on the loop; (8) not propagating context for tracing/security.

Golden rule there: never block an event-loop thread — one `sleep` blocks every request on that worker.

> [!warning] Unverified traps from the dump
> - “Nothing happens until subscribe” is a Reactor slogan that dumps apply to dropped repository `save` calls in WebFlux services.

