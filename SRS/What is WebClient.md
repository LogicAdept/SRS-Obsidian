<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebFlux #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

`WebClient` is WebFlux’s reactive HTTP client for non-blocking requests. `WebClient.create(baseUrl).get().uri("/data").retrieve().bodyToMono(String.class)`. It returns `Mono` or `Flux`, unlike blocking `RestTemplate`.

It handles reactive streams with backpressure, Java 8 lambdas, and both sync and async scenarios. The instance is thread-safe because it is immutable. Dumps also call it a higher-level functional API for HTTP that supports synchronous and asynchronous communication.

> [!warning] Unverified traps from the dump
> - Dumps still call RestTemplate deprecated since Spring 5, while other dumps say maintenance mode.
> - `.block()` on the resulting `Mono` is the blocking escape hatch dumps mention; they warn against it on the event loop.

