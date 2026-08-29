<!--
reps: 0
priority: 0
-->
#Java/Concurrency/Synchronization #SRS

# How does notify differ from notifyAll in Java?

> [!abstract] Short answer
> Both must run while the caller **owns that object’s monitor**. **`notify()`** moves **one** arbitrary thread from the wait-set toward runnable. **`notifyAll()`** moves **every** waiter. Neither thread runs `wait`’s return until it **reacquires** the monitor. One wait-set plus two reasons to wait (full vs empty) needs **`notifyAll`** — [[How do you implement a bounded buffer with synchronized in Java]]. Same trio: [[How do methods wait and notify notifyAll]].

## One waiter vs the whole wait-set

`wait` parks the current thread **in that object’s wait-set** and **releases** the monitor. `notify` / `notifyAll` do not hand the lock to the woken thread; they only make waiters **eligible**. The scheduler plus the next `lock` of the same monitor decide who actually enters. `IllegalMonitorStateException` if you call any of them without owning the monitor — [[Why must wait and notify run inside synchronized blocks]].

`notify()`: if the wait-set is empty, it is a no-op; otherwise **one** thread is chosen (**no fairness** documented). If producers and consumers share **one** set, that one thread might be the **wrong role** and go back to `wait` with nobody left to signal.

`notifyAll()`: every waiter competes for the monitor, then **re-tests** the predicate (`while`, not `if` — spurious wakeup). Extra wakeups cost context switches; they do not skip the `while` check.

`ReentrantLock` can split roles onto two `Condition`s and `signal()` one queue — [[How do you implement a bounded buffer with ReentrantLock]].

```java
public final class NotifyVsNotifyAll {
 private boolean ready;

 public synchronized void awaitReady() throws InterruptedException {
 while (!ready) {
 wait();
 }
 }

 public synchronized void signalOne() {
 ready = true;
 notify();
 }

 public synchronized void signalAll() {
 ready = true;
 notifyAll();
 }
}
```

**Listing 1.** One predicate: `notify` is enough if every waiter wants `ready`. Two predicates on the same object: use `notifyAll` (or two `Condition`s).

```d2
direction: down
ws: "wait-set of obj" {
 width: 200
 height: 40
 style.fill: "#e3f2fd"
}
one: "notify — one arbitrary waiter" {
 width: 280
 height: 45
 style.fill: "#fff8e1"
}
all: "notifyAll — every waiter" {
 width: 280
 height: 45
 style.fill: "#e8f5e9"
}
ws -> one
ws -> all
```

**Fig. 1.** Same monitor, different number of threads taken out of the wait-set. All still serialize on reacquire.

> [!warning] `notify` is not FIFO
> The specification does not say which waiter wins. Do not assume “the one that waited longest.”

> [!warning] `if (!ready) wait()` is wrong even after `notifyAll`
> Spurious wakeup and extra signals require looping on the condition.

> [!tip] Interview answer
> `notify` wakes one arbitrary thread in that object’s wait-set; `notifyAll` wakes them all. They still fight for the monitor. I use `notifyAll` when more than one kind of waiter shares the lock, and I always wait in a `while`.
