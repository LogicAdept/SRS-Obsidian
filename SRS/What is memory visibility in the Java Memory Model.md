<!--
reps: 0
priority: 0
-->
#Java/JMM #SRS

# What is memory visibility in the Java Memory Model

> [!abstract] Short answer
> **Memory visibility is the question "if thread T1 wrote a value, when is thread T2 guaranteed to read that value?"** The JMM's answer: only when an happens-before edge connects the write to the read — via `volatile`, monitor lock/unlock, thread `start`/`join`, and their transitive combinations. Without an edge, the read may return the default value, an old value, or the new one — every outcome is legal.

## Why staleness is legal in the first place

The model does not promise that every write is pushed instantly everywhere. Conceptually each thread works with its own view of memory, and the JVM is free to keep values in registers or caches, or to reorder work, so long as single-thread semantics look unchanged. The cost of that freedom is: a plain read has *no* obligation to see a concurrent plain write.

```d2
direction: right
t1: "T1\ndata = 42" {
  width: 220
  height: 80
  style.fill: "#e3f2fd"
}
edge: "Visibility requires an edge\nvolatile w/r | monitor unlock/lock\nstart() | join()" {
  width: 340
  height: 110
  style.fill: "#fff3e0"
}
t2: "T2 reads data" {
  width: 220
  height: 80
  style.fill: "#fff3e0"
}
ok: "Edge present\n-> sees 42" {
  width: 200
  height: 80
  style.fill: "#e8f5e9"
}
stale: "No edge\n-> 0, 42, anything legal" {
  width: 290
  height: 80
  style.fill: "#ffebee"
}
t1 -> edge
edge -> t2
t2 -> ok: "guaranteed"
t2 -> stale: "data race"
```

**Fig. 1.** Visibility is binary on the happens-before relation: either an edge orders write before read, or every value is legal.

```java
public class HappensBeforeDemo {
    static int data;                 // plain field
    static volatile boolean ready;   // volatile flag

    public static void main(String[] args) throws Exception {
        Thread writer = new Thread(() -> {
            data = 42;
            ready = true;
        });
        writer.start();

        int stale = 0, tries = 2_000;
        for (int t = 0; t < tries; t++) {
            data = 0; ready = false;
            Thread w = new Thread(() -> { data = 42; ready = true; });
            w.start();
            while (!ready) { /* volatile spin */ }
            if (data != 42) stale++;
            w.join();
        }
        System.out.println("reads after volatile flag: stale " + stale + " out of " + tries);
    }
}
```

**Listing 1.** Verified on JDK 21:

```java
reads after volatile flag: stale 0 out of 2000
```

**Listing 2.** Two thousand writer-reader exchanges, zero stale reads — because the reader's volatile read of `ready` synchronizes-with the volatile write, dragging the earlier plain `data` write into the visible past. The volatile edge, not the timing, produces the guarantee.

## The practical menu of edges

Everyday ways to make a write visible: declare the field `volatile` (flag-style publication), do read/write inside the same monitor (the lock edge), publish through `final` fields of a properly constructed object, hand values across `start()`/`join()` or an `ExecutorService` future (`get()`), or use `java.util.concurrent` structures whose methods carry the same semantics. The exact edge algebra is in [[How would you explain the happens-before guarantee in the Java Memory Model]] and [[How does the Java Memory Model define visibility and ordering]].

> [!warning] Visibility fixes staleness only — it never fixes lost updates
> The classic interview lie is "make it volatile and it's thread-safe". A volatile write is visible immediately, but two threads still interleave a read-modify-write and lose updates ([[Why is the Java increment operator not atomic]]); and the guarantee is *only* about values crossing the edge — code that reads the shared state before establishing the edge still races. Conversely, the absence of visible staleness in testing proves nothing: an x86 server often hides reordering that an ARM box or the JIT will expose later, because the race is in the specification space, not something a test reliably reproduces. Race condition versus data race terminology: [[What is the difference between a race condition and a data race]].

> [!tip] Interview answer
> **Memory visibility is when one thread's write is guaranteed to be seen by another. The JMM's rule: visible only along happens-before — volatile write/read, monitor unlock/lock, start/join, transitively. Without such an edge the reader may legally see a stale or default value, because caches, registers and reordering are all permitted. Visibility makes stale reads impossible; it does not make compound operations atomic — that needs CAS or locks.**

