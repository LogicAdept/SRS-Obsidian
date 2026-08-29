<!--
reps: 0
priority: 0
-->
#Java/Concurrency/Threads #SRS

# How do you create a thread in Java?

> [!abstract] Short answer
> Construct a **platform** `Thread` with a `Runnable` (or subclass `Thread` and override `run`), then call **`start()`**. Public constructors always make platform threads. Since 21, **`Thread.ofPlatform()`** / **`Thread.ofVirtual()`** (or `startVirtualThread`) is the builder API. An `Executor` is a way to **run a task**, not a third constructor: it may use a new thread, a pooled thread, or the **caller**. Composition vs subclass: [[What is the difference between Thread and Runnable in Java]].

## `start` schedules; constructors do not

`Thread` implements `Runnable`. A new thread of execution begins only when **`start()`** schedules `run` to execute **concurrently** with the caller. The thread ends when `run` completes (normally or via an uncaught handler). **`start` at most once** — a second call throws `IllegalThreadStateException`. Invoking **`run()`** on the `Thread` object is not starting: for a platform thread built with a task it just runs that `Runnable` on the **current** thread; for a virtual thread a direct `run()` does **nothing**.

**Platform constructors.** `new Thread(task)` is equivalent to `Thread.ofPlatform().unstarted(task)` for a non-null task. No-arg / name-only constructors exist **only** so a subclass can override `run()`. The JDK says most applications have little need to extend `Thread`. Daemon status and priority are inherited from the parent at construction unless the builder sets them.

**Builders (21+).** `Thread.ofPlatform().start(runnable)` or `.unstarted(runnable)` then `start()`. `Thread.ofVirtual().start(runnable)` / `Thread.startVirtualThread(task)`. Virtual threads are daemons, unnamed by default, not meant for long CPU-bound work — [[How would you explain Virtual Threads]].

**Tasks vs threads.** `Runnable.run` returns `void`. `Callable` is **not** a `Thread` constructor argument. Returning a value is `ExecutorService.submit` / `Future`, which still does not let you name “the” worker thread — [[What is the difference between Runnable and Callable in Java]]. `Executor.execute` is documented as the alternative to `new Thread(task).start()` per task; a pool reuses workers — [[What advantages does ExecutorService offer over creating raw threads]].

```java
public final class CreateThread {
    public static void main(String[] args) {
        Runnable work = () -> System.out.println(Thread.currentThread());

        Thread platform = new Thread(work, "worker");
        platform.start();

        Thread virtual = Thread.ofVirtual().name("vt").start(work);
        Thread.startVirtualThread(work);
    }
}
```

**Listing 1.** Platform thread: constructor plus `start()`. Virtual thread: builder / `startVirtualThread`. `new Thread(work).run()` would print the **main** thread’s name, not start a second platform thread.

```d2
direction: down
task: "Runnable (or override run)" {
  width: 260
  height: 45
  style.fill: "#e3f2fd"
}
t: "new Thread / ofPlatform / ofVirtual" {
  width: 300
  height: 50
  style.fill: "#fff8e1"
}
start: "start() — scheduled once" {
  width: 260
  height: 45
  style.fill: "#e8f5e9"
}
exec: "Executor.execute\nnew, pooled, or caller" {
  width: 280
  height: 70
  style.fill: "#fce4ec"
}
task -> t: "create Thread object"
t -> start: "live concurrent thread"
task -> exec: "not the same as new Thread"
```

**Fig. 1.** Creating a `Thread` and submitting work to an executor are different APIs. Only `start()` (or a builder `start`) begins a new thread of execution.

> [!warning] `Callable` does not construct a `Thread`
> There is no `new Thread(callable)`. `submit(Callable)` returns a `Future`; the executor chooses the worker. That is not a fourth `Thread` constructor.

> [!warning] Do not call `run()` when you meant `start()`
> `run()` is the body. Without `start()`, you stay on the caller. After termination, `start()` cannot be reused.

> [!tip] Interview answer
> I pass a `Runnable` to `new Thread(...)` and call `start()`, or I use `Thread.ofVirtual().start` since 21. I do not subclass `Thread` unless I must; constructors without a task exist only for that. An executor is how I run work without managing each `Thread` myself — it is not `new Thread`.
