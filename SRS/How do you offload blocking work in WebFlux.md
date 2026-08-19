<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebFlux #Java/Library/Reactor #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

`Mono.fromCallable(() -> slowDbCall()).subscribeOn(Schedulers.boundedElastic())` so I/O does not occupy the event loop.

`Schedulers.boundedElastic()` wraps blocking I/O (legacy JDBC, file I/O) in a pool that grows but is capped.

`subscribeOn` sets the scheduler for the source; first `subscribeOn` wins. `publishOn` switches threads downstream.

> [!warning] Unverified traps from the dump
> - Offloading is a workaround; dumps prefer reactive drivers. Unbounded blocking still exhausts `boundedElastic`.

