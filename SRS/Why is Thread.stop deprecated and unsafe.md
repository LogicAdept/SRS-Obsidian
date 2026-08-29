<!--
reps: 0
priority: 0
-->
#Java/Concurrency/Threads #SRS

# Why is Thread.stop deprecated and unsafe?

> [!abstract] Short answer
> `Thread.stop` was specified to inject **`ThreadDeath`** into another thread. As that **Error** unwound the stack it **unlocked every monitor** the victim held. Any object still **mid-update** became **damaged** and visible — **arbitrary** behavior, often **hours later**, with **no** uncaught-exception warning (`ThreadDeath` died **quietly**). Deprecated **since 1.2**; the ability to actually stop a thread is **gone**. In **21** `stop()` **always** throws **`UnsupportedOperationException`**. Cancel with a **`volatile`** (or synchronized) **flag**, return from `run`, and **`interrupt`** waits. Interrupt: [[How would you explain InterruptedException in Java threads]]. Flag vs `interrupted()`: [[What is the difference between interrupted and isInterrupted in Java]]. Why visibility needs a protocol: [[Why does the Java Memory Model matter for concurrency]].

## ThreadDeath, monitors, silence

A `synchronized` region is supposed to leave shared state **consistent** before **unlock**. `stop` did not wait for that: `ThreadDeath` could be thrown **almost anywhere**, including inside the region. Unlock was just exception unwinding. Other threads then used **inconsistent** objects. Catching `ThreadDeath` to “repair” is not practical: it can fire **anywhere**, and a **second** `ThreadDeath` can hit **`catch` / `finally`** while you clean up.

That is why the primitive is **inherently unsafe**, not merely “rude.” `suspend` / `resume` were removed for a **different** reason (deadlock if the victim holds a monitor you need in order to `resume`). Uncaught exceptions on `run`: [[What happens when an uncaught exception escapes a thread run method]].

**Replacement.** Set a flag the worker **polls**; it **returns** from `run` in order. The flag must be **`volatile`** or guarded by **synchronization**. If the worker **waits** (`Object.wait`, `sleep`, `join`, …), **`interrupt`** after the flag. Methods that catch `InterruptedException` and cannot handle cancel **now** must **reassert**: `Thread.currentThread().interrupt()`. There is **no** general kill for code that ignores interrupt (and `stop` would not have helped those I/O cases either). Cooperative cancel: [[What principles do you follow in multithreaded Java programming]].

```java
final class CooperativeCancel implements Runnable {
    private volatile boolean running = true;
    private Thread worker;

    void start() {
        worker = Thread.ofPlatform().start(this);
    }

    void cancel() {
        running = false;
        Thread w = worker;
        if (w != null) {
            w.interrupt();
        }
    }

    @Override
    public void run() {
        while (running) {
            try {
                Thread.sleep(100);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                running = false;
            }
        }
    }
}
```

**Listing 1.** Flag plus **interrupt**. The flag is **`volatile`** so the worker sees cancel; interrupt breaks **`sleep`**. Restoring the interrupt status keeps cancel visible to callers up the stack.

```d2
direction: down
stop: "Thread.stop (historical)" {
  width: 220
  height: 40
  style.fill: "#ffebee"
}
death: "ThreadDeath on victim" {
  width: 200
  height: 36
  style.fill: "#fff8e1"
}
unlock: "unlock all monitors" {
  width: 200
  height: 36
  style.fill: "#ffe0b2"
}
damage: "inconsistent objects visible" {
  width: 240
  height: 40
  style.fill: "#ffcdd2"
}
stop -> death
death -> unlock
unlock -> damage
```

**Fig. 1.** The hazard is **unlock while mutated**, not “the thread exited.”

> [!warning] `stop()` does not stop anyone now
> `@Deprecated(since = "1.2", forRemoval = true)` and, in **21**, **always** `UnsupportedOperationException`. Do not write it as a cancel API. `ThreadDeath` itself is deprecated **since 20**, for removal, because stopping was taken out.

> [!warning] Swallowing `InterruptedException` undoes interrupt-cancel
> Empty `catch` after `sleep` **clears** the interrupt (the catch already did) and **does not** restore it. The official “reinterrupt yourself” line is `Thread.currentThread().interrupt()`. A `volatile` flag without interrupt still leaves a thread stuck in a long **wait**.

> [!warning] Do not treat `stop` as “who closes the socket / transaction”
> Official harm is **monitor unlock on damaged objects**, not a specified JDBC or TCP checklist. There was **no** safe general cleanup for “killed in the middle.” Your `finally` around **your** `run` loop is the cleanup path.

> [!tip] Interview answer
> Thread.stop was unsafe because it threw ThreadDeath into another thread and unlocked every monitor on the way out, so other threads could see half-updated objects, sometimes much later, with no loud failure. It was deprecated in 1.2 and in modern JDKs the method only throws UnsupportedOperationException. I cancel with a volatile flag, return from run, and interrupt waits, restoring the interrupt status if I catch InterruptedException.
