<!--
reps: 0
priority: 0
-->
#Java/JMM #SRS

# What is the program order rule in the Java Memory Model

> [!abstract] Short answer
> **Within one thread, actions in source order are ordered: if action x comes before action y in the program order of the same thread, then `hb(x, y)` (JLS 17.4.5).** Everything a thread writes before some point in its own code is visible to its own later reads — this is the as-if-serial guarantee, and it holds even without any synchronization.

The rule is the first edge generator of the happens-before relation. It is deliberately local: it connects actions **of the same thread only**. The compiler and CPU may still reorder, buffer, or overlap the underlying machine operations, but the observable result of that thread's execution must be indistinguishable from sequential execution of the source — the model calls this appearing **as-if-serial** (JLS 17.4.3). What program order never gives is any promise across threads: two independent threads have no happens-before edges between them until something from the synchronizes-with list connects them ([[What is the synchronizes-with relation in the Java Memory Model]]).

```d2
direction: right
t1: "Thread 1" {
  width: 200
  height: 74
  a: "x = 1" {
    width: 200
    height: 74
    style.fill: "#e3f2fd"
  }
  b: "y = 2" {
    width: 200
    height: 74
    style.fill: "#e3f2fd"
  }
  a -> b: "hb: program order"
}
t2: "Thread 2" {
  width: 200
  height: 74
  r: "reads x and y" {
    width: 200
    height: 74
    style.fill: "#fff3e0"
  }
}
t1 -> t2: "no edge: no guarantee" { style.stroke: "#c62828"; style.stroke-dash: 4 }
```

**Fig. 1.** Program order creates edges inside Thread 1 only. Without a synchronizes-with edge into Thread 2, its reads are data races and may see 0, 1, 2, or the write of `y` before the write of `x`.

```java
int x;
int y;

// thread 1
x = 1;
y = 2;
// thread 1 reading x here is guaranteed to see 1:
// hb(x = 1, this read) by program order

// thread 2 (no synchronization)
int r1 = x;   // may see 0 — no edge from thread 1
int r2 = y;   // may see 0 too, even "after" x = 1 in wall time
```

**Listing 1.** Same-thread reads are safe by program order; cross-thread reads are unordered. Adding `sleep` or `yield` in thread 1 changes nothing — these methods create no happens-before edges.

> [!warning] Program order is not an inter-thread promise
> The most common misreading of the rule is "the other thread will see my writes because my source lines are in order". The model allows every action of one thread to be reordered relative to another thread unless an edge connects them, and a read may even observe the default value after the "obviously earlier" write. Ordering across threads needs a synchronizes-with edge — monitor unlock→lock, a volatile write→read, or the thread lifecycle rules ([[What is the volatile visibility rule in the Java Memory Model]], [[What is the thread start rule in the Java Memory Model]]). Without it the pair of conflicting accesses is a data race ([[What is the difference between a race condition and a data race]]).

> [!tip] Interview answer
> **The program order rule says that in a single thread, if action x precedes action y in source order, then x happens-before y — so each thread always sees its own writes and behaves as-if-serial. It is purely intra-thread: it never orders actions of different threads, so cross-thread visibility needs additional synchronizes-with edges, which happen-before then combines with program order transitively.**
