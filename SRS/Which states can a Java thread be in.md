<!--
reps: 0
priority: 0
-->
#Java/Concurrency/Threads #SRS

# Which states can a Java thread be in?

> [!abstract] Short answer
> Exactly **six** `Thread.State` values, and **only one at a time**: **`NEW`**, **`RUNNABLE`**, **`BLOCKED`**, **`WAITING`**, **`TIMED_WAITING`**, **`TERMINATED`**. These are **virtual-machine** states, **not** OS run/wait bits. **`RUNNABLE` already includes both “on a CPU” and “waiting for the OS to give a CPU.”** There is **no** `Running` constant. **`getState()`** is for **monitoring**, not for locking. What is a thread: [[What is thread]]. `start` vs `run`: [[What is the difference between Thread start and run]]. Monitor (`BLOCKED`): [[What is monitor in Java]]. `wait` vs `sleep`: [[How would you explain wait, sleep]].

## Six VM states

**`NEW`** — constructed; **`start()`** has not run. **`RUNNABLE`** — executing in the JVM (may still wait on the OS for a processor). **`BLOCKED`** — waiting to **enter** or **reenter** a **`synchronized`** monitor after `wait`. **`WAITING`** — wait with **no** timeout (`Object.wait()`, `Thread.join()`, `LockSupport.park()`). **`TIMED_WAITING`** — wait with a **timeout** (`sleep`, timed `wait`/`join`, `parkNanos`/`parkUntil`). **`TERMINATED`** — `run` has finished (normal or uncaught). **`isAlive()`** is true after start and before terminate (`NEW` and `TERMINATED` are not alive).

```d2
direction: down
n: NEW {
 width: 120
 height: 32
 style.fill: "#eceff1"
}
r: RUNNABLE {
 width: 140
 height: 32
 style.fill: "#e8f5e9"
}
b: BLOCKED {
 width: 120
 height: 32
 style.fill: "#ffebee"
}
w: WAITING {
 width: 120
 height: 32
 style.fill: "#fff8e1"
}
tw: TIMED_WAITING {
 width: 160
 height: 32
 style.fill: "#fff8e1"
}
x: TERMINATED {
 width: 140
 height: 32
 style.fill: "#e3f2fd"
}
n -> r: start
r -> b: monitor
b -> r
r -> w: wait/join/park
w -> r
r -> tw: sleep/timed wait
tw -> r
r -> x: run ends
```

**Fig. 1.** One `Thread.State` at a time. Wait states return to **`RUNNABLE`**, not to **`NEW`**.

```java
Thread t = new Thread(() -> {});
assert t.getState() == Thread.State.NEW;
t.start();
t.join();
assert t.getState() == Thread.State.TERMINATED;
```

**Listing 1.** `NEW` before `start`; `TERMINATED` after `join`. Mid-run states need a pause or a lock to observe.

> [!warning] `BLOCKED` is a monitor, not I/O
> Waiting on a socket or a `BlockingQueue.take()` is **`WAITING` / `TIMED_WAITING`** (or native parking), **not** `BLOCKED`. `BLOCKED` means **another thread owns the `synchronized` lock** this thread needs.

> [!warning] Do not lock on `getState()`
> The API is for **monitoring**. There is **no** `Running` enum constant. OS “running vs ready” is **inside** `RUNNABLE`.

> [!tip] Interview answer
> A Java thread has six Thread.State values: NEW, RUNNABLE, BLOCKED, WAITING, TIMED_WAITING, and TERMINATED, and only one at a time. RUNNABLE already covers both executing and waiting for a CPU; BLOCKED is only the intrinsic monitor. getState is for diagnostics, not for synchronization.
