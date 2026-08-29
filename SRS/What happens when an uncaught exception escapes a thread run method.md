<!--
reps: 0
priority: 0
-->
#Java/Concurrency/Threads #Java/Exceptions/Unchecked #SRS

# What happens when an uncaught exception escapes a thread `run` method?

> [!abstract] Short answer
> **That thread terminates.** Before it dies, `finally` clauses on the way out run, then the thread’s **uncaught exception handler**. If none was set, the `ThreadGroup` handles it, then the **default** handler. The usual default prints the stack trace on `System.err`. The JVM exits only if no other non-daemon thread is still running.

## The thread dies; the handler is not a `catch`

`Runnable.run` cannot declare checked exceptions, so what escapes is almost always a `RuntimeException` or `Error`. Unwinding still runs `finally`. If no `catch` on that thread handles the throw, the thread is **terminated** ([[How would you explain Java exception handling try catch and propagation]], [[Can main throw exceptions outward and where are they handled]]).

Order of uncaught handling:

1. `thread.setUncaughtExceptionHandler(...)` if set
2. Else `ThreadGroup.uncaughtException` (parents, then default)
3. Else `Thread.setDefaultUncaughtExceptionHandler`
4. Else print the thread name and stack trace to `System.err` (`ThreadDeath` is ignored by that last print)

The handler **observes** the `Throwable`. It does not resume `run`, and it does not keep the thread alive ([[How do you handle exceptions in Java applications]], [[What is ThreadDeath]]). Other threads are unaffected. A worker dying does not by itself stop a server with remaining non-daemon threads.

`main` is the same rule on the initial thread ([[Can a lambda throw a checked exception]], [[How would you explain InterruptedException in Java threads]]).

```d2
direction: down
run: "run() throws" {
  width: 280
  height: 50
}
fin: "finally on the way out" {
  width: 280
  height: 50
}
h: "UncaughtExceptionHandler" {
  width: 300
  height: 50
  style.fill: "#fff8e1"
}
dead: "thread terminated" {
  width: 280
  height: 50
}
run -> fin -> h -> dead
```

**Fig. 1.** Uncaught in `run` ends **this** thread after the handler, not the whole process by default.

```java
class Demo {
    static void start() {
        Thread t = new Thread(() -> {
            throw new IllegalStateException("worker");
        });
        t.start();
    }
}
```

**Listing 1.** The worker prints a stack trace (default handler) and ends. `main` can still return normally.

> [!warning] The handler is not a `try`/`catch` on `run`
> Work after the throw in that thread never runs. Install a handler for logging; put recovery **inside** `run` if the thread must continue.

> [!warning] One failed worker is not process exit
> Only the last non-daemon thread’s death ends the JVM. A pool thread’s uncaught exception can leave the process up and a task gone.

> [!tip] Interview answer
> **If `run` throws and nothing catches it, that thread is terminated after its uncaught-exception handler.** The default is a stack trace on standard error. Other threads keep running; the process exits only when no non-daemon thread remains.
