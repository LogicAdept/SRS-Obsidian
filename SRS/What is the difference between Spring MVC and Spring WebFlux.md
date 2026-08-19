<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebFlux #Java/Spring/Framework/WebMvc #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

MVC is synchronous/blocking, Servlet API, one thread per request, good for traditional apps. WebFlux is asynchronous/non-blocking, Project Reactor, event-loop, aimed at high concurrency. Both still use `@Controller` / `@RestController`.

MVC is thread-per-request on Tomcat; WebFlux is non-blocking on Netty with a small pool and `Mono`/`Flux`. Pick WebFlux for heavy traffic or streaming.

Spring MVC async I/O toward the client is still blocking; WebFlux is not. Processing the request body is blocking in MVC async and non-blocking in WebFlux. WebFlux also lists Netty and Undertow among servers.

> [!warning] Unverified traps from the dump
> - Spring Boot auto-config dumps say you will not run both MVC and WebFlux from classpath; MVC cannot run on Netty.

