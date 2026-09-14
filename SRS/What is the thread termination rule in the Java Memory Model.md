<!--
reps: 0
priority: 0
-->
#Java/JMM/HappensBefore #Java/Concurrency/Threads #SRS

# What is the thread termination rule in the Java Memory Model

> [!abstract] Short answer
> **The final action in a thread synchronizes-with any action in another thread that detects its termination — by `join()` returning or `isAlive()` returning false (JLS 17.4.4).** All actions the terminated thread ever performed are visible to the thread that successfully joins it.

This is the receiving half of the thread lifecycle: results computed in a worker are safely published to the caller at the moment `join()` returns, with no locks or volatile fields needed ([[What is the thread start rule in the Java Memory Model]]). The detection can be indirect — any observation that the thread is gone counts, including `isAlive() == false` checked from any thread. The JDK implementation matches the spec: `join(long)` synchronizes on the thread object and waits in a loop `while (isAlive())`, relying on a `notifyAll` that fires when the thread terminates, so the detection itself goes through monitor lock/unlock actions — extra edges on top of the spec's termination edge.

```d2
direction: right
w: "Worker thread" {
  width: 200
  height: 74
  c: "compute result\n(plain writes)" {
    width: 200
    height: 104
    style.fill: "#e3f2fd"
  }
  f: "final action in run()" {
    width: 249
    height: 74
    style.fill: "#fff3e0"
  }
  c -> f: "program order"
}
m: "Main thread" {
  width: 200
  height: 74
  j: "worker.join()\n(detects termination)" {
    width: 249
    height: 104
    style.fill: "#fff3e0"
  }
  r: "reads result\n-> fully visible" {
    width: 204
    height: 104
    style.fill: "#e8f5e9"
  }
  j -> r: "program order"
}
f -> j: "synchronizes-with\n(termination detected)"
```

**Fig. 1.** Every action of the worker is ordered before the joiner's read through the single termination-detection edge — the classic "fork, compute, join, read" pattern needs no other synchronization.

```java
long result = 0;

Thread worker = new Thread(() -> {
    result = expensiveComputation();   // plain write
});

worker.start();
worker.join();                          // returns only when the worker is done
System.out.println(result);             // guaranteed to see the computed value
```

**Listing 1.** `join()` publishes the worker's entire output: after a successful join, the parent sees every write the worker made, including plain-field ones.

> [!warning] A timeout return is not detection of termination
> The edge is delivered when the joiner *detects* termination. `join(timeout)` can return because the timeout expired while the worker is still alive — in that case no termination was detected, no edge is delivered, and reading the worker's fields is a data race. Check `isAlive()` after a timed join before trusting its writes. Two more traps: joining an already-terminated thread still detects termination and delivers the edge, and `Thread.sleep` inside the worker does nothing for visibility — edges need detection, not time ([[How does Thread.join work in Java]], [[What is the difference between wait and sleep]]).

> [!tip] Interview answer
> **All actions in a thread happen-before any other thread that detects its termination — via `join()` returning successfully or `isAlive()` returning false. So a joiner sees the full output of the terminated thread without extra synchronization. A timed join that returns due to timeout does not detect termination and gives no edge, which is the usual interview trap.**

