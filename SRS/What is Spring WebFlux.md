<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebFlux #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Spring WebFlux is Spring’s reactive-stack web framework, introduced as a parallel alternative to Spring MVC. Dumps say the whole stack is non-blocking so the model can scale, it supports backpressure, and it uses Project Reactor (`Mono` / `Flux`) as the async foundation.

It is part of Spring 5, supports fully non-blocking reactive streams, and uses Netty as the inbuilt server for reactive apps. Servers include Reactor Netty, Tomcat, Jetty, and Undertow, with Reactor Netty as the default. Dumps describe it as designed for asynchronous, non-blocking applications.

> [!warning] Unverified traps from the dump
> - WebFlux is not described as necessarily faster CRUD; one dump says it is better at scalability, hardware use, and latency, not raw speed.
> - Project Reactor is the engine; WebFlux is the web framework on top of it.

