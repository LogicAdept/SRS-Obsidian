<!--
reps: 0
priority: 0
-->
#Java/Concurrency/Atomics #SRS

# What is the difference between compareAndSet and weakCompareAndSet?

> [!abstract] Short answer
> **`compareAndSet`:** **strong** CAS with **volatile** read/write semantics. If the witness **`==` expected**, it **succeeds** (returns `true`). **`weakCompareAndSet*`:** **may return `false` even when the value still matches** (**spurious** failure, often contention). Use **weak only in a retry loop**. On `AtomicInteger`, the old **`weakCompareAndSet` is deprecated**: it was **plain**, not volatile, despite the name — use **`weakCompareAndSetPlain`** or **`weakCompareAndSetVolatile`**. The **`compareAndSwap`** spelling is **`Unsafe`**, not `AtomicInteger`. CAS idea: [[How would you explain compare and swap CAS in concurrent algorithms]]. Atomics: [[How would you explain Java atomic types in java.util.concurrent.atomic]]. `volatile` vs atomic: [[What is the difference between volatile fields and atomic variables]]. Visibility vs RMW: [[How does volatile visibility differ from atomicity for compound updates]].

## Strong vs “possibly,” and the memory-effect trap

**`VarHandle.compareAndSet`:** if `witness == expected`, store `newValue` with **`getVolatile`/`setVolatile`**. **`false` means the witness was not expected.**

**`weakCompareAndSet` (VarHandle):** same **volatile** pair, but **`false` can be spurious**. **`weakCompareAndSetPlain`:** **plain** get/set **and** spurious fail. Acquire/release weak variants exist. **`compareAndExchange`** returns the **witness** when you need it.

**`AtomicInteger`:** `compareAndSet` → `VarHandle.compareAndSet`. Prefer **`weakCompareAndSetVolatile`** when you want weak **+** volatile. Do **not** treat deprecated **`weakCompareAndSet`** as “CAS but weaker hardware” only — it was **plain**.

On many chips the CPU instruction is the same; you still **loop** on weak and **do not** assume one-shot weak success.

```java
AtomicInteger n = new AtomicInteger(0);
n.compareAndSet(0, 1);                         // strong; volatile
int w;
do { w = n.get(); }
while (!n.weakCompareAndSetVolatile(w, w + 1)); // may fail with w still correct
```

**Listing 1.** One-shot strong CAS vs a retry loop that tolerates spurious `false`.

```d2
direction: down
cas: "compareAndSet" {
  width: 180
  height: 36
  style.fill: "#e8f5e9"
}
weak: "weakCompareAndSet*" {
  width: 200
  height: 36
  style.fill: "#fff8e1"
}
cas -> weak: "false: value changed"
weak -> cas: "false: maybe spurious"
```

**Fig. 1.** Strong `false` is informative. Weak `false` is not.

> [!warning] There is no `AtomicInteger.compareAndSwap`
> The atomic classes expose **`compareAndSet`**. `compareAndSwap` was the old `Unsafe` spelling.

> [!warning] Deprecated `weakCompareAndSet` is plain
> The name looks volatile. The method was **plain**. That mismatch is why it is deprecated.

> [!warning] Weak CAS is not a single-attempt API
> If you cannot retry, use **`compareAndSet`** (or **`compareAndExchange`**).

> [!tip] Interview answer
> compareAndSet is a strong volatile CAS: if the value is still expected, it succeeds. weakCompareAndSet may fail even then, so you only use it inside a loop. On AtomicInteger the old weakCompareAndSet was actually plain, so I call weakCompareAndSetVolatile or weakCompareAndSetPlain on purpose.
