<!--
reps: 0
priority: 0
-->
#Java/JMM #SRS

# What is ordering as-if-serial semantics sequential consistency visibility atomicity happens-before mutual excl?

> [!abstract] Short answer
> A **glossary** of Java memory-model words. **Intra-thread** (“as-if-serial”): **one** thread looks sequential. **Sequential consistency**: a **global** interleaving of **all** threads’ program orders — Java **promises that appearance only if there are no data races**. **Happens-before** is the **visibility and ordering** relation between actions. **Atomicity** is “no torn / partial result,” not “`i++` is one step.” **Mutual exclusion** is **one owner** of a monitor. **Safe publication** means later readers see a **fully initialized** object via those edges. JMM: [[How does the Java Memory Model define visibility and ordering]]. HB: [[How would you explain the happens-before guarantee in the Java Memory Model]]. Visibility: [[What is memory visibility in the Java Memory Model]]. Race vs data race: [[What is the difference between a race condition and a data race]]. `volatile` vs `i++`: [[How does volatile visibility differ from atomicity for compound updates]].

## Intra-thread vs global vs happens-before

**Ordering:** compilers and CPUs **reorder**. The model still requires **intra-thread semantics**: inside one thread, reads see what that thread’s own program would see. That local guarantee is what interviews call **as-if-serial**. It is **not** sequential consistency.

**Sequential consistency:** there is a **total order** of all actions consistent with **every** thread’s **program order**, and each read sees the **latest** write in that order. **Correctly synchronized** programs (no data race in any SC execution) **appear** sequentially consistent. A **data race** (conflicting accesses **not** ordered by happens-before) **drops** that appearance.

**Happens-before (`hb`):** if `hb(x, y)`, then `x` is **visible to** and **ordered before** `y`. It is **program order** plus **synchronizes-with** (unlock → later lock of the **same** monitor; **volatile** write → later read; `start` → the new thread; and so on), **transitively**. It does **not** mean the chip executed `x` then `y`.

**Visibility:** a write is usable in another thread when **happens-before** (or the extra **final**-field freeze rules) says so — not because you assigned a field.

**Atomicity:** a single write/read of a **reference**, `int`, etc. is one action. A **non-volatile `long`/`double`** write **may** be **two 32-bit** writes (torn read). **`i++` is not atomic.** Groups of operations need a **lock** (or an atomic API) if they must look like one step.

**Mutual exclusion:** **one** thread **owns** an object’s monitor (`synchronized`). It **excludes** other lockers of **that** object; it does **not** freeze unsynchronized fields.

**Safe publication:** make the new object reachable only after initialization, with a happens-before edge to the readers: **class initialization** (`static` fields), a **volatile**/atomic write of the reference, unlocking a monitor that protected the write, or **`final`** fields after the constructor returns.

```java
int x;
volatile boolean ready;

void publish() { x = 1; ready = true; }           // volatile write
int take() { return ready ? x : -1; }             // later read: sees x == 1
```

**Listing 1.** `ready`’s write happens-before a later read, so `x = 1` is visible. Without `volatile` (or a lock), `take` may see `ready == true` and `x == 0`.

```d2
direction: down
intra: "intra-thread / as-if-serial" {
  width: 240
  height: 40
  style.fill: "#fff8e1"
}
sc: "sequential consistency (no data races)" {
  width: 300
  height: 40
  style.fill: "#e8f5e9"
}
hb: "happens-before: visibility + order" {
  width: 280
  height: 40
  style.fill: "#e3f2fd"
}
intra -> sc: "not the same"
hb -> sc: "DRF programs appear SC"
```

**Fig. 1.** One-thread sequential look is weaker than a global interleaving. Happens-before is what you actually program.

> [!warning] Sequential consistency ≠ as-if-serial
> As-if-serial is **per thread**. Sequential consistency is **all threads**. Equating them is the usual wrong glossary.

> [!warning] Happens-before is not a CPU trace
> Reordering is legal if the execution still satisfies the model. Data-race reads can see **stale or surprising** values.

> [!tip] Interview answer
> As-if-serial means one thread still looks sequential while the machine reorders. Sequential consistency is a global interleaving, and Java only promises that look when there are no data races. Between threads, visibility and order come from happens-before, and atomicity is a separate question from a compound update like increment.
