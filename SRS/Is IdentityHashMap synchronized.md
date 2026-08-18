<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/IdentityHashMap #Java/Collections/Concurrency #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump: **no.** Wrap at creation:

```java
Map m = Collections.synchronizedMap(new IdentityHashMap(...));
```

Same dump for `HashMap`.

> [!warning] Unverified traps from the dump
> - External wrap is not `ConcurrentHashMap` semantics.
> - `==` keys do not make the table thread-safe.
