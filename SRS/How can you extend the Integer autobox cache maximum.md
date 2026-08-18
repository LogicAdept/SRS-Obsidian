<!--
reps: 0
priority: 0
-->
#Java/Language/Wrappers #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps: Java caches `Integer` objects for `-128` to `127` inclusive via `Integer.valueOf`. The range can be extended with the JVM flag `-XX:AutoBoxCacheMax`, but relying on identity (`==`) after changing the flag is called fragile.

The cache is an optimisation inside `valueOf`. Values outside the configured range still allocate new objects.

> [!warning] Unverified traps from the dump
> - Default high bound is 127; dumps say the flag raises the maximum, not the lower bound of `-128`.
> - Do not write production logic that depends on `==` staying true after a cache-size change.
