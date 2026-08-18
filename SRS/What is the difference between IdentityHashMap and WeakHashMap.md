<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/IdentityHashMap #Java/Collections/Map/WeakHashMap #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

FAQ / comparison dump:

| | IdentityHashMap | WeakHashMap |
|---|---|---|
| Key comparison | `==` | `equals()` |
| Memory | not GC-sensitive | keys can be collected |
| Key refs | strong | weak |
| Typical job | framework internals | cache / listeners |
| Hashing | `System.identityHashCode` | `key.hashCode()` |

FAQ: **do not use IdentityHashMap as a cache**; it does not drop unused keys. Both allow **null keys**. Overriding `equals` on an IdentityHashMap key **does nothing**.

> [!warning] Unverified traps from the dump
> - Identity vs weak are orthogonal: one is `==`, the other is GC of keys.
> - “Use WeakHashMap for caches” in the same FAQ is still not an LRU `LinkedHashMap`.
