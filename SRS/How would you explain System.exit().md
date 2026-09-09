<!--
reps: 0
priority: 0
-->
#Java/Runtime #SRS

# How would you explain System.exit()

> [!abstract] Short answer
> `System.exit(n)` initiates the JVM shutdown sequence with status code `n` and never returns — it neither completes normally nor throws. By convention nonzero means abnormal termination. It is effectively `Runtime.getRuntime().exit(n)`. The JVM starts all shutdown hooks, waits for them, then terminates and hands `n` to the operating system as the process exit code.

Two details of the Java 21 contract matter. First, `exit` is **serialized**: only the first successful invocation initiates the sequence and terminates the VM with its status; every later invocation performs no action and blocks indefinitely. Second, the method that triggers the sequence is irrelevant — normal termination (the last non-daemon thread finishes, see [[How would you explain daemon threads in Java]]), `System.exit`, or an external signal all funnel into the same shutdown sequence.

## What runs and what does not

Calling `System.exit` from the middle of a method abandons that call stack: the method does not complete, `finally` clauses of frames below are never popped into action, and try-with-resources closes nothing for the caller. What does run is the shutdown machinery: registered hooks, started concurrently, then JVM termination with your status.

```d2
direction: right
call: "System.exit(3)" {
  width: 200
  height: 70
  style.fill: "#fff3e0"
}
seq: "Shutdown sequence starts\nhooks run concurrently" {
  width: 260
  height: 100
  style.fill: "#e3f2fd"
}
term: "JVM terminates\nprocess exit code = 3" {
  width: 260
  height: 100
  style.fill: "#e8f5e9"
}
skip: "Caller frames abandoned:\nno finally, no resource close" {
  width: 300
  height: 100
  style.fill: "#ffebee"
}
call -> seq
seq -> term
call -> skip
```

**Fig. 1.** `exit` switches from your call stack to the shutdown sequence; the code after the call never executes.

```java
public class ExitStatusDemo {
    public static void main(String[] args) {
        System.out.println("before exit");
        try {
            System.exit(3);
        } finally {
            System.out.println("finally never runs after System.exit");
        }
    }
}
// Output (JDK 21):
// before exit
// (process exit code: 3)
```

**Listing 1.** The `finally` block is skipped because `exit` never returns; the status code is still delivered to the OS.

> [!warning] "finally always runs" is a lie
> A `finally` block runs when control leaves the `try` block — but `System.exit` prevents control from ever leaving: the calling thread parks inside `exit` until the JVM terminates. Relying on `finally` or try-with-resources to flush state across an `exit` call is a classic production bug; put that flush into a shutdown hook instead, see [[What is a JVM shutdown hook]].

The halt-shaped sibling that skips hooks entirely is compared in [[What is the difference between System.exit and Runtime.halt]], and calling `exit` from inside a hook has its own trap in [[What happens if you call System.exit from a shutdown hook]].

> [!tip] Interview answer
> `System.exit(n)` starts the JVM shutdown sequence and blocks forever — it never returns. Registered shutdown hooks run, then the JVM terminates with exit code `n`; nonzero conventionally means failure. Since it abandons the call stack, `finally` and try-with-resources around the call do not execute — only shutdown hooks get a chance to clean up.

