<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebFlux #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

`spring-webflux` is not necessarily faster; it is better at scalability, efficient hardware use, and latency.

Event-loop, few threads, non-blocking I/O, backpressure; suited to high-concurrency streaming / real-time APIs. Thousands of concurrent connections on few event-loop threads; constraint shifts from thread-pool size to memory and CPU.

> [!warning] Unverified traps from the dump
> - WebFlux is not “faster CRUD” in these dumps.
> - Same dumps list a steep learning curve and blocking JDBC as reasons not to adopt it.

