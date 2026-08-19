<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebFlux #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

like `bodyToMono`, but for a collection resource as `Flux`. Example: `client.get().uri("/stocks").retrieve().bodyToFlux(Stock.class)` then `subscribe`.

> [!warning] Unverified traps from the dump
> - Use `bodyToMono` for one object; `bodyToFlux` for many. A `Mono<List<T>>` in other dumps is one list at once, not a streamed `Flux`.

