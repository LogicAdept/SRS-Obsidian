<!--
reps: 0
priority: 0
-->
#Java/JMM #SRS

# How would you explain memory Java

> [!abstract] Short answer
> The filename is garbled; the question is the **Java Memory Model**: when one thread’s **writes** become **visible** and **ordered** for another. The spec is **happens-before**, not a required “working memory vs main memory” machine. If **hb(x, y)**, then **x** is visible to and ordered before **y**. Intra-thread **program order**; **unlock** of a monitor **hb** later **lock** of the **same** monitor; **volatile write hb later read** of **that** field; **`start` hb** the new thread’s actions; a thread’s **last action hb** another thread **detecting termination** (`join` / `isAlive`); **interrupt hb** observing that interrupt. Transitive. Visibility: [[What is memory visibility in the Java Memory Model]]. HB list: [[How would you explain the happens-before guarantee in the Java Memory Model]]. Ordering: [[How does the Java Memory Model define visibility and ordering]].

## Happens-before, not a hidden cache API

Threads communicate through **shared variables**, **monitors**, **volatiles**, **starting/joining** threads, and **interruption**. Compilers and CPUs may **reorder** so long as each thread’s own sequential semantics hold and the HB edges are respected. There is **no** rule that “the rest of the universe” sees a write. A third thread needs its **own** HB path.

**`synchronized`:** unlocking **m** hb a later lock of **m**. Everything the first thread did in program order before the unlock is then ordered before what the second does after the lock. Different monitors do **not** link.

**`volatile`:** a write to **v** hb a later read of **v**. Together with program order, that is how a volatile **flag** can publish earlier plain writes. It does **not** make `count++` one action — [[How does volatile visibility differ from atomicity for compound updates]].

**`final`:** after a constructor **finishes**, and the reference was not published early, other threads that only see the object **then** see those finals — [[How would you explain immutability and its benefits in Java]]. Reflection can still rewrite finals; that is a special, easy-to-get-wrong case.

Heap vs stack is **where** bytes live (JVMS), not this visibility spec — [[How would you explain the two main JVM memory regions stack and heap]].

```java
final class Publish {
    int data;
    volatile boolean ready;
    void writer() { data = 1; ready = true; }
    int reader() { return ready ? data : -1; }
}
```

**Listing 1.** If `reader` sees `ready == true`, HB gives it `data == 1`. A plain `boolean ready` would not.

```d2
direction: down
po: "program order\nin one thread" {
  width: 220
  height: 45
  style.fill: "#e3f2fd"
}
sw: "synchronizes-with\n(unlock, volatile, start, join, interrupt)" {
  width: 340
  height: 55
  style.fill: "#fff8e1"
}
hb: "happens-before\n(transitive)" {
  width: 220
  height: 45
  style.fill: "#e8f5e9"
}
po -> hb
sw -> hb
```

**Fig. 1.** Visibility is the transitive closure of program order and synchronization.

> [!warning] “Main memory vs thread-local copies” is teaching fiction
> The language does **not** require a working-memory cache. Implementations may use registers and caches; the **programmer contract** is happens-before.

> [!warning] Volatile is not a global fence and not atomic RMW
> Same-field write/read is the volatile edge. Two volatiles, or a volatile plus `++`, still follow the usual compound-action rules.

> [!tip] Interview answer
> The Java Memory Model says when writes in one thread are visible to another, using happens-before. Unlocking a monitor, writing a volatile, starting a thread, and joining all create those edges. I do not explain it as each thread having a private copy of the heap; I explain the edges I actually get from synchronized, volatile, and start/join.
