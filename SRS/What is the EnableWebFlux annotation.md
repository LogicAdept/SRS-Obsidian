<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebFlux #Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

`@EnableWebFlux` explicitly turns on the reactive web stack so you control routing and server settings and can bypass Boot’s default auto-configuration. Use it when you need custom behavior beyond `spring-boot-starter-webflux`.

`@Configuration` + `@EnableWebFlux` on a class that implements `WebFluxConfigurer`.

> [!warning] Unverified traps from the dump
> - On a typical Boot app the starter is enough; dumps present `@EnableWebFlux` as the “full control” knob, which can also disable Boot WebFlux auto-config — verify before copying that into a review answer.

