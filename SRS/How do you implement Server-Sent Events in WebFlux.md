<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebFlux #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

SSE with `Flux` and `produces = MediaType.TEXT_EVENT_STREAM_VALUE`. Example: `Flux.interval(Duration.ofSeconds(1)).map(i -> "Stock Update #" + i)` on `@GetMapping("/stocks")`.

streaming/SSE is a reason to keep WebFlux even when virtual threads exist; `WebTestClient` can assert SSE by accepting `TEXT_EVENT_STREAM`.

> [!warning] Unverified traps from the dump
> - This is not WebSocket (`#Java/Spring/Framework/WebSocket`).
> - An infinite `Flux` without backpressure/cancel is the overload scenario another dump solves with `limitRate` / `request(n)`.

