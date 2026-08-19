<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebFlux #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Reactor Netty is an asynchronous event-driven network framework. It provides non-blocking, backpressure-ready TCP, HTTP, and UDP clients and servers, based on Netty.

WebFlux defaults to Netty. Unlike Tomcat, Netty uses an event-loop and can manage thousands of connections with few threads. WebFlux supports Reactor Netty, Tomcat, Jetty, Undertow; Reactor Netty is the default.

> [!warning] Unverified traps from the dump
> - Reactor Netty is the default *server* (and WebClient connector) in dumps, not another name for Project Reactor.
> - Tomcat can still host WebFlux in those server lists; Boot’s default for `spring-boot-starter-webflux` is Netty.

