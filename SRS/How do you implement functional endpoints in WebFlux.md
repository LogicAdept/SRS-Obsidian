<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebFlux #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

`RouterFunction` bean — `route(GET("/hi"), req -> ServerResponse.ok().bodyValue("Hi, Functional World!"))`.

`route().GET(...)` style wiring to an `EmployeeService`. This is the non-annotation routing model next to `@RestController`.

> [!warning] Unverified traps from the dump
> - Fuller samples still return `Mono<ServerResponse>` from handlers; one dump uses `bodyValue` on `ServerResponse.ok()`.

