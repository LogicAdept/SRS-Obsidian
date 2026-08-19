<!--
reps: 0
priority: 0
-->
#Java/Spring/Session #Java/Spring/Data/Redis #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Spring Session replaces the servlet container `HttpSession` with a session stored in Redis (`spring-session-data-redis`, `spring.session.store-type=redis`, or `@EnableRedisHttpSession`). A filter (`springSessionRepositoryFilter`) loads/saves the session by id (cookie).

Any app instance can serve any request by reading Redis. That removes sticky sessions on the load balancer and lets new instances during a rolling deploy see existing sessions.

Dumps also mention cookie name / SameSite / secure cookie via `CookieSerializer`.

> [!warning] Unverified traps from the dump
> - Session objects still need a serializer; JDK serialization has the same problems as RedisTemplate defaults.
> - `flush-mode` `on-save` vs `immediate` changes when Redis is written.
