<!--
reps: 0
priority: 0
-->
#Java/JMM #Java/Concurrency/Threads #SRS

# What is the interrupt happens-before rule in the Java Memory Model

> [!abstract] Short answer
> **If thread T1 interrupts thread T2, the interrupt synchronizes-with any point where any other thread — including T2 itself — determines that T2 has been interrupted: an `InterruptedException` being thrown, or `Thread.interrupted()` / `Thread.isInterrupted()` returning true (JLS 17.4.4).** Interrupt is therefore not only a cancellation signal but also a memory edge.

The rule makes the interruption status a legitimate communication channel: writes performed by the interrupting thread before the call become visible wherever the target observes the interruption ([[How would you explain InterruptedException in Java threads]]). This matters for graceful shutdown — a worker that catches `InterruptedException` or polls `isInterrupted()` sees the latest state of shared shutdown flags that the caller updated before calling `interrupt()`. The detection points are exhaustive in the spec: the exception, the static `interrupted()` (which also clears the flag), and the instance `isInterrupted()`; a thread that never checks any of them never reaches the acquire side of the edge.

```d2
direction: right
c: "Controller thread" {
  width: 213
  height: 74
  w: "shutdown = true\n(plain write)" {
    width: 200
    height: 104
    style.fill: "#e3f2fd"
  }
  i: "worker.interrupt()\n(release)" {
    width: 222
    height: 104
    style.fill: "#fff3e0"
  }
  w -> i: "program order"
}
wk: "Worker thread" {
  width: 200
  height: 74
  d: "catch (InterruptedException)\nor isInterrupted() == true\n(acquire)" {
    width: 312
    height: 134
    style.fill: "#fff3e0"
  }
  r: "reads shutdown -> true" {
    width: 258
    height: 74
    style.fill: "#e8f5e9"
  }
  d -> r: "program order"
}
i -> d: "synchronizes-with\n(interruption detected)"
```

**Fig. 1.** The interrupt delivers both the cancellation request and the memory edge: the worker's detection point orders its later reads after the controller's pre-interrupt writes.

```java
volatile boolean shutdownRequested; // plain field would also work here

// controller
shutdownRequested = true;           // write before the interrupt
worker.interrupt();                 // release: signal + memory edge

// worker (blocked in a blocking call)
try {
    queue.take();                   // throws InterruptedException when interrupted
} catch (InterruptedException e) {
    if (shutdownRequested) {        // guaranteed to see true
        cleanupAndExit();
    }
}
```

**Listing 1.** Flag plus interrupt: the catch block is a detection point, so the plain flag read afterwards is guaranteed to observe the controller's update even without `volatile`.

> [!warning] Detection is a precondition, and catching clears the flag
> If the target thread never checks its interruption status and never blocks in an interruptible call, no detection point is reached and the edge is never delivered — the guarantee is conditional on the acquire side ([[What is the difference between interrupted and isInterrupted in Java]]). Catching `InterruptedException` clears the flag, so a worker that swallows the exception without re-interrupting itself breaks the protocol for later detection ([[How do you stop a Java thread safely and what does safely mean]]). And interrupt is a request, not a stop: it delivers visibility and a signal, never termination by itself.

> [!tip] Interview answer
> **An interrupt by T1 synchronizes-with any detection of that interruption — the thrown `InterruptedException` or `interrupted()`/`isInterrupted()` returning true. So writes the interrupter made before the call are visible at the detection point, which makes flag-plus-interrupt a correct shutdown pattern. But the edge needs a detection point: a thread that ignores its status gets nothing, and catching the exception without re-interrupting loses the flag.**
