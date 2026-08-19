<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebFlux #Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

`@Configuration` `@EnableWebFlux` class implementing `WebFluxConfigurer`, plus a `@SpringBootApplication` `main`.

`server.port` in `application.properties` still applies to Netty. For Netty backlog they show a `WebServerFactoryCustomizer<NettyReactiveWebServerFactory>` setting `ChannelOption.SO_BACKLOG`.

> [!warning] Unverified traps from the dump
> - Boot + `spring-boot-starter-webflux` is the usual path; the `@EnableWebFlux` example is the “architect wants full control” dump.

