<!--
reps: 0
priority: 0
-->
#Java/Concurrency/Synchronization #SRS

# Why must `wait` be called in a `while` loop?

> [!abstract] Short answer
> Because waking up does **not** mean the condition is true. The `Object.wait` Javadoc (SE 21) states it directly: a thread "can wake up without being notified, interrupted, or timing out, a so-called **spurious wakeup**", and "applications **must guard against it by testing for the condition** that should have caused the thread to be awakened, and **continuing to wait if the condition is not satisfied**". Add two more everyday causes — another thread **consumes the resource** between `notify` and your re-acquisition of the monitor, and **`notifyAll` wakes every waiter** for a single unit of work — and an `if` would resume on a false predicate. The `while` re-tests; the `if` gambles. The primitive itself is dissected in [[How would you explain the Object wait method and waiting on monitors]], and its contrast with `sleep` in [[What is the difference between wait and sleep]].

## What actually happens between notify and resume

The Javadoc describes the wakeup as a **race, not a hand-off**: the awakened thread "is then removed from the wait set and re-enabled for thread scheduling. **It competes in the usual manner with other threads for the right to synchronize** on this object." So between `notify()` and the waiter's resumption, three things can invalidate the predicate:

* **Spurious wakeup.** Permitted by the specification on essentially all platforms; rare, but "applications must guard against it" — this is normative wording, not folklore.
* **Stolen condition.** Two waiters, one `notify`, one item: whichever thread wins the monitor race removes the item; the loser resumes with an **empty** queue unless it re-tests.
* **Broadcast wakeup.** `notifyAll()` is the safe default precisely because `notify()` may pick a waiter whose predicate is still false; with `notifyAll`, every woken thread re-tests in the loop and all but one go back to waiting.

A `while` turns each wakeup into *"re-acquire lock, re-check predicate, wait again if false"* — the only shape that survives all three cases.

```java
class BoundedBuffer {
    private final Object notFull  = new Object();
    private final Object notEmpty = new Object();
    private final Object[] cells = new Object[8];
    private int count, head, tail;

    public Object take() throws InterruptedException {
        synchronized (notEmpty) {
            while (count == 0) {          // re-tested on EVERY wakeup
                notEmpty.wait();          // releases notEmpty's monitor
            }
            Object item = cells[head];
            head = (head + 1) % cells.length;
            count--;
            synchronized (notFull) { notFull.notifyAll(); }
            return item;
        }
    }
}
```

**Listing 1.** The guarded-wait idiom: predicate, `wait`, and the mutation of the predicate all live under the **same monitor**, so the re-test can never see a stale interleaving.

```d2
direction: right
notify: "producer: notifyAll()" {style.fill: "#fff3e0"}
race: "all waiters re-enabled\nand compete for monitor" {style.fill: "#e3f2fd"}
winner: "first to get lock:\nitem available" {
  style.fill: "#e8f5e9"
}
loser: "next to get lock:\nitem already taken" {
  style.fill: "#ffebee"
}
iffail: "if: proceeds with\nEMPTY queue" {style.fill: "#b71c1c"}
whileok: "while: re-tests,\nwait() again" {style.fill: "#e8f5e9"}
notify -> race
race -> winner
race -> loser
winner -> whileok
loser -> iffail
loser -> whileok
```

**Fig. 1.** After `notifyAll` the lock is won sequentially: the first thread takes the work, the rest must re-test — an `if` lets the "loser" thread run with a false condition.

## Why the same monitor owns both the predicate and the wait

The guard only works because **check, wait, and the state change are mutually exclusive**. The waiting thread re-tests while holding the monitor; the producer mutates `count` while holding the same monitor; therefore a re-test can never observe a half-finished update. Breaking this — waiting on one object while synchronizing on another — reintroduces the lost-update window even with a `while`. This is also why the interruption path matters: `wait` may exit via `InterruptedException`, which is just another reason the code after it must be reached only through a fresh, successful re-test; see [[How would you explain InterruptedException in Java threads]].

> [!warning] `while` outside the right monitor is still broken
> The loop is necessary but not sufficient. Calling `wait()` from a `while` inside `synchronized (somethingElse)` throws **`IllegalMonitorStateException`** — the Javadoc requires the current thread to own "this object's monitor lock". And calling `notify()` on the condition object without holding its monitor throws the same exception. The pair *right monitor + right predicate in a while* is one idiom, not two optional habits; the monitor mechanics are in [[How would you explain monitor locks and intrinsic locks in Java]].

> [!tip] Interview answer
> **Because a wakeup is not a promise: the Javadoc explicitly requires guarding against spurious wakeups by re-testing the condition, and besides that, between notify and resumption another thread can consume the resource, while notifyAll wakes many waiters for one unit of work. The awakened thread must re-acquire the monitor and only then re-check — a while loop does exactly that, an if would proceed on a false predicate. And the whole idiom — check, wait, notify — must live on the same monitor, or the exception is IllegalMonitorStateException.**
