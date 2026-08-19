<!--
reps: 0
priority: 0
-->
#Java/Concurrency/Synchronizers #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump: construct `CyclicBarrier(int parties, Runnable barrierAction)`. When **all** parties call `await()`, the action runs **before** the waiting threads are released. Then the barrier can be used again.

Ferry dump: barrier of 3 plus a `FerryBoat` runnable; each car `await()`s; when three have arrived, the ferry prints and the cars continue:

```java
private static final CyclicBarrier BARRIER = new CyclicBarrier(3, new FerryBoat());
BARRIER.await();
```

Dump: this is an alternative to `join()`, which only “collects” threads **after they have finished**.

> [!warning] Unverified traps from the dump
> - Action runs once per trip, then a **new cycle** starts (nine cars → three trips in the sample).
> - `await()` throws checked exceptions in the dump (`Exception` swallowed).
