<!--
reps: 0
priority: 0
-->
#Paradigms/Async #Java/Concurrency #SRS

# What is the difference between being async and being concurrent?

> [!abstract] Short answer
> **Concurrent:** more than one computation is **in progress** (Java’s unit is the **thread**). **Async:** the **caller does not stay blocked** waiting — completion arrives later (`Future` / callback / event). They **overlap** (`supplyAsync` on a pool) but are **not** the same: two `Thread`s are concurrent without an async API; a **callback pipeline** can be async while **few** threads run stages. Not **parallel** (same instant on two cores). Trio: [[How does multithreading differ from parallelism and async work]]. Async style: [[How would you explain asynchronous programming and execution]]. `Future` / CF: [[How would you explain the Future interface in java.util.concurrent]], [[What is CompletableFuture]], [[How would you explain CompletableFuture for composing async work]]. Spring `@Async`: [[How does Spring Async work]], [[What happens when a Spring bean calls its own Async method]].

## In progress vs “I’ll take a callback”

**Concurrent (Java):** several **threads** exist and the scheduler **interleaves** them (or runs them in **parallel** on several cores). `new Thread(…).start()`, a **pool**, **virtual threads** — the caller of `start`/`execute` usually **returns immediately**, but that is **submitting work**, not the “async style” of **non-blocking I/O + callbacks**.

**Async style (JEP 444):** I/O methods that **do not wait**; they **signal later**. One **OS thread** can **service many** requests by **returning to the pool** while I/O is outstanding. Stages of **one** request may run on **different** threads. High **concurrency of operations** without one **platform thread per request**. **Virtual threads** keep **thread-per-request** code and still **unmount** on blocking JDK I/O — scale **without** rewriting as callbacks.

**`CompletableFuture`:** `supplyAsync` is **async for the caller** (you get a future) **and** **concurrent** (another thread in the **common pool**, unless you pass an `Executor`). `join()`/`get()` makes **that** caller **wait** — the **producer** was still concurrent.

```java
new Thread(this::a).start();
new Thread(this::b).start();                    // concurrent; caller not in async style

CompletableFuture<String> f = CompletableFuture.supplyAsync(this::load);
doOtherWork();                                  // caller not blocked on load
String v = f.join();                            // now this thread waits
```

**Listing 1.** Two threads vs a future. `join` is a **later** wait, not proof the work was sequential.

```d2
direction: down
c: "concurrent: threads in progress" {
  width: 260
  height: 40
  style.fill: "#e3f2fd"
}
a: "async: caller does not wait here" {
  width: 280
  height: 40
  style.fill: "#fff8e1"
}
p: "parallel: same instant, two cores" {
  width: 260
  height: 40
  style.fill: "#e8f5e9"
}
c -> p: "possible, not required"
a -> c: "often, not required"
```

**Fig. 1.** Async is about **when the caller waits**. Concurrent is about **how many executions exist**.

> [!warning] Async is not “faster threads”
> It **decouples waiting**. CPU-bound work still needs **cores**. Virtual threads are for **lots of blocked** tasks, not a speedup of arithmetic.

> [!warning] Spring `@Async` is not this definition
> That annotation **submits** to an **executor** (usually concurrent + async from the caller). **Self-invocation** and **`@EnableAsync`** are **proxy** rules — see the Spring cards, not the JMM.

> [!tip] Interview answer
> Concurrent means more than one thread of work is in progress. Async means the caller does not sit blocked; the result arrives later on a future or callback. They often go together on an executor, but two threads are concurrent without an async API, and an async pipeline can share a small pool.
