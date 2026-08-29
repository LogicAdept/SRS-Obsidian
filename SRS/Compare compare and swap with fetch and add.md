<!--
reps: 0
priority: 0
-->
#Java/Concurrency/Atomics #SRS

# Compare compare-and-swap with fetch-and-add

> [!abstract] Short answer
> **CAS** (`compareAndSet`) is a **conditional** store: write `newValue` only if the current value `== expectedValue`, else return `false`. **Fetch-and-add** (`getAndAdd`) **always** adds a delta and returns the **previous** value. Both are lock-free RMWs on one variable. Use add for counters; use CAS when the next value depends on seeing a specific current value (or is not an add).

## Conditional store vs unconditional add

`java.util.concurrent.atomic` (Java 5+) is lock-free updates of single variables, backed by `VarHandle` memory effects. `compareAndSet` is the low-level RMW; `getAndUpdate` is a higher-level CAS loop. `AtomicInteger` / `AtomicLong` also expose atomic increment/add.

| | Compare-and-swap | Fetch-and-add |
| --- | --- | --- |
| Java | `compareAndSet(expected, new)` | `getAndAdd(delta)` / `addAndGet(delta)` |
| Effect | Store **if** witness `==` expected | **Always** add `delta` |
| Result | `boolean` (`false` ⇒ value was not expected) | Previous (`getAndAdd`) or updated (`addAndGet`) int/long |
| Types | ints, longs, refs, … | Numeric add (`AtomicInteger`/`AtomicLong`; `VarHandle.getAndAdd`) |
| Failure | Yes — caller retries or gives up | No “failed add”; the add is the RMW |
| Memory | `VarHandle.compareAndSet` (volatile get/set) | `VarHandle.getAndAdd` (volatile get/set) |

`getAndIncrement()` is `getAndAdd(1)`. `incrementAndGet()` is `addAndGet(1)`. Arbitrary functions go through **CAS**: `getAndUpdate` / `updateAndGet` may **re-apply** the function when updates fail due to contention — the function must be side-effect-free. Weak CAS may fail spuriously; that is a different knob than fetch-and-add — [[What is the difference between compareAndSet and weakCompareAndSet]]. Package overview: [[How would you explain Java atomic types in java.util.concurrent.atomic]].

```java
import java.util.concurrent.atomic.AtomicInteger;

public final class CasVsFetchAdd {
    private final AtomicInteger n = new AtomicInteger();

    public int ticket() {
        return n.getAndAdd(1); // always takes the next value
    }

    public boolean claimZero() {
        return n.compareAndSet(0, 1); // only if still 0
    }
}
```

**Listing 1.** Fetch-and-add is the sequencer. CAS is “change it only if it is still this.” `compareAndExchange` returns the **witness** instead of a boolean (Java 9+).

```d2
direction: down
need: "What update?" {
  width: 220
  height: 50
  style.fill: "#e3f2fd"
}
faa: "getAndAdd\nunconditional +delta" {
  width: 280
  height: 70
  style.fill: "#e8f5e9"
}
cas: "compareAndSet\nonly if expected matches" {
  width: 300
  height: 70
  style.fill: "#fff3e0"
}
need -> faa: "counter / sequence"
need -> cas: "link, flag, or computed next"
```

**Fig. 1.** Implementing add yourself as `while (!cas(old, old + d)) old = get()` is a CAS loop. `getAndAdd` is that problem as one atomic. `c++` on a plain `int` is **not** atomic.

> [!warning] A failed CAS is not a failed fetch-and-add
> `compareAndSet` returning `false` means the witness was not `expectedValue`. Another thread already moved the variable. Swallowing `false` **drops** the update. Fetch-and-add does not give you that `false`.

> [!warning] CAS on references can see ABA
> Matching `== expected` does not mean “nobody touched it.” `AtomicStampedReference` pairs a stamp with the ref. An integer fetch-and-add counter does not have that link-swap ABA shape; it also cannot express “set only if still null.”

> [!tip] Interview answer
> CAS is compare-and-store: succeed only if the value is still what you read; fail and retry otherwise. Fetch-and-add always applies a delta and returns the old (or new) value — that is `getAndAdd` / `incrementAndGet`. Counters want add; lock-free structures and “set if still X” want CAS.
