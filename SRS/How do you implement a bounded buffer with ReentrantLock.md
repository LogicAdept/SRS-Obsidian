<!--
reps: 0
priority: 0
-->
#Java/Concurrency/Synchronization/Locks #Career/Interview/Exercises #SRS

# How do you implement a bounded buffer with ReentrantLock?

> [!abstract] Short answer
> One **`ReentrantLock`**, two **`Condition`s** from `lock.newCondition()`: **`notFull`** for putters, **`notEmpty`** for takers. `put` awaits while the ring is full, then `notEmpty.signal()`. `take` awaits while empty, then `notFull.signal()`. Always **`lock` / `try` / `finally unlock`**, and wait in a **`while`**. Production code should use **`ArrayBlockingQueue`**, which is this design. Monitor-only version: [[How do you implement a bounded buffer with synchronized in Java]].

## Two wait-sets on one lock

`Condition` splits `Object.wait` / `notify` into **per-condition wait-sets** on a `Lock`. `await` **atomically releases** the lock and parks; before it returns, the thread **re-acquires** the lock. Spurious wakeups are allowed, so the capacity/`count` test stays in a **loop**. `signal` wakes **one** waiter on **that** condition — so a `put` need not wake another putter.

`ReentrantLock.lock()` then work in `try`/`finally unlock()`. `unlock` without holding throws `IllegalMonitorStateException`. `await` / `signal` on this lock’s conditions also require the lock held, or the same exception. `lockInterruptibly` if you want acquire to be an interrupt point; untimed `tryLock` can **barge** even on a fair lock.

Fair `ReentrantLock(true)`: condition waiters are signalled **FIFO**; reacquire order prefers the longest waiter. Fairness is not thread-scheduling fairness. Lock vs `synchronized`: [[What is the difference between synchronized and ReentrantLock]]. Single wait-set `wait`/`notify`: [[How do methods wait and notify notifyAll]].

```java
import java.util.concurrent.locks.Condition;
import java.util.concurrent.locks.Lock;
import java.util.concurrent.locks.ReentrantLock;

public final class BoundedBuffer<E> {
    private final Lock lock = new ReentrantLock();
    private final Condition notFull = lock.newCondition();
    private final Condition notEmpty = lock.newCondition();
    private final Object[] items;
    private int putptr, takeptr, count;

    public BoundedBuffer(int capacity) {
        if (capacity <= 0) {
            throw new IllegalArgumentException();
        }
        items = new Object[capacity];
    }

    public void put(E x) throws InterruptedException {
        lock.lock();
        try {
            while (count == items.length) {
                notFull.await();
            }
            items[putptr] = x;
            if (++putptr == items.length) {
                putptr = 0;
            }
            ++count;
            notEmpty.signal();
        } finally {
            lock.unlock();
        }
    }

    @SuppressWarnings("unchecked")
    public E take() throws InterruptedException {
        lock.lock();
        try {
            while (count == 0) {
                notEmpty.await();
            }
            E x = (E) items[takeptr];
            items[takeptr] = null;
            if (++takeptr == items.length) {
                takeptr = 0;
            }
            --count;
            notFull.signal();
            return x;
        } finally {
            lock.unlock();
        }
    }
}
```

**Listing 1.** Same structure as the `Condition` API sample (ring + `count`). Clearing the slot is extra; the sample leaves the stale reference. Prefer `ArrayBlockingQueue` instead of shipping this class.

```d2
direction: down
lock: "ReentrantLock" {
  width: 180
  height: 40
  style.fill: "#e3f2fd"
}
nf: "Condition notFull\nput waits" {
  width: 200
  height: 55
  style.fill: "#fff8e1"
}
ne: "Condition notEmpty\ntake waits" {
  width: 200
  height: 55
  style.fill: "#e8f5e9"
}
lock -> nf
lock -> ne
```

**Fig. 1.** One mutex, two queues. `signal` on `notEmpty` after a `put` wakes a taker without waking a blocked putter.

> [!warning] `if (count == 0) await` is wrong
> Spurious wakeup and extra `signal`s require re-testing the predicate. Use `while`.

> [!warning] Do not `synchronized (notEmpty)` or `notEmpty.notify()`
> A `Condition` is a normal object. Its monitor has **no** specified relationship to the `Lock`. Use `await` / `signal` while holding that lock.

> [!tip] Interview answer
> I use one `ReentrantLock` and two conditions, `notFull` and `notEmpty`. Put loops on full then signals empty; take loops on empty then signals full. Unlock in `finally`. In production I would use `ArrayBlockingQueue`.
