<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/ConcurrentHashMap #Java/Collections/Concurrency #SRS

# What is `concurrencyLevel` in `ConcurrentHashMap`?

> [!abstract] Short answer
> **A constructor hint for “how many threads will update at once,” never a cap on threads and not a live lock count on Java 8+.** Java 7 used it to size the `Segment[]` (default 16, power of two). Java 8+ may only raise `initialCapacity` so there are at least that many bins. Default table size **16** is a different knob.

## Hint for sizing, two generations

Class docs: constructors may still take an expected `concurrencyLevel` **for compatibility**, as an extra hint for internal sizing. The three-arg constructor: estimated number of concurrently updating threads; the implementation **may** use it as a sizing hint. `<= 0` is `IllegalArgumentException`. It does not reject a 17th writer and does not lock the whole table ([[Does ConcurrentHashMap get lock the whole table]]).

```d2
direction: right
j7: "Java 7\nconcurrencyLevel → Segment[] length\n(power of two, default 16)" {
  width: 280
  height: 90
  style.fill: "#fff8e1"
}
j8: "Java 8+\nmay bump initialCapacity\nto ≥ concurrencyLevel bins" {
  width: 280
  height: 90
  style.fill: "#e8f5e9"
}
j7 -> j8: "no longer stripe count"
```

**Fig. 1.** Same parameter name; Java 8 does not restore segment locks from this argument ([[Why did ConcurrentHashMap drop segment locks in Java 8]]).

Java 7: round `concurrencyLevel` up to a power of two (`ssize`), allocate that many `Segment`s, cap `1 << 16`. Each `Segment` is a `ReentrantLock`. Ideal case: that many concurrent writers without sharing a stripe. Real concurrency varies with hashing. Default constructors passed **16** for both this hint and default **initial capacity** — easy to conflate ([[How does ConcurrentHashMap use Segment locks in Java 7]]).

Java 8+: the three-arg constructor does `if (initialCapacity < concurrencyLevel) initialCapacity = concurrencyLevel` (“at least as many bins as estimated threads”). The no-arg map is default table size 16 with an empty constructor. `ConcurrentHashMap(n)` and `(n, loadFactor)` pass **`concurrencyLevel` 1**, not 16. Live updates CAS an empty bin or `synchronized` the bin head ([[How does ConcurrentHashMap use CAS and synchronized in Java 8]]). A dummy `Segment` type remains for serialization. The class arrived in 1.5 ([[In which Java version was ConcurrentHashMap introduced]]).

```java
import java.util.concurrent.ConcurrentHashMap;

class Demo {
    static void constructors() {
        new ConcurrentHashMap<String, Integer>();           // default table size 16
        new ConcurrentHashMap<String, Integer>(32);         // Java 8+: hint 1
        new ConcurrentHashMap<String, Integer>(32, 0.75f, 16); // sizing hint 16
    }
}
```

**Listing 1.** Only the three-arg form still takes `concurrencyLevel`. It is not `setMaxWriters(16)`.

```java
// Conceptual — what the hint actually did
// Java 7:  ssize = nextPow2(concurrencyLevel);  segments = new Segment[ssize];
// Java 8+: if (initialCapacity < concurrencyLevel) initialCapacity = concurrencyLevel;
```

**Listing 2.** Java 7 sized stripes. Java 8+ sized the starting bin array, then ignored it as a lock table.

> [!warning] Default **16** is two different defaults
> Initial capacity 16 (how many mappings to expect) is not `concurrencyLevel`. Java 7’s default stripe count was also 16. On Java 8+, `new ConcurrentHashMap()` does not pass 16 as a concurrency hint at all.

> [!warning] N stripes ≠ N permitted threads, and Java 8 has no stripes
> Extra writers still enter; they contend. A hot hash can pile keys on one Java 7 segment. After Java 8, quoting `concurrencyLevel` as “number of locks” is the old model: locks are per occupied bin, not `concurrencyLevel` monitors.

> [!tip] Interview answer
> **`concurrencyLevel` is a sizing hint for expected concurrent writers, not a thread limit.** Java 7 turned it into the `Segment[]` length (default 16, power of two). Java 8+ may only ensure at least that many initial bins; it is not the lock count. Do not confuse it with default capacity 16.
