<!--
reps: 0
priority: 0
-->
#Java/Concurrency/Synchronization #Java/Language #SRS

# How would you explain the Object wait method and waiting on monitors?

> [!abstract] Short answer
> **`Object.wait()`** parks the **current** thread on **this object’s wait set** until **notify / notifyAll**, **interrupt**, a **timeout**, or a **spurious wakeup**. You **must own the monitor** (`synchronized` on **that** object) or you get **`IllegalMonitorStateException`**. `wait` **drops all nested locks on this object**, sleeps, then **reacquires the same nesting** before return. Other objects you still hold stay locked. **`wait()` ≡ `wait(0L, 0)`**: zero timeout means **ignore the clock** (wait until awakened). Always **`while (!condition) wait(...)`**. Must be synchronized: [[Why must wait and notify run inside synchronized blocks]]. `while` not `if`: [[Why wait() while, if]]. Timed vs untimed: [[How does Object wait with a timeout differ from wait without arguments]]. Notify: [[How does notify differ from notifyAll in Java]].

## Wait set, then compete for the monitor again

Every object has a **monitor** and a **wait set**. `wait`/`notify`/`notifyAll` are the only APIs that move threads on that set. After wakeup you **are not inside the monitor yet** — you **contend** like any other locker; when you win, state is as **before** `wait`. `InterruptedException` is thrown **after** that restore; the interrupt flag is **cleared**. Interrupt: [[How would you explain InterruptedException in Java threads]].

`Thread.sleep` **keeps** monitors. `Lock` + `Condition.await` is the same shape for explicit locks. Bounded buffer: [[How do you implement a bounded buffer with synchronized in Java]]. Intrinsic lock: [[How would you explain monitor locks and intrinsic locks in Java]].

```java
synchronized (obj) {
    while (!ready) {
        obj.wait();
    }
    // condition holds; still holding obj's monitor
}
```

**Listing 1.** Official pattern: loop around `wait` so notify and spurious wakeups do not proceed with a false condition.

```d2
direction: down
own: "own monitor of obj" {
  width: 200
  height: 40
  style.fill: "#e3f2fd"
}
ws: "enter wait set\nunlock obj (all nests)" {
  width: 260
  height: 50
  style.fill: "#fff8e1"
}
wake: "notify / interrupt / timeout / spurious" {
  width: 300
  height: 45
  style.fill: "#ffebee"
}
relock: "reacquire obj, then return" {
  width: 260
  height: 40
  style.fill: "#e8f5e9"
}
own -> ws
ws -> wake
wake -> relock
```

**Fig. 1.** Waiting is not holding. Return from `wait` is back in the monitor.

> [!warning] Only this object’s locks are released
> If you also hold `other`, you keep it. That is a **deadlock** trap if the notifier needs `other`.

> [!warning] `if (!ready) wait()` is wrong
> Spurious wakeup is **allowed**. `notify` also does not name **which** waiter. Re-test the condition in a **`while`**.

> [!tip] Interview answer
> wait parks you on that object’s wait set and drops the monitor so someone else can notify. You must already be synchronized on that same object, and you loop while the condition is false. Timed wait of zero means wait forever, same as wait with no arguments.
