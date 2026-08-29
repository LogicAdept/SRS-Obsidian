<!--
reps: 0
priority: 0
-->
#Java/Concurrency/Synchronization #Career/Interview/Exercises #SRS

# How do you implement a bounded buffer with synchronized in Java?

> [!abstract] Short answer
> One monitor, a ring (or list) plus a **count**, and **`wait` / `notifyAll`**. `put` loops **`while` full**, then inserts and **`notifyAll()`**. `take` loops **`while` empty**, then removes and **`notifyAll()`**. `wait` must run while owning that monitor and **releases it** until wakeup, then **reacquires** before returning. One wait-set cannot target only producers or only consumers, so **`notify` is unsafe** here. Two `Condition`s: [[How do you implement a bounded buffer with ReentrantLock]].

## One wait-set, two predicates

`synchronized` methods lock **`this`**. A `synchronized (lock)` block locks **that** object. `wait` / `notify` / `notifyAll` must be invoked on **the same** object, and the caller must own its monitor (`IllegalMonitorStateException` otherwise) — [[Why must wait and notify run inside synchronized blocks]], [[How do methods wait and notify notifyAll]].

Unlike `ReentrantLock` + `notFull` / `notEmpty`, a built-in monitor has **one** wait-set. `notify()` wakes an **arbitrary** waiter. If a producer is waiting for space and a consumer for data, waking the wrong kind **deadlocks** (everyone still blocked, no `notifyAll`). Use **`notifyAll`**. Still loop: spurious wakeup, and a wakeup does not mean **your** predicate is true.

`wait` throws `InterruptedException`; restore the interrupt if you abort. Unlock is implicit when the `synchronized` block/method exits, including after `wait` reacquires.

The dump pasted **method vs block** and **`this` vs a private lock**. That is not this exercise. A private `final Object lock` is a valid mutex for the buffer (callers cannot `synchronized` on your `this`). “Blocks are faster than methods” is not a language rule.

```java
public final class SyncBoundedBuffer<E> {
    private final Object[] items;
    private int putptr, takeptr, count;

    public SyncBoundedBuffer(int capacity) {
        if (capacity <= 0) {
            throw new IllegalArgumentException();
        }
        items = new Object[capacity];
    }

    public synchronized void put(E x) throws InterruptedException {
        while (count == items.length) {
            wait();
        }
        items[putptr] = x;
        if (++putptr == items.length) {
            putptr = 0;
        }
        ++count;
        notifyAll();
    }

    @SuppressWarnings("unchecked")
    public synchronized E take() throws InterruptedException {
        while (count == 0) {
            wait();
        }
        E x = (E) items[takeptr];
        items[takeptr] = null;
        if (++takeptr == items.length) {
            takeptr = 0;
        }
        --count;
        notifyAll();
        return x;
    }
}
```

**Listing 1.** Intrinsic lock is `this`. Same ring as the `Condition` sample; `notifyAll` because producers and consumers share one wait-set. Prefer `ArrayBlockingQueue` in production.

```d2
direction: down
mon: "synchronized (this)\none wait-set" {
  width: 260
  height: 55
  style.fill: "#e3f2fd"
}
put: "while full: wait()\nthen notifyAll" {
  width: 240
  height: 55
  style.fill: "#fff8e1"
}
take: "while empty: wait()\nthen notifyAll" {
  width: 240
  height: 55
  style.fill: "#e8f5e9"
}
mon -> put
mon -> take
```

**Fig. 1.** Both roles sleep on the same set. `notifyAll` lets each thread re-test `count`.

> [!warning] `notify()` can stall the buffer
> One wait-set, two reasons to wait. The woken thread might be another producer on a full buffer (or another consumer on empty) and go back to `wait` with nobody left to signal.

> [!warning] `if (count == 0) wait()` is wrong
> Spurious wakeup and `notifyAll` both require re-checking the predicate. Use `while`.

> [!tip] Interview answer
> I synchronize on the buffer, wait in a `while` until there is room or an item, then `notifyAll`. I do not use `notify`, because producers and consumers share one wait-set. For separate queues I would use `ReentrantLock` and two `Condition`s, or just `ArrayBlockingQueue`.
