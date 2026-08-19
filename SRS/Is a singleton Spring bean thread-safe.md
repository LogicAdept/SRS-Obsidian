<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC/Scopes #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

**No.** The default singleton is one shared instance per container. Mutable instance fields are visible to every request thread. Concurrent writes need synchronization, immutability, or no shared state.

Dumps: keep service beans **stateless**; if they must hold state, use immutable state, `ThreadLocal`, or a narrower scope (`prototype` / `request` / `session`). Read-only shared fields are the safe case.

Changing scope to `request`/`prototype`/`session` is claimed to make the bean “thread-safe” at the cost of more instances.

> [!warning] Unverified traps from the dump
> - “Spring beans are thread-safe because they are singletons” is the popular lie.
> - `request` scope is not a substitute for designing a stateless service; it only isolates HTTP-request state.
