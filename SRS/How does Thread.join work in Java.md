<!--
reps: 0
priority: 0
-->
#Java/Concurrency/Threads #SRS

# How does Thread.join work in Java?

> [!abstract] Short answer
> **`t.join()`** blocks the **caller** until **`t` terminates**. The no-arg form is **`join(0)`**: wait forever. Timed `join(millis)` / `join(millis, nanos)` cap the wait (`0` millis still means forever). **Millis-`join` on a thread that was never `start()`ed returns immediately.** `join(Duration)` (Java 19+) **throws `IllegalThreadStateException`** if `t` was never started. Ordering T1 then T2: [[How do you run three Java threads T1 T2 T3 in that sequence]].

## Wait for `isAlive` to become false

The caller is whoever invokes `join` on a `Thread` object. It waits interruptibly until that thread is **dead**, or the timeout elapses. `InterruptedException` clears the caller’s interrupt status. After a successful wait for termination, the target’s actions **happen-before** the caller’s later code.

For **platform** threads, `join(millis)` loops on **`this.wait`** while **`isAlive`**. Termination runs **`notifyAll`** on that `Thread`. Applications must **not** use `wait` / `notify` / `notifyAll` on `Thread` instances.

`join(Duration)` does not wait if the duration is ≤ 0; it only tests whether the thread has already terminated. It still requires **`start`** first.

`join` does not start the thread — [[How do you forcibly start a Java thread]].

```java
public final class JoinExample {
    public static void main(String[] args) throws InterruptedException {
        Thread t = new Thread(() -> {}, "worker");
        t.start();
        t.join();
    }
}
```

**Listing 1.** Main waits until `worker` finishes `run`. Skip `start()` and millis-`join` returns at once; `join(Duration.ofSeconds(1))` throws `IllegalThreadStateException`.

```d2
direction: down
caller: "caller" {
  width: 120
  height: 40
  style.fill: "#e3f2fd"
}
join: "t.join()" {
  width: 140
  height: 35
  style.fill: "#fff8e1"
}
t: "t: run → terminate" {
  width: 200
  height: 40
  style.fill: "#e8f5e9"
}
caller -> join: "blocks"
t -> join: "isAlive false / notifyAll"
```

**Fig. 1.** Join waits for death of that thread. It does not run `t` and does not wait if millis-`join` sees an unstarted `t`.

> [!warning] Unstarted millis-`join` is silent
> No exception. Sequencing “T2 joins T1” fails if T1 has not been started.

> [!warning] Do not `wait` on a `Thread`
> `join` already uses that object’s monitor. Your `notify` races the implementation.

> [!tip] Interview answer
> `join` makes the current thread wait until that other thread terminates. No-arg waits forever; timed forms can return earlier. I always `start` before `join`, because the old millis overloads do not wait for an unstarted thread.
