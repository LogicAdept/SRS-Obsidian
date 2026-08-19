<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Cache #Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

`sync = true` on `@Cacheable`: only one thread computes a missing key; others wait. Dump prevention for in-process cache stampede.

> [!warning] Unverified traps from the dump
> - Not a distributed lock. Combine with Redis locking if several app instances miss together.

