<!--
reps: 0
priority: 0
-->
#Java/Concurrency/Threads #SRS

# What is the difference between interrupted and isInterrupted in Java?

> [!abstract] Short answer
> **`Thread.interrupted()`** is **`static`**: it tests the **current** thread and **clears** the interrupt status. Call it **twice** and the second result is **`false`** unless a new interrupt arrived. **`isInterrupted()`** is an **instance** method: it tests **that** `Thread` and **leaves the status**. Use `t.isInterrupted()` to peek at **another** thread, or `currentThread().isInterrupted()` to peek at **yourself** without clearing. `interrupt()` **sets** the flag (or wakes `wait`/`join`/`sleep` with **`InterruptedException`**, which **clears** it). IE: [[How would you explain InterruptedException in Java threads]]. Cooperative stop: [[How do you stop a Java thread safely and what does safely mean]]. Sleep: [[What does it mean to put a Java thread to sleep]].

## Clear vs peek

**`interrupt()`** records a request. A CPU loop **must poll**; it will **not** stop by magic. Poll with **`isInterrupted()`** if later code still needs the bit. Use **`interrupted()`** when you **consume** the request (then throw `InterruptedException`, or restore with **`currentThread().interrupt()`** if you cannot honor it).

Catching **`InterruptedException`** from **`wait` / `join` / `sleep`** means the status was **already cleared**. If you keep running, **set it again**. **`interrupted()` cannot take a `Thread` argument** — it is always the caller.

```java
Thread.currentThread().interrupt();
Thread.interrupted();                 // true, then cleared
Thread.interrupted();                 // false

worker.isInterrupted();               // peek; flag unchanged
```

**Listing 1.** Static method eats the flag. Instance method does not.

```d2
direction: down
intr: "interrupt()" {
  width: 120
  height: 36
  style.fill: "#fff8e1"
}
flag: "interrupt status" {
  width: 150
  height: 36
  style.fill: "#ffebee"
}
ie: "interrupted() clears" {
  width: 180
  height: 36
  style.fill: "#e3f2fd"
}
is: "isInterrupted() peeks" {
  width: 200
  height: 36
  style.fill: "#e8f5e9"
}
intr -> flag
flag -> ie
flag -> is
```

**Fig. 1.** One flag. Only the static test clears it (plus interruptible waits that throw).

> [!warning] `interrupted()` is not “the other thread”
> It always means **`Thread.currentThread()`**. To inspect `worker`, call **`worker.isInterrupted()`**.

> [!warning] Swallowing the bit hides cancel
> `if (Thread.interrupted()) { /* ignore */ }` **drops** the request. Restore or rethrow.

> [!tip] Interview answer
> interrupted is static: it asks about the current thread and clears the interrupt status. isInterrupted is an instance method that peeks at that thread and leaves the flag. If I catch InterruptedException and keep running, I set the flag again with interrupt.
