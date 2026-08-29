<!--
reps: 0
priority: 0
-->
#Java/Concurrency/Threads #Java/Exceptions/Checked #SRS

# How would you explain `InterruptedException` in Java threads?

> [!abstract] Short answer
> **It is a checked exception meaning “this blocking call ended because the thread was interrupted.”** `sleep`, `wait`, `join`, and similar methods throw it after **clearing** the interrupt status. Catching it and doing nothing loses the interrupt. Rethrow it, or call `Thread.currentThread().interrupt()` before you continue or wrap it.

## Interrupt is a request, `InterruptedException` is the blocking reply

`Thread.interrupt()` sets the thread’s **interrupt status** — a request to stop or cancel the current work. If the thread is in `sleep`, `wait`, or `join`, that status is **cleared** and the method throws `InterruptedException`. If it is not in one of those calls, the flag is just set; later `sleep` still throws once the thread notices ([[What is the difference between interrupted and isInterrupted in Java]], [[What is ThreadDeath]]).

Because `InterruptedException` extends `Exception` (not `RuntimeException`), methods that call `sleep` must `catch` or declare `throws` ([[What happens if you neither catch nor declare a checked exception]], [[How do you handle exceptions in Java applications]]).

The blocking method **clears** the flag before throwing. An empty `catch` means later code sees “not interrupted.” Official guidance: **rethrow**, or **restore** with `Thread.currentThread().interrupt()`, then continue or wrap in another exception. If you wrap, restore the flag **before** throwing the wrapper ([[How do you propagate an exception up the call stack in Java]]).

Non-blocking work can poll `Thread.interrupted()` (clears the flag) or `isInterrupted()` (does not). `Runnable.run` cannot declare `throws InterruptedException`, so people wrap — still restore the status.

I/O on an interruptible channel is different: `ClosedByInterruptException` and the interrupt status stays **set**.

```d2
direction: down
irq: "interrupt()" {
  width: 260
  height: 50
}
sleep: "sleep / wait / join" {
  width: 280
  height: 50
}
ie: "InterruptedException\nstatus cleared" {
  width: 300
  height: 70
  style.fill: "#fff8e1"
}
fix: "rethrow or interrupt() again" {
  width: 300
  height: 50
  style.fill: "#e8f5e9"
}
irq -> sleep -> ie -> fix
```

**Fig. 1.** Blocking interruptible methods convert the flag into a checked exception and clear it.

```java
class Demo {
    static void pause() {
        try {
            Thread.sleep(1000);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }
}
```

**Listing 1.** After `sleep` throws, the interrupt flag is already false. Restoring it lets callers still see the interrupt. Swallowing without `interrupt()` hides it.

> [!warning] Empty `catch (InterruptedException e) {}` is a bug
> The status was cleared to throw. If you do not restore or rethrow, cancellation is lost.

> [!warning] Wrapping without restoring is the same bug
> `throw new RuntimeException(e)` without `interrupt()` first still leaves the thread looking un-interrupted.

> [!tip] Interview answer
> **`InterruptedException` means a blocking call (`sleep`, `wait`, `join`) noticed `interrupt()`.** It is checked, and the interrupt flag is cleared when it is thrown. Catch and rethrow, or restore with `Thread.currentThread().interrupt()` — never swallow it.
