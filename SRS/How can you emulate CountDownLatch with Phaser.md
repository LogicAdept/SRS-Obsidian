<!--
reps: 0
priority: 0
-->
#Java/Concurrency #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump: Phaser can **reproduce CountDownLatch**. Race start: `new Phaser(8)`; each car `arriveAndDeregister()` then `awaitAdvance(0)`; the starter thread also `arriveAndDeregister()` for “On your marks / Get set / Go”:

```java
private static final Phaser START = new Phaser(8);

// car at the line
START.arriveAndDeregister();
START.awaitAdvance(0);

// starter commands
START.arriveAndDeregister(); // "На старт!"
START.arriveAndDeregister(); // "Внимание!"
START.arriveAndDeregister(); // "Марш!"
```

Dump wait-for-cars loop: `while (START.getRegisteredParties() > 3) Thread.sleep(100);`

> [!warning] Unverified traps from the dump
> - `awaitAdvance(0)` is tied to **phase 0** in this sample; later phases are a different Phaser story.
> - CountDownLatch itself is one-shot; this Phaser sketch deregisters parties instead of a single `countDown` to zero.
