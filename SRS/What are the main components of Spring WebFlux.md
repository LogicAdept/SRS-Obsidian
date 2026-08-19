<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebFlux #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Two main components — `RouterFunction` maps incoming requests to the matching `HandlerFunction`; the handler returns the response.

Other dumps still list annotated `@RestController` methods, `WebClient`, Netty / Reactor, and `Mono`/`Flux` as the types you actually return.

> [!warning] Unverified traps from the dump
> - Do not treat “only router + handler” as a complete module map; it is one dump’s functional-style answer.

