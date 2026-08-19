<!--
reps: 0
priority: 0
-->
#Java/Spring/Data/Redis #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump checklist:

1. Configure connection timeouts and command timeouts.
2. Use circuit breakers (Resilience4j) to fail fast.
3. Fall through to the database on cache miss (degrade).
4. Configure Lettuce reconnection with exponential backoff.
5. Monitor connection pool metrics.
6. For sessions, configure a fallback to in-memory sessions.
> [!warning] Unverified traps from the dump
> - Cache-aside fallthrough is a degradation path, not a substitute for fixing Redis.
> - Lettuce is the dump's default client for reconnect behavior.
