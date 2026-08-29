<!--
reps: 0
priority: 0
-->
#Java/JMM #Java/Concurrency #SRS

# Why does the Java Memory Model matter for concurrency?

> [!abstract] Short answer
> Threads share **heap** memory (fields, array elements — **not** locals). Compilers, JITs, and CPUs may **reorder** and cache those writes. The memory model is the **contract** for which write a read is **allowed** to see. Without a **happens-before** edge, conflicting accesses are a **data race** and “impossible” values are legal. With **no data races**, you may reason as if the program were **sequentially consistent** — still not a free pass for `get`+`put`. HB: [[How would you explain the happens-before guarantee in the Java Memory Model]]. Race vs data race: [[What is the difference between a race condition and a data race]]. Why threads at all: [[Why do we need concurrency]].

## Visibility is not “it ran earlier”

An implementation may produce **any** code whose executions stay inside the model, including **reordering** and dropping “unnecessary” synchronization. Intra-thread semantics still hold; **values seen by reads** are what the model decides.

**Happens-before** is the programmer-facing order: if *x* happens-before *y*, then *x* is **visible to** and **ordered before** *y*. Same-thread program order; **synchronizes-with** (unlock → later lock on the **same** monitor; volatile write → later read of **that** field; `start` → first action in the new thread; thread end → successful `join`); transitivity. That edge is **not** a promise the machine executed *x* first — only that observed results match a legal execution. Writes in a data race may appear **out of order** to the racing reads.

**Data race:** two **conflicting** accesses (same variable, at least one write) **not** ordered by happens-before. A program is **correctly synchronized** iff every sequentially consistent execution is data-race-free; then **all** executions **appear** sequentially consistent. You do **not** have to reason about reorderings to *find* races — but correct sync does **not** make the *program* correct. Groups of operations that must look atomic still fail if they are not one protocol. Volatile visibility vs `i++`: [[How does volatile visibility differ from atomicity for compound updates]]. Volatile on a reference: [[What does volatile on a reference field guarantee for visibility]].

j.u.c **extends** the same edges: submit → run; task → `Future.get()`; put into a concurrent collection → later take; `unlock` / `release` / `countDown` → matching acquire. Toolbox: [[How would you explain the java.util.concurrent package]].

**`final` fields:** after the constructor finishes, another thread that only sees the published reference is guaranteed the **initialized `final`s** (and contents they refer to, at least that up-to-date). A plain `int` next to them can still be **default `0`**. Do not leak `this` before the constructor ends. Immutable objects: [[How would you explain immutability and its benefits in Java]].

```java
class SurprisingReorder {
    static int a, b; // initially 0

    static void thread1() {
        int r2 = a;
        b = 1;
        use(r2);
    }

    static void thread2() {
        int r1 = b;
        a = 2;
        use(r1);
    }

    static void use(int ignored) {}
}
```

**Listing 1.** No happens-before between the writes and the other thread’s reads. `r2 == 2` and `r1 == 1` looks absurd in program order; a compiler may swap each thread’s two statements, and that result is **allowed**. Add a shared monitor, `volatile`, or a j.u.c edge if you need it forbidden.

```d2
direction: down
share: "shared field / array slot" {
  width: 220
  height: 36
  style.fill: "#fff8e1"
}
race: "conflicting access, no HB" {
  width: 240
  height: 40
  style.fill: "#ffebee"
}
ok: "HB edge: lock, volatile, start/join, j.u.c" {
  width: 280
  height: 40
  style.fill: "#e8f5e9"
}
sc: "appears sequentially consistent" {
  width: 240
  height: 36
  style.fill: "#e3f2fd"
}
share -> race: "data race"
share -> ok: "correctly synchronized"
ok -> sc: "then reason SC"
```

**Fig. 1.** The model matters because **shared** locations have **no** default inter-thread order. You either have a happens-before story or you have a data race.

> [!warning] Happens-before is not wall-clock order
> An HB edge does **not** force the CPU to run *x* before *y*. It constrains **what a read may observe**. Racing reads can still see writes **out of order**. Locals are not in this game; fields and array elements are.

> [!warning] Data-race-free is not “my check-then-act is atomic”
> Sequential consistency still allows bugs in **groups** of operations that are not one atomic step. `volatile` is not `i++`. `synchronized` on the wrong object does not order the field you meant. `final` *x* does not freeze neighboring *y*.

> [!tip] Interview answer
> The Java Memory Model is why another thread might not see my write, and why compilers are allowed to make that look impossible. I treat happens-before as the visibility contract: no edge between conflicting accesses is a data race. If there are no data races I reason as if sequentially consistent, but I still make compound updates one atomic protocol, not a volatile hope.
