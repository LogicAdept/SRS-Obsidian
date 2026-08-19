<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Cache #Java/Spring/Framework/AOP #Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump list: (1) self-invocation bypasses the proxy; (2) private method — AOP intercepts public methods; (3) void return — nothing to cache; (4) `condition` is false; (5) the method throws — result not cached; (6) `@EnableCaching` missing.

> [!warning] Unverified traps from the dump
> - Cache stampede and Redis serialization failures are different failure modes, not this “annotation silent” list.

