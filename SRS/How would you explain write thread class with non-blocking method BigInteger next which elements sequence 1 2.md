<!--
reps: 0
priority: 0
-->
#Java/Concurrency/Atomics #SRS

# How would you write a thread-safe non-blocking BigInteger next() for 1, 2, 4, 8, …?

> [!abstract] Short answer
> Garbled cue: a **thread-safe** class whose **non-blocking** `BigInteger next()` yields **`1, 2, 4, 8, 16, …`**. Store the last published power in an **`AtomicReference<BigInteger>`**. **`next()`**: read `recent`, compute `recent == null ? ONE : recent.shiftLeft(1)` (`this << 1` = ×2), **`compareAndSet(recent, next)`** until it sticks, **return the new value**. `BigInteger` is **immutable**, so CAS of the **reference** is the whole update. Sibling: [[How do you implement a non-blocking power-of-two BigInteger sequence]]. Atomics: [[How would you explain Java atomic types in java.util.concurrent.atomic]]. CAS loop: [[How would you explain write minimum non-blocking stack two method — push and pop]].

## Double via `shiftLeft`, publish via CAS

`AtomicInteger` **overflows**; the sequence is unbounded. **`updateAndGet(r -> r.shiftLeft(1))`** is the same retry loop if you start from **`ONE`** (first call must still yield **1** — either start at `null` and treat that as “before 1”, or `getAndUpdate` returning the **previous** value starting at `ONE`). Failed CAS means another thread took that power; retry from the new `get()`. No `synchronized`, no `Lock`.

```java
final class PowersOfTwo {
    private final AtomicReference<BigInteger> current = new AtomicReference<>();

    BigInteger next() {
        BigInteger recent, next;
        do {
            recent = current.get();
            next = (recent == null) ? BigInteger.ONE : recent.shiftLeft(1);
        } while (!current.compareAndSet(recent, next));
        return next;
    }
}
```

**Listing 1.** First `next()` CASes `null → 1`; later calls CAS `n → n<<1`. Each power is handed out **once**.

```d2
direction: down
g: "get recent" {
  width: 140
  height: 36
  style.fill: "#e3f2fd"
}
m: "next = 1 or recent<<1" {
  width: 200
  height: 36
  style.fill: "#fff8e1"
}
cas: "CAS current" {
  width: 140
  height: 36
  style.fill: "#e8f5e9"
}
g -> m -> cas
cas -> g: "lost race"
```

**Fig. 1.** Linearization is the successful CAS. Losers recompute from the winner’s value.

> [!warning] `synchronized` on `next()` would be thread-safe and blocking
> The cue is **lock-free**. A mutex serializes callers; CAS lets them overlap the multiply and retry.

> [!warning] Do not mutate a `BigInteger`
> There is no `shiftLeft` in place. Sharing one mutable counter without CAS is a race.

> [!tip] Interview answer
> I keep the last power in an AtomicReference and CAS the next doubling with shiftLeft one. The first call publishes ONE. Callers who lose the race retry, so each value 1, 2, 4, 8 appears once without a lock.
