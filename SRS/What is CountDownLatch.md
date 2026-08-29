<!--
reps: 0
priority: 0
-->
#Java/Concurrency/Synchronizers #SRS

# What is CountDownLatch?

> [!abstract] Short answer
> A **`CountDownLatch`** (Java 5) lets **one or more threads `await`** until other threads have **`countDown`** a constructor **count** to **zero**. Then waiters are **released** and later **`await` returns immediately**. **One-shot:** the count **cannot be reset** (use **`CyclicBarrier`** or **`Phaser`** if you need reuse). **`countDown` does not wait.** Start-together: [[How do you use CountDownLatch so several threads start together]]. Vs barrier: [[What is the difference between CyclicBarrier and CountDownLatch]]. Phaser: [[How can you emulate CountDownLatch with Phaser]].

## Gate or N completions

**Count 1:** on/off **gate** — everyone `await`s until one `countDown`. **Count N:** wait until **N** actions (or N threads) have counted down. Coordinators **`await`**; workers **`countDown`** and **proceed**. Negative count → **`IllegalArgumentException`**. Extra `countDown` at zero is a **no-op**. **`await`** throws **`InterruptedException`** and **clears** the interrupt status. Timed **`await`** returns **`false`** on timeout. Actions before **`countDown`** **happen-before** after a successful **`await`**. Package: [[How would you explain the java.util.concurrent package]]. **`Phaser`**: [[How would you explain java.util.concurrent.Phaser]].

```java
CountDownLatch start = new CountDownLatch(1);
CountDownLatch done = new CountDownLatch(n);
for (int i = 0; i < n; i++) {
 new Thread(() -> {
 try {
 start.await();
 work();
 done.countDown();
 } catch (InterruptedException e) {
 Thread.currentThread().interrupt();
 }
 }).start();
}
start.countDown();
done.await();
```

**Listing 1.** Start signal (count 1) then completion latch (count N). Both are one-shot.

```d2
direction: down
c: "count N" {
 width: 100
 height: 36
 style.fill: "#fff8e1"
}
d: "countDown × N" {
 width: 140
 height: 36
 style.fill: "#e8f5e9"
}
a: "await returns" {
 width: 140
 height: 36
 style.fill: "#e3f2fd"
}
c -> d -> a: "reaches 0"
```

**Fig. 1.** Waiters block until the count hits zero. No reset.

> [!warning] Not a cyclic barrier
> After zero, it stays open. There is **no `reset`**. Repeating phases → **`CyclicBarrier`** or **`Phaser`**.

> [!warning] `countDown` is not `await`
> Workers can finish and run more code. Only **`await`** waits. Swallowing **`InterruptedException`** in workers hides cancel.

> [!tip] Interview answer
> CountDownLatch is a one-shot counter: threads await until others have counted down to zero. Count one is a start gate; count N waits for N tasks. I cannot reset it, and countDown does not block.
