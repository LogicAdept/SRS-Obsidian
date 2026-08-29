<!--
reps: 0
priority: 0
-->
#Java/Concurrency/Threads #Career/Interview/Exercises #SRS

# How do you run three Java threads T1 T2 T3 in that sequence?

> [!abstract] Short answer
> **`join`**. Start **T1**, **`t1.join()`**, then start **T2**, join, then **T3**. `join` waits for that thread to **terminate**. Starting all three and then joining them in order only waits for **completion**, it does **not** stop T2 from running at the same time as T1. Priority will not order them — [[Can thread priority reliably control execution order in Java]]. How `join` waits: [[How does Thread.join work in Java]].

## Join the predecessor; do not rely on start order

`Thread.join()` waits for that thread to terminate (`join(0)` waits forever). Timed overloads exist. **`InterruptedException`**: clear and restore if you abort. For platform threads, `join` is implemented with `wait` on the `Thread` object while `isAlive`; termination does `notifyAll`. Do **not** use `wait`/`notify` on `Thread` yourself.

**`join` on a thread that was never `start()`ed returns immediately.** If T3’s first line is `t2.join()` before anyone has called `t2.start()`, T3 runs at once. Start predecessors **before** anyone joins them.

Coordinator pattern (clearest):

1. `t1.start(); t1.join();`
2. `t2.start(); t2.join();`
3. `t3.start(); t3.join();`

Worker pattern: T2’s `run` starts with `t1.join()`, T3 with `t2.join()`. Start **T1, then T2, then T3** so no join hits an unstarted thread.

`CountDownLatch(1)` between stages also sequences **work** while all threads may already be alive: T2 `await`s T1’s `countDown`, T3 awaits T2. That is the opposite of a **start-together** gate — [[How do you use CountDownLatch so several threads start together]]. A **single-thread** executor runs three **tasks** in order, not three concurrent `Thread`s.

Successful `join` happens-before continued work in the joiner: T1’s writes are visible to T2 after `t1.join()`.

```java
public final class SequenceT1T2T3 {
 public static void main(String[] args) throws InterruptedException {
 Thread t1 = new Thread(() -> System.out.print("T1"), "T1");
 Thread t2 = new Thread(() -> System.out.print("T2"), "T2");
 Thread t3 = new Thread(() -> System.out.print("T3"), "T3");
 t1.start();
 t1.join();
 t2.start();
 t2.join();
 t3.start();
 t3.join();
 }
}
```

**Listing 1.** Prints `T1T2T3`. `t1.start(); t2.start(); t3.start();` then three joins does **not** give that order.

```d2
direction: down
t1: "T1 start → run → terminate" {
 width: 280
 height: 45
 style.fill: "#e8f5e9"
}
j1: "join T1" {
 width: 120
 height: 35
 style.fill: "#fff8e1"
}
t2: "T2 start → run → terminate" {
 width: 280
 height: 45
 style.fill: "#e8f5e9"
}
j2: "join T2" {
 width: 120
 height: 35
 style.fill: "#fff8e1"
}
t3: "T3 start → run" {
 width: 220
 height: 40
 style.fill: "#e8f5e9"
}
t1 -> j1 -> t2 -> j2 -> t3
```

**Fig. 1.** Sequence is **start, join, start**, not start-all then hope.

> [!warning] `join` before `start` is a no-op wait
> Unstarted `join` returns at once. Starting T2/T3 first and joining the predecessor from inside them races that rule.

> [!warning] Three `start()` then three `join()` is “wait until all done”
> T1, T2, and T3 still overlap. That is not T1-then-T2-then-T3.

> [!tip] Interview answer
> I start T1 and `join` it, then start T2 and join, then T3. I do not start all three at once if I need their `run` methods in order. `join` on a thread that was never started does not wait.
