<!--
reps: 0
priority: 0
-->
#Java/JMM #SRS

# What is the synchronizes-with relation in the Java Memory Model

> [!abstract] Short answer
> **Synchronizes-with is the cross-thread edge relation of the JMM (JLS 17.4.4): monitor unlock→lock, volatile write→read, thread start→first action, default-value write→first action in every thread, termination detection, and interrupt detection. The source of an edge is called a release, the destination an acquire, and every synchronizes-with edge also becomes a happens-before edge.**

Happens-before is built from exactly two ingredients: program order inside a thread (JLS 17.4.5) and this synchronizes-with relation between threads, closed under transitivity. That decomposition is the practical tool for reasoning: to prove visibility you hunt for the synchronizes-with edges in the code — every use of `synchronized`, `volatile`, `start`, `join`, `interrupt`, or a j.u.c synchronizer plants one ([[What is the monitor lock rule in the Java Memory Model]], [[What is the volatile visibility rule in the Java Memory Model]]). The release/acquire terminology is deliberate: a release publishes everything the releasing thread did before the edge; an acquire makes it visible to everything after the edge on the receiving side.

```d2
direction: right
graph: {
  monitor: "monitor unlock -> lock\n(same monitor)" { style.fill: "#e3f2fd" }
  vol: "volatile write -> read\n(same variable)" { style.fill: "#e3f2fd" }
  start: "start() -> first action\nof the new thread" { style.fill: "#e3f2fd" }
  def: "default-value write\n-> first action in any thread" { style.fill: "#e3f2fd" }
  term: "final action of T1 ->\ndetection in T2 (join, isAlive)" { style.fill: "#e3f2fd" }
  intr: "interrupt() ->\ndetection of interruption" { style.fill: "#e3f2fd" }
}
note: "sw(x, y) implies hb(x, y);\nhb = program order + sw, transitively closed" { style.fill: "#e8f5e9" }
```

**Fig. 1.** The complete synchronizes-with catalogue from JLS 17.4.4. Every higher-level j.u.c guarantee (executors, concurrent collections, latches, barriers) is expressed in terms of these basic edges plus program order.

```java
// each statement plants one synchronizes-with edge
synchronized (m) { queue.add(x); }   // unlock(m) -> next lock(m): release
boolean r = ready;                   // prior volatile write -> this read: acquire
t.start();                           // -> first action inside t
t.join();                            // final action of t -> return of join
worker.interrupt();                  // -> InterruptedException / isInterrupted()
```

**Listing 1.** The same five lines as an edge inventory — code review for visibility bugs is mostly checking which of these edges connect each producer-consumer pair.

> [!warning] Synchronizes-with is cross-thread by definition
> Program order is not a synchronizes-with edge — it is the separate intra-thread ingredient of happens-before, and confusing the two leads to wrong conclusions like "my write is visible because it is in program order with my unlock" (that one is true only *after* transitivity merges the two relations). Also note the edges are pairwise on actions, not on threads: an unlock orders against the *next* lock of the same monitor, a volatile write against *subsequent* reads of the same variable — different monitors or different variables give nothing ([[How would you explain the happens-before guarantee in the Java Memory Model]]).

> [!tip] Interview answer
> **Synchronizes-with is the set of cross-thread edges defined in JLS 17.4.4 — monitor unlock to lock, volatile write to read, thread start, default-value write, termination detection, interrupt detection — with the source called release and the destination acquire. Each such edge is also a happens-before edge, and happens-before is the transitive closure of synchronizes-with plus program order. All j.u.c guarantees are built on these basic edges.**
