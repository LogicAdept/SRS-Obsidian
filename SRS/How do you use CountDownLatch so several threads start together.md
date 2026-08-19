<!--
reps: 0
priority: 0
-->
#Java/Concurrency/Synchronizers #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump race: `CountDownLatch(8)` — five cars each `countDown()` when they reach the line, then `await()`. The starter thread `countDown()`s three more times (“On your marks”, “Get set”, “Go”). When the count hits **0**, **all** waiters unblock **together**.

```java
private static final CountDownLatch START = new CountDownLatch(8);

// car
START.countDown();
START.await();

// starter
START.countDown(); // На старт!
START.countDown(); // Внимание!
START.countDown(); // Марш!
```

Dump also: any number of threads can wait until **N operations in other threads** finish. Life example: a tour group does not start until enough people arrive.

> [!warning] Unverified traps from the dump
> - One latch, **two roles**: cars decrement-and-wait; starter only decrements.
> - After zero the latch is **spent** (contrast CyclicBarrier reuse in the same article).
