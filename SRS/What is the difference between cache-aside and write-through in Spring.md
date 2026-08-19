<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Cache #Caching #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Cache-aside: app checks cache, on miss loads DB then puts; writes update DB then evict (`@CacheEvict`). Simple, briefly inconsistent after writes. Write-through: every write updates cache and DB (`@CachePut`); cache stays current, writes slower, may cache unread data. Dumps: cache-aside is more common; write-through when read-after-write consistency matters.

`@Cacheable` is the read/lazy side; `@CachePut` is the write-through-shaped annotation.

> [!warning] Unverified traps from the dump
> - Spring annotations do not magically implement a full cache-aside library; you still choose evict vs put.

