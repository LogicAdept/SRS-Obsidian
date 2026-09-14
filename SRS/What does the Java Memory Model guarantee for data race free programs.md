<!--
reps: 0
priority: 0
-->
#Java/JMM/HappensBefore #Java/Concurrency #SRS

# What does the Java Memory Model guarantee for data race free programs

> [!abstract] Short answer
> **DRF-SC: a program is correctly synchronized if and only if all sequentially consistent executions are free of data races, and if a program is correctly synchronized, then all of its executions appear sequentially consistent (JLS 17.4.5).** Get the happens-before edges right and the compiler, JIT, and CPU reorderings become invisible — the program behaves like a simple interleaving.

This is the headline guarantee the model makes to programmers. The definition is per program, not per run: check whether every pair of conflicting accesses — two accesses to the same variable, at least one a write — is ordered by happens-before in every sequentially consistent execution. If yes, no execution of the real program on real hardware can observe any reordering, buffering, or cache staleness: every result is explainable as some interleaving of threads' source-level actions ([[What is ordering as-if-serial semantics sequential consistency visibility atomicity happens-before mutual excl]]). Practically, that means you never reason about caches, store buffers, or instruction pipelines — you only reason about which edges exist ([[How would you explain the happens-before guarantee in the Java Memory Model]]).

```d2
direction: right
ok: "Every conflicting pair\nordered by hb?" {
  width: 258
  height: 104
  yes: "correctly synchronized\n-> all executions appear\nsequentially consistent" {
    width: 276
    height: 134
    style.fill: "#e8f5e9"
  }
  no: "a data race exists\n-> no DRF-SC guarantee;\nreads may see defaults\nor any racing write" {
    width: 267
    height: 164
    style.fill: "#ffebee"
  }
  ok -> yes: "yes"
  ok -> no: "no"
}
```

**Fig. 1.** The DRF-SC dichotomy: one un-ordered conflicting pair anywhere drops the program out of the strong guarantee and into the much weaker happens-before-consistency rules ([[What reads does the Java Memory Model allow in a data race]]).

```java
class Counter {
    private int count;                       // conflicting accesses: race
    private volatile boolean closed;         // ordered accesses: fine

    void inc() { count++; }                  // race with any other inc/read
    int get() { return count; }              // race with inc
    void close() { closed = true; }          // volatile write: ordered
    boolean isClosed() { return closed; }    // volatile read: ordered
}
```

**Listing 1.** The volatile pair is correctly synchronized, but the single `count` field makes the whole program not correctly synchronized — DRF-SC is all-or-nothing, so `get()` may return stale values even though the flag logic is clean. Making `count` an `AtomicInteger` (or locking both methods) restores the guarantee.

> [!warning] The guarantee is fragile at the program level
> A single un-ordered conflicting access is enough to lose DRF-SC for the *entire* program — races do not stay local, because the optimizer is free to reorder code far away from the missing edge ([[Is there a universal fix for race conditions in concurrent code]]). Note also the split between what the guarantee covers and what it does not: sequential consistency of the memory picture says nothing about atomicity of compound actions or about logic bugs like check-then-act on properly visible values ([[Why is the Java increment operator not atomic]]).

> [!tip] Interview answer
> **The JMM's headline guarantee is DRF-SC: if all conflicting accesses are ordered by happens-before — the program is correctly synchronized — then every execution appears sequentially consistent, and you can ignore hardware and compiler reordering entirely. One data race anywhere breaks the program out of this guarantee, which is why visibility review is about finding missing edges, not tolerating races.**
