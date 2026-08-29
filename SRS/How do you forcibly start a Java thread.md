<!--
reps: 0
priority: 0
-->
#Java/Concurrency/Threads #SRS

# How do you forcibly start a Java thread?

> [!abstract] Short answer
> You **cannot** force a `Thread` onto the CPU or bring a finished one back. The only start API is **`start()`** (or a builder / `startVirtualThread` that calls it): that **schedules** `run` to execute **concurrently**. A thread is started **at most once**; a second `start()` throws **`IllegalThreadStateException`**. Calling **`run()`** is not a start. Constructing vs starting: [[How do you create a thread in Java]].

## `start` schedules; nothing “forces” the scheduler

`Thread.start()` “schedules this thread to begin execution” and it then runs **independently** of the caller. It does not mean “run this instruction now” or “preempt every other thread.” When the new thread actually gets a core is up to the JVM and OS. Priority is not a reliable order knob — [[Can thread priority reliably control execution order in Java]].

`start` may be invoked **at most once**. After the thread has been started — including after it has **terminated** — you cannot restart that same object. Create a **new** `Thread` (or a new virtual thread) for another execution of the same `Runnable`. There is no supported `resume`/`suspend` pair on modern `Thread` to “kick” a parked worker; those primitives are gone the same way `stop` is.

`run()` is the body. On a platform thread created with a `Runnable`, invoking `run()` yourself runs the task on the **current** thread. On a virtual thread, a direct `run()` does **nothing**. Neither is a forced concurrent start.

`Thread.ofPlatform().start(task)` / `Thread.ofVirtual().start(task)` / `Thread.startVirtualThread(task)` still go through the same start rule. `unstarted(task)` only builds the object; you still need `start()`.

`Thread.start` in the memory model happens-before the first action in the new thread. That is publication of the start, not a guarantee of immediate execution.

```java
public final class StartOnce {
    public static void main(String[] args) {
        Thread t = new Thread(() -> {}, "once");
        t.start();
        t.start(); // IllegalThreadStateException — already started
    }
}
```

**Listing 1.** The second `start()` is the documented failure. After `t` terminates, another `start()` still fails; you need a new `Thread`.

```d2
direction: down
obj: "new Thread / ofPlatform / ofVirtual" {
  width: 300
  height: 50
  style.fill: "#e3f2fd"
}
start: "start() — schedule, at most once" {
  width: 300
  height: 50
  style.fill: "#e8f5e9"
}
no: "run() / second start() / dead Thread" {
  width: 320
  height: 50
  style.fill: "#fce4ec"
}
obj -> start: "concurrent execution"
obj -> no: "not a start"
```

**Fig. 1.** Construction is not execution. There is no “force run now” or “force restart” API.

> [!warning] `run()` looks like it “starts” the work
> It runs the task **here**. Interviewers treat `thread.run()` instead of `thread.start()` as the classic bug.

> [!warning] A terminated thread is not reusable
> “Forcibly start it again” is not allowed. Keep the `Runnable` and wrap it in a **new** `Thread`.

> [!tip] Interview answer
> I call `start()`, which only schedules the thread; I cannot force the CPU. I never call `start()` twice on the same object, and I do not call `run()` when I meant a new thread. If the work must run again, I construct another `Thread`.
