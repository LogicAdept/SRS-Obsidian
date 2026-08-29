<!--
reps: 0
priority: 0
-->
#OperatingSystems/Concurrency #Java/Concurrency #Problems/Concurrency #SRS

# What is the difference between a race condition and a data race?

> [!abstract] Short answer
> A **data race** is a **JMM** bug: two **conflicting** accesses to the **same variable** (at least one **write**) with **no happens-before**. A **race condition** is a **logic** bug: the **outcome depends on interleaving**, even when every single access is race-free. **Data-race-free is not enough** — a **group** of operations may still need to look **atomic** (`containsKey` then `put`). Race notes: [[How would you explain race conditions in concurrent programs]]. No universal fix: [[Is there a universal fix for race conditions in concurrent code]]. Check-then-act: [[How do you avoid a check-then-act race on ConcurrentHashMap]]. Compound vs `volatile`: [[How does volatile visibility differ from atomicity for compound updates]]. HB: [[How would you explain the happens-before guarantee in the Java Memory Model]].

## Memory-model race vs “wrong interleaving”

**Data race:** unsynchronized `c++` from two threads is the textbook case (`c++` is **read, add, write**). No SC appearance; reads may see **stale or surprising** values. Java still forbids some nonsense (array length stays honest); it is **not** C++ **undefined behavior**.

**Race condition / thread interference:** two multi-step operations **overlap** so an update is **lost** or an invariant breaks. That **includes** data races, and **also** **check-then-act** on a **concurrent map**, or two **`synchronized`** methods that each look fine but **compose** badly. Fix the **whole** check+update (one lock, `putIfAbsent`, `compareAndSet`), not only `volatile` on a field.

```java
int c;
void unsyncInc() { c++; } // data race if two threads

void act(ConcurrentHashMap<K, V> m, K k, V v) {
 if (!m.containsKey(k)) m.put(k, v); // DRF map; still a race
}
```

**Listing 1.** Left: JMM data race. Right: no data race, still a race condition.

```d2
direction: down
rc: "race condition: interleaving breaks the spec" {
 width: 340
 height: 40
 style.fill: "#fff8e1"
}
dr: "data race: conflicting accesses, no happens-before" {
 width: 360
 height: 40
 style.fill: "#ffebee"
}
cta: "check-then-act on a concurrent structure" {
 width: 320
 height: 40
 style.fill: "#e3f2fd"
}
rc -> dr
rc -> cta
```

**Fig. 1.** Data race is one kind of race. Concurrent collections can still lose a check-then-act.

> [!warning] No data races ≠ correct
> Freedom from data races still allows errors when a **group** of operations must look **atomic** and does not.

> [!warning] `volatile` does not fix `c++`
> It orders **single** reads/writes. The increment is still **three steps**.

> [!tip] Interview answer
> A data race is two conflicting accesses to the same variable with no happens-before. A race condition is any bug that depends on thread interleaving, including check-then-act on a data-race-free map. Data-race-free is required for sequential consistency, but it does not make compound updates atomic.
