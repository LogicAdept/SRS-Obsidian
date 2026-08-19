<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebFlux #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

`bodyToMono()` extracts the HTTP body into a `Mono`. `Mono.block()` then subscribes and waits for the response; `Mono.subscribe()` is the non-blocking path.

Used on `WebClient` `retrieve()` for a single JSON object.

> [!warning] Unverified traps from the dump
> - `bodyToFlux` is the collection/stream sibling on the same dump list.
> - Calling `block()` after `bodyToMono` on a Netty event-loop thread is the failure mode other dumps name (`IllegalStateException`).

