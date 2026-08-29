<!--
reps: 0
priority: 0
-->
#Java/Concurrency/Threads #SRS

# How do you run a class instance on its own thread?

> [!abstract] Short answer
> Make the instance a **`Runnable`**, pass it to a **`Thread`**, and call **`start()`**. That thread’s `run()` is the instance’s `run()`. Extending `Thread` makes the object **itself** the thread: `instance.start()`. Calling other methods on that object from `main` still runs on **the caller**. Creating vs starting: [[How do you create a thread in Java]]. `Runnable` vs subclass: [[What is the difference between Thread and Runnable in Java]].

## The instance is the task, `start` is the thread

`Thread` implements `Runnable`. Public constructors take a **`Runnable` task**. `new Thread(worker).start()` schedules **`worker.run()`** concurrently. `Thread.ofPlatform().start(worker)` / `Thread.ofVirtual().start(worker)` / `startVirtualThread(worker)` do the same for platform or virtual threads.

If the class **extends `Thread`**, override `run()` and call **`start()` on that instance**. No-arg constructors exist **only** for that subclass pattern. The JDK says most applications should pass a task instead of extending `Thread`.

`start()` at most once (`IllegalThreadStateException` otherwise). **`run()`** on the `Thread` or on the `Runnable` from another thread does **not** create a new thread of execution — [[How do you forcibly start a Java thread]]. An `Executor.execute(worker)` may use a **pool** or even the **caller**; that is not “its own” dedicated `Thread`.

Do not `start()` from a constructor that passes **`this`**: other threads can observe the object **before** the constructor finishes. Finish construction, then start.

```java
public final class Worker implements Runnable {
    private final String name;

    public Worker(String name) {
        this.name = name;
    }

    @Override
    public void run() {
        System.out.println(name + " on " + Thread.currentThread());
    }

    public static void main(String[] args) {
        Worker w = new Worker("job");
        Thread t = new Thread(w, "worker");
        t.start();
        w.run(); // still main — not a second worker thread
    }
}
```

**Listing 1.** One object, two executions of `run`: `t.start()` on thread `worker`, the explicit `w.run()` on `main`.

```d2
direction: down
obj: "instance implements Runnable" {
  width: 280
  height: 45
  style.fill: "#e3f2fd"
}
th: "new Thread(instance).start()" {
  width: 280
  height: 45
  style.fill: "#e8f5e9"
}
call: "instance.method() from main" {
  width: 280
  height: 45
  style.fill: "#fce4ec"
}
obj -> th: "run() on the new thread"
obj -> call: "still the caller"
```

**Fig. 1.** Sharing the object does not move later method calls onto that thread. Only `run` (after `start`) is scheduled there.

> [!warning] `new Thread(this)` inside the constructor
> `start()` can run `run()` before subclass fields are assigned. Construct, then start from the caller.

> [!warning] `thread.run()` is not “on its own thread”
> It invokes the task on the **current** thread. Use `start()`.

> [!tip] Interview answer
> I implement `Runnable` on the class, pass the instance to `new Thread(...)`, and call `start()`. I do not extend `Thread` unless I must. Other methods on that object still run on whoever calls them, not automatically on the worker thread.
