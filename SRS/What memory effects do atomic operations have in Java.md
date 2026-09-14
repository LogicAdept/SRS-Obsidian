<!--
reps: 0
priority: 0
-->
#Java/JMM/HappensBefore #Java/Concurrency/Atomics #SRS

# What memory effects do atomic operations have in Java

> [!abstract] Short answer
> **The `java.util.concurrent.atomic` classes are documented wrappers over VarHandle access modes: default `get`/`set` behave like volatile read/write, and `compareAndSet` carries the memory effects of `VarHandle.compareAndExchange` — an atomic read-modify-write at the volatile tier.** A successful CAS therefore releases everything written before it and acquires for the winner, forming happens-before edges like any volatile action.

Since Java 9 the atomic classes are specified through VarHandles rather than raw `Unsafe` calls: the package description states that instances "maintain values that are accessed and updated using methods otherwise available for fields using associated atomic VarHandle operations". The default methods sit on the top tier of the access-mode ladder — `AtomicInteger.get` maps to `VarHandle.getVolatile`, `set` to `setVolatile`, `getAndIncrement` to the volatile-tier `getAndAdd`, and `compareAndSet` to `compareAndExchange` — where, per the VarHandle specification, all volatile operations are totally ordered with respect to each other. Explicit suffix variants (`getPlain`, `getOpaque`, `getAcquire`, `setRelease`, `weakCompareAndSetPlain`...) expose the lower tiers for lock-free code that needs weaker, cheaper ordering ([[How do VarHandle access modes order memory in Java]]).

This is what makes CAS-based publication correct. A read-modify-write at the volatile tier reads and writes with volatile memory effects, so plain writes performed before a successful `compareAndSet` become visible to any thread that later reads the reference with `get` or wins its own CAS on the same atomic object. The same logic explains the atomic array classes, which extend the guarantee element-wise — the package description notes they provide volatile access semantics for their array elements — and why a lock-free algorithm built from CAS needs no additional fencing on the default tiers.

```d2
direction: right
plain: "Plain\ngetPlain / setPlain\nno ordering" {
  width: 200
  height: 96
  style.fill: "#f5f5f5"
}
opaque: "Opaque\natomic + coherent\non one variable" {
  width: 210
  height: 96
  style.fill: "#e8eaf6"
}
arel: "Acquire / Release\ngetAcquire, setRelease\none-way ordering" {
  width: 230
  height: 96
  style.fill: "#fff3e0"
}
vol: "Volatile\ndefault get / set / CAS\ntotally ordered" {
  width: 230
  height: 96
  style.fill: "#e8f5e9"
}
plain -> opaque
opaque -> arel
arel -> vol
```

**Fig. 1.** The VarHandle ordering ladder the atomic API is specified against: each tier adds ordering strength, and the default atomic methods sit at the volatile tier, so a successful CAS behaves like a volatile read plus a volatile write.

```java
class CasPublication {
    private final AtomicReference<State> ref = new AtomicReference<>();
    private State preparedState;               // plain field

    void publisher() {
        preparedState = new State("ready");    // (1) plain write
        ref.compareAndSet(null, preparedState); // (2) volatile-tier RMW
    }                                          // hb(1, 2) program order

    void consumer() {
        State s = ref.get();                   // (3) volatile read: hb(2, 3)
        if (s != null) {
            s.use();                           // (4) sees State("ready")
        }                                      // hb(1, 4) by transitivity
    }
}
```

**Listing 1.** The CAS acts as the publication edge: everything the publisher did before it is visible to the consumer that reads through the same atomic reference, exactly as with a volatile hand-off.

> [!warning] Atomicity of one variable is not atomicity of an invariant
> The guarantee is per-variable. Two `AtomicInteger`s updated one after another have no compound invariant: a reader can see the first update and not the second, because each variable orders itself but neither orders the pair. Consistent snapshots still need an immutable holder object, a lock, or `AtomicReference` over the whole state. And the weaker variants betray the default-tier expectations — `weakCompareAndSet` may fail spuriously and, in its `Plain` form, creates no happens-before ordering at all ([[What is the difference between compareAndSet and weakCompareAndSet]]).

> [!tip] Rule of thumb: default methods are volatile-tier
> Treat `get`, `set`, `compareAndSet`, and `getAndIncrement` as volatile-equivalent unless the code explicitly asks for cheaper tiers, and reserve the suffixed variants for measured hot paths. This mapping is also the vocabulary bridge between the atomic classes and the raw memory model: the overview of the atomic toolkit ([[How would you explain Java atomic types in java.util.concurrent.atomic]]) and the non-atomicity of `++` ([[Why is the Java increment operator not atomic]]) both make sense once you see atomics as volatile semantics plus single-variable atomicity.
