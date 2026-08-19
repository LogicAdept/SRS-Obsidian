<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Cache #Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

`@CacheEvict` removes entries so callers do not keep stale data. Configure a key to drop one entry, or `allEntries = true` to clear the whole named cache. Example: `@CacheEvict(value = "books", key = "#isbn")` on delete; `@CacheEvict(value = "books", allEntries = true)` to wipe the region.

`beforeInvocation` can evict before the method runs so a failed method still clears the cache.

> [!warning] Unverified traps from the dump
> - Evict after a failed update can leave the cache empty while the DB still has the old row — dumps still list `beforeInvocation` as the “evict first” knob.
> - `allEntries = true` is a blunt cluster-unfriendly flush if every node has a local map.

