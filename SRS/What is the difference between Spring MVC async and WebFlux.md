<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebFlux #Java/Spring/Framework/WebMvc #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Spring MVC `@Async` / async I/O toward the client is still blocking; WebFlux is not. Request-body processing is blocking in Spring Async and non-blocking in WebFlux. WebFlux supports more servers such as Netty and Undertow.

> [!warning] Unverified traps from the dump
> - `@Async` on MVC is not the same as Servlet 3 async request processing; the dump lumps “Spring Async” against WebFlux.
> - This is not the virtual-threads comparison.

