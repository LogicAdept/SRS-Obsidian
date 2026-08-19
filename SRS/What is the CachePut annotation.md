<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Cache #Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

`@CachePut` always runs the method and then writes the return value into the cache. Same options as `@Cacheable` (`value`, `key`, …). Dumps say use it to populate or refresh the cache, not to skip work.

Contrast: `@Cacheable` may skip the method on a hit.

> [!warning] Unverified traps from the dump
> - Never put `@Cacheable` on a method with required side effects — a hit skips the side effect. `@CachePut` is the write-through-shaped annotation in these dumps.

