<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebFlux #Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

`@RestController` method returns `Mono` (example `Mono.just("Hello, Reactive User!")`).

`@GetMapping("/mono")` → `Mono<String>`; `@GetMapping("/flux")` → `Flux.just(...)`.

That is the annotated model; functional `RouterFunction` is the other dump path.

> [!warning] Unverified traps from the dump
> - Returning `Mono.just` after a `.block()` inside the method is the anti-pattern other dumps call out.
> - The framework must subscribe; “nothing happens until subscribe” still applies if you drop the publisher.

