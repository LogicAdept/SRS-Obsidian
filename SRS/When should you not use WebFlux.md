<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebFlux #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Skip WebFlux for CPU-bound work; blocking libraries with no reactive alternative (JDBC, sync SDKs); team without reactive experience; need full JPA/Hibernate; simple CRUD with moderate traffic; Boot 3.2+ virtual threads covering the same concurrency more simply.

Migration dumps add: replace JDBC with R2DBC, rewrite to `Mono`/`Flux`, manage backpressure and debug pipelines, ensure downstream I/O is non-blocking.

> [!warning] Unverified traps from the dump
> - Virtual threads on MVC is a different coexistence question, not “two stacks on one Boot classpath”.

