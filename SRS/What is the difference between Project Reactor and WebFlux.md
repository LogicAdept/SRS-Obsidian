<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebFlux #Java/Library/Reactor #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Project Reactor is the foundational library (`Mono`, `Flux`) for non-blocking reactive Java. WebFlux is the Spring *web* framework that uses Reactor for high-concurrency asynchronous HTTP. Reactor is the engine; WebFlux is the framework implementing it for the web.

WebFlux in Spring Framework 5 uses Reactor as its async foundation; `Mono`/`Flux` implement Reactive Streams `Publisher`.

> [!warning] Unverified traps from the dump
> - Mono vs Flux cardinality belongs on `#Java/Library/Reactor/Mono` and `Flux` (those cues already exist).
> - You can use Reactor without WebFlux; dumps still introduce both together in WebFlux interviews.

