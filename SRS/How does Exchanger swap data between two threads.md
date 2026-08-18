<!--
reps: 0
priority: 0
-->
#Java/Concurrency #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump: `Exchanger<V>` is for **two threads to swap data at a rendezvous**. It is generic in the payload type.

A thread that calls `exchange(x)` **blocks** until the other thread calls `exchange(y)`. Then each returns the **other’s** argument. **`null` is allowed** — one-way send, or a pure sync point with no payload.

Dump story: two trucks meet at a crossroads and swap parcels:

```java
private static final Exchanger<String> EXCHANGER = new Exchanger<>();
// each truck
parcels[1] = EXCHANGER.exchange(parcels[1]);
```

> [!warning] Unverified traps from the dump
> - Exactly **a pair** of threads; a third caller is not part of this story.
> - `null` exchange is a dump feature, not “no rendezvous.”
