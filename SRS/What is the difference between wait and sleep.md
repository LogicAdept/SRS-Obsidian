<!--
reps: 0
priority: 0
-->
#Java/Concurrency/Threads #SRS

# What is the difference between `wait` and `sleep`?

> [!abstract] Short answer
> **`wait()`** is a final method of **`Object`** used for **coordination**: the thread must **hold the object's monitor**, then it **relinquishes** that monitor and parks in the object's **wait set** until `notify`/`notifyAll`, interruption, timeout, or a spurious wakeup. **`Thread.sleep(ms)`** is a **static** method used for **timing**: it pauses the **currently executing thread** and — in the words of the SE 21 Javadoc — "the thread **does not lose ownership of any monitors**". So `wait` releases a lock, `sleep` releases none; `wait` needs a monitor, `sleep` needs nothing; `wait` is woken by another thread's `notify`, `sleep` only by elapsed time or interruption. The guarded-`wait` discipline lives in [[Why must wait be called in a while loop]]; the monitor protocol it depends on is in [[How would you explain the Object wait method and waiting on monitors]].

## Contract side by side

Both methods throw **`InterruptedException`** (checked), but they answer different questions. `wait()` asks *"when is the condition ready?"* — it is meaningless without a shared monitor and a predicate. `sleep(ms)` asks *"how long should I pause?"* — it needs no lock, no object, no condition. The mechanics differ in three verified ways.

* **Class and lookup.** `wait()` is declared final on `java.lang.Object`, so every object has one. `sleep` is a **static** method of `java.lang.Thread`; calling `t.sleep(1000)` still sleeps the **current** thread, not `t` — the qualifier is ignored.
* **Monitor ownership.** The Javadoc for `wait` requires: "The current thread must own this object's monitor lock", otherwise it throws **`IllegalMonitorStateException`** at runtime. `sleep` has no such precondition.
* **What is released.** On `wait`, the thread "place[s] itself in the wait set for this object and then ... relinquish[ies] any and all synchronization claims **on this object**" — and the Javadoc adds that **other** objects the thread holds stay locked. On `sleep`, **no monitor is released at all**: a sleeping thread inside `synchronized` still blocks every competitor.

After waking, a `wait`ing thread does **not** continue immediately: it "competes in the usual manner with other threads for the right to synchronize" and must **re-acquire the monitor** before the call returns.

```java
public class Queue<T> {
    private final java.util.ArrayDeque<T> items = new java.util.ArrayDeque<>();

    public synchronized T take() throws InterruptedException {
        while (items.isEmpty()) {   // re-test: spurious wakeups happen
            wait();                 // releases THIS monitor, parks in wait set
        }
        return items.removeFirst(); // monitor re-acquired before returning
    }

    public synchronized void put(T item) {
        items.addLast(item);
        notifyAll();                // wakes waiters; they re-test in while
    }

    public void retry(long backoff) throws InterruptedException {
        Thread.sleep(backoff);      // holds no monitor: safe pause
    }
}
```

**Listing 1.** `wait` inside `synchronized` with a predicate loop; `sleep` used for a lock-free back-off pause.

```d2
direction: right
wait lane: "" {
  hold: "hold monitor\n(synchronized)" {style.fill: "#e3f2fd"}
  park: "wait(): release monitor\nenter wait set" {style.fill: "#fff3e0"}
  wake: "notify / interrupt /\ntimeout / spurious" {style.fill: "#ffebee"}
  reacq: "re-acquire monitor\nthen resume" {style.fill: "#e8f5e9"}
  hold -> park -> wake -> reacq
}
sleep lane: "" {
  hold2: "maybe holds monitors" {style.fill: "#e3f2fd"}
  timer: "sleep(ms): keeps ALL locks\njust doesn't run" {style.fill: "#fff3e0"}
  after: "resume after elapsed ms\nor interrupt" {style.fill: "#e8f5e9"}
  hold2 -> timer -> after
}
```

**Fig. 1.** `wait` is a monitor lifecycle (release, park, re-acquire); `sleep` is pure time-out with locks untouched.

## Which one to reach for

Use `wait`/`notifyAll` when a thread must react to a **state change produced by another thread** — queue occupancy, a flag, a connection becoming ready. Use `sleep` when the thread must simply **wait out time**: polling back-off, rate limiting, test timing. Replacing one with the other breaks correctness: `sleep` inside a condition check makes other threads wait out your whole pause, and `wait` outside `synchronized` throws immediately. Interrupt handling is the same shape for both — the call exits with `InterruptedException`, and the thread's interruption status is cleared, so the status should be restored by hand; details in [[How would you explain InterruptedException in Java threads]].

> [!warning] `t.sleep(...)` does not sleep thread `t`
> The classic trap: writing `myThread.sleep(1000)` and believing another thread will pause. `sleep` is **static** — the call is equivalent to `Thread.sleep(1000)` and pauses the **caller**. The JLS even lets compilers flag such calls. The same illusion around `wait` fails harder: `otherObject.wait()` outside a `synchronized (otherObject)` block throws **`IllegalMonitorStateException`** on the spot.

> [!example] Partial release is still release
> `wait` releases **only the monitor of the object it was called on**. If a thread holds locks on `a` and `b` and calls `a.wait()`, lock `b` stays held — other threads that need `b` remain blocked while the thread waits. Nested monitors are why `wait`-based designs keep one lock per condition object; see [[Can Java code manually control which thread holds a monitor]].

> [!tip] Interview answer
> **`wait` is Object's monitor API: you must hold the object's lock, it releases exactly that lock and parks in the wait set until notify, interrupt, timeout or a spurious wakeup, then re-acquires the lock. `sleep` is a static Thread method that pauses the current thread for a duration and releases no monitors at all. One is for condition coordination, the other for plain time-out — and both blow up real code through the traps: `t.sleep` sleeps the caller, `wait` outside synchronized throws IllegalMonitorStateException.**
