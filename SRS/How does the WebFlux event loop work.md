<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebFlux #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

MVC uses one thread per request and a large Tomcat pool, often blocked on I/O. WebFlux uses a small fixed event-loop pool (Netty); requests are processed asynchronously.

Netty boss group accepts connections; worker group (default CPU cores) polls `epoll`/`kqueue`. Register I/O, move on, callback when ready. 4–8 threads for 10,000+ connections. No thread-per-request.

> [!warning] Unverified traps from the dump
> - Never block the event-loop thread (`Thread.sleep`, JDBC, `.block()`) — dumps call that the number-one WebFlux outage.

