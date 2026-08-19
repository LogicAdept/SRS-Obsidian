<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebFlux #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

`RouterFunction` is the functional alternative to `@RequestMapping` / `@Controller`. It routes requests to handler functions.

`@Bean RouterFunction<ServerResponse>` with `route(GET("/hi"), req -> ServerResponse.ok().bodyValue(...))` when the manager wants routing without annotations.

`RouterFunction` plus `WebFluxConfigurer` under `@EnableWebFlux` as the Java config shape.

> [!warning] Unverified traps from the dump
> - One dump claims the two *main* WebFlux components are only `RouterFunction` and `HandlerFunction` — annotated controllers still appear in every other dump.

