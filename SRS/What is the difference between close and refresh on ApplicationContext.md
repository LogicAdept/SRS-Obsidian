<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

`close()` shuts the container down: destroy callbacks (`@PreDestroy`, `DisposableBean`, `destroy-method`), release resources. Typical at the end of a standalone `main`.

`refresh()` reloads the context after it has already been initialized (dumps: often mentioned for web apps that need a manual refresh). It is not a substitute for `registerShutdownHook()`.

> [!warning] Unverified traps from the dump
> - Calling `refresh()` on a context that is not designed for it can recreate singletons and surprise listeners.
> - Forgetting `close()` in a non-Boot process skips destroy callbacks (related to shutdown-hook).
