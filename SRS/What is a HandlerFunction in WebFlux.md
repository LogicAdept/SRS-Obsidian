<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebFlux #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

The two main WebFlux components in that dump are `RouterFunction` (maps the incoming request) and `HandlerFunction` (handles the request and returns a response).

> [!warning] Unverified traps from the dump
> - Annotated `@RestController` methods returning `Mono`/`Flux` are the other programming model in the same dumps.

