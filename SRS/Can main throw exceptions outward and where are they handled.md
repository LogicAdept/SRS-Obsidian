<!--
reps: 0
priority: 0
-->
#Java/Exceptions/Checked #Java/Exceptions/Unchecked #Java/Concurrency/Threads #SRS

# Can `main` throw exceptions outward and where are they handled?

> [!abstract] Short answer
> **Yes.** `main` may declare `throws` (including checked types) and let an exception leave. There is no special “launcher catch.” If nothing in that thread catches it, the **main thread** is terminated after its **uncaught exception handler** runs — by default a stack trace on the standard error stream.

## `main` is an ordinary method on the initial thread

A candidate `main` may have a `throws` clause. Checked exceptions still need `catch` or `throws`, same as any method ([[What happens if you neither catch nor declare a checked exception]], [[Can a constructor throw a checked exception]]). Unchecked exceptions and `Error` need no `throws`.

If the throw is not caught in `main` (or a caller — there is none above `main`), the thread that ran `main` is terminated. Before that, `finally` blocks on the way out still run. Then the JVM invokes that thread’s `UncaughtExceptionHandler`. If none was set on the thread, the thread’s `ThreadGroup` handles it; with the usual group that means the **default** handler, which prints the thread name and `printStackTrace` to **standard error** ([[What happens if no catch matches and a finally block is present]], [[How many catch blocks execute for one thrown exception]]).

That is the same uncaught path as any other thread. Installing `Thread.setDefaultUncaughtExceptionHandler` (or a per-thread handler) replaces the default print. Exceptions thrown **from the handler itself** are ignored.

The process does not always end the instant `main` throws. The VM exits when **all non-daemon threads** have terminated (or someone calls `System.exit` / `Runtime.halt`). Other non-daemon threads keep the program alive after the main thread dies.

```d2
direction: down
main: "main throws\n(no matching catch)" {
  width: 280
  height: 70
}
fin: "enclosing finally blocks run" {
  width: 280
  height: 50
}
ueh: "UncaughtExceptionHandler\n(default: stack to stderr)" {
  width: 300
  height: 70
  style.fill: "#fff8e1"
}
term: "main thread terminates" {
  width: 280
  height: 50
}
exit: "VM exits if no other\nnon-daemon threads" {
  width: 280
  height: 70
}
main -> fin -> ueh -> term -> exit
```

**Fig. 1.** An exception leaving `main` is uncaught on the initial thread, not caught by the launcher.

```java
class Demo {
    public static void main(String[] args) throws Exception {
        if (args.length == 0) {
            throw new Exception("need args");
        }
    }
}
```

**Listing 1.** `main` may declare `throws Exception`. With no `catch`, the checked exception leaves the initial thread; the default uncaught handler prints a stack trace to standard error, then that thread ends.

> [!warning] `throws` on `main` is not a free pass at compile time
> A checked exception that `main` can throw must still be declared or caught. The launcher does not exempt `main` from the checked-exception rules.

> [!warning] The default handler is not a `catch` in your code
> After the handler, that thread is dead. Other non-daemon threads can keep the JVM running. Do not assume the process always exits solely because `main` threw.

> [!tip] Interview answer
> **Yes — `main` can throw, including checked types if it declares them.** Nothing above `main` catches it. The initial thread’s uncaught exception handler runs — usually a stack trace on stderr — then that thread terminates. The JVM stays up if other non-daemon threads are still alive.
