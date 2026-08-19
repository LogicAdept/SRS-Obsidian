<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

For a non-web `ApplicationContext`, dumps list two ways, both on `AbstractApplicationContext`:

1. `registerShutdownHook()` — preferred; JVM shutdown runs destroy callbacks (`@PreDestroy`, `DisposableBean`).
2. Call `close()` yourself.

Spring Boot registers a shutdown hook for you.

Context close is what runs singleton destroy callbacks. Prototype beans are not tracked for destruction.

> [!warning] Unverified traps from the dump
> - Forgetting the shutdown hook in a standalone (non-Boot) process skips `@PreDestroy`.
> - Web apps typically close with the servlet context; Boot still registers the hook.
