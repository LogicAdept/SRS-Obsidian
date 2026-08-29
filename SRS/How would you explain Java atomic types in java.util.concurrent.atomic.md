<!--
reps: 0
priority: 0
-->
#Java/Concurrency/Atomics #SRS

# How would you explain Java atomic types in java.util.concurrent.atomic?

> [!abstract] Short answer
> The package is a **toolkit for lock-free updates of one variable** (or one array slot). Values are read and written with the same atomic **`VarHandle`** operations you would use on a field: **`get`/`set`** (volatile-like by default), **`compareAndSet`**, **`getAndAdd`**, **`getAndUpdate`**. **`AtomicInteger` / `AtomicLong` / `AtomicBoolean` / `AtomicReference`** are the scalars; **`*Array`** types give **volatile-element** arrays; **`AtomicMarkableReference`** / **`AtomicStampedReference`** pair a ref with a mark or stamp; **`LongAdder`** / **`DoubleAdder`** spread a sum. They are **not** `Integer` stand-ins and are **bad map keys**. Volatile vs atomic: [[What is the difference between volatile fields and atomic variables]]. Strong vs weak CAS: [[What is the difference between compareAndSet and weakCompareAndSet]]. `++` is not atomic: [[Why is the Java increment operator not atomic]].

## One variable, VarHandle methods

A typical use is a sequence number: `getAndIncrement` on an `AtomicLong`. Low-level RMW is `compareAndSet` (succeeds only if the **witness** still equals expected). Higher-level helpers (`getAndUpdate`, `accumulateAndGet`) retry that idea with a function. Default `get`/`set` on `AtomicInteger` match **volatile** read/write. That is **visibility plus atomic RMW on that payload**, not a lock around arbitrary code — [[How does volatile visibility differ from atomicity for compound updates]]. Field-level: [[What is the difference between volatile fields and atomic variables]].

**Arrays** (`AtomicIntegerArray`, …) document **volatile** access to **elements** (plain `int[]` elements are not volatile). **Field updaters** are older reflection tools for a chosen `volatile` field on a class; they **predate `VarHandle`**, are clumsier, and have **weaker** guarantees — prefer `VarHandle` for new code. **Adders** keep a **sum** across stripes when many threads only add.

```java
final class Sequencer {
    private final AtomicLong sequenceNumber = new AtomicLong(17);
    public long next() {
        return sequenceNumber.getAndIncrement();
    }
}
```

**Listing 1.** Package sample: atomic increment as a sequence, not `long++` on a shared field.

```d2
direction: down
pkg: "java.util.concurrent.atomic" {
  width: 280
  height: 40
  style.fill: "#e3f2fd"
}
one: "one value or array slot" {
  width: 240
  height: 40
  style.fill: "#fff8e1"
}
vh: "VarHandle CAS / getAndAdd / getAndUpdate" {
  width: 320
  height: 45
  style.fill: "#e8f5e9"
}
pkg -> one
one -> vh
```

**Fig. 1.** Scope is a single variable. Two atomics together still need a lock or one combined structure.

> [!warning] Not `Integer`, not a hash key
> No `equals` / `hashCode` / `compareTo` contract like wrappers. The object is **meant to mutate**. Do not put an `AtomicInteger` in a `HashMap` key.

> [!warning] CAS is not the whole package
> Increment, add, and `getAndUpdate` are atomic RMWs too. “Only CAS” misses `getAndIncrement` and the adders. Two fields still race unless one atomic (or a lock) covers both.

> [!tip] Interview answer
> java.util.concurrent.atomic gives lock-free atomic updates to one variable using VarHandle operations. AtomicInteger and friends add CAS and getAndIncrement so a counter does not lose updates the way volatile plus plus does. They are not Integer replacements, and they do not make two separate fields one transaction.
