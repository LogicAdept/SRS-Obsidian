<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebFlux #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

`.block()` on a Netty event-loop thread throws `IllegalStateException` (“block()/blockFirst()/blockLast() are blocking, which is not supported in thread reactor-http-nio-X”). Can deadlock if the waited signal can only arrive on that same thread. Occupies one of the few loop threads. Only acceptable in tests or at the application boundary (main, `CommandLineRunner`).

One dump still shows `Mono.block()` as how you wait for the body — that is the blocking client usage, not a WebFlux controller on Netty.

> [!warning] Unverified traps from the dump
> - `.block()` on `WebClient`/`Mono` is a dump-listed escape hatch for tests or process boundaries, not for Netty request threads.

