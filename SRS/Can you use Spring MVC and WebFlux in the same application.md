<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebFlux #Java/Spring/Framework/WebMvc #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Spring Boot auto-configures either MVC or WebFlux from the classpath, not both. Spring MVC cannot run on Netty. MVC is blocking and WebFlux is non-blocking, so they serve different purposes and should not be mixed.

No — because Spring MVC cannot run on Netty, in the short form of the same dump.

> [!warning] Unverified traps from the dump
> - Using `WebClient` from an MVC app is a different claim than Boot auto-configuring both web stacks.
> - Virtual threads on MVC is a different coexistence story than mixing MVC and WebFlux servers.

