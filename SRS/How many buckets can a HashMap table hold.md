<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/HashMap #SRS

# How many buckets can a `HashMap` table hold?

> [!abstract] Short answer
> **From 16 by default up to `1 << 30` (1 073 741 824) in OpenJDK.** Capacity is bucket count — `table.length` — always a power of two once the array exists. Asking for more buckets than that is clamped, not rejected. That ceiling is **not** a cap on `size()`: extra mappings still go into those bins.

## The range that actually exists

The public javadoc talks in “number of buckets” and “about twice as many” on rehash. It does not name a maximum. OpenJDK `HashMap` does:

```java
static final int DEFAULT_INITIAL_CAPACITY = 1 << 4;  // 16
static final int MAXIMUM_CAPACITY         = 1 << 30; // 1_073_741_824
```

**Listing 1.** OpenJDK constants (Java 21). Both must be powers of two. The table is created on first use, so these numbers are lengths of `Node[]`, not `size()`.

```d2
direction: down
req: "requested capacity" {
  width: 240
  height: 70
  style.fill: "#e3f2fd"
}
round: "tableSizeFor\nnext power of two" {
  width: 260
  height: 80
  style.fill: "#fff3e0"
}
clamp: "if > 1 << 30\nuse 1 << 30" {
  width: 240
  height: 80
  style.fill: "#ffe0b2"
}
stop: "already 1 << 30\nresize returns same array" {
  width: 300
  height: 90
  style.fill: "#eeeeee"
}

req -> round
round -> clamp
clamp -> stop
```

**Fig. 1.** Requested size is rounded up to a power of two, then capped. At the cap, doubling stops.

`HashMap(n)` / `HashMap(n, f)` throw `IllegalArgumentException` only if `n < 0` (or load factor is nonpositive / NaN). If `n > MAXIMUM_CAPACITY`, OpenJDK **assigns** `MAXIMUM_CAPACITY` and continues. `tableSizeFor` also returns that constant when the rounded value would meet or exceed it.

```java
Map<String, Integer> a = new HashMap<>(1 << 30);       // asked the ceiling
Map<String, Integer> b = new HashMap<>(1_073_741_825); // still the ceiling, no IAE
Map<String, Integer> c = new HashMap<>(-1);            // IllegalArgumentException
```

**Listing 2.** Too-large initial capacity is legal; a negative one is not. The array is still allocated on the first `put`, not in the constructor.

Default no-arg map: 16 buckets after that first allocation. [[What are the initial capacity and load factor parameters of HashMap]] and [[What is initial capacity in Java collections such as HashMap]] are those knobs. Growth: [[How and when does HashMap resize its buckets]].

## Why doubling stops at `1 << 30`

Bucket index is `(n - 1) & hash`. That mask is correct only when `n` is a power of two. A Java array’s length is a positive `int`. The next power of two after `1 << 30` is `1 << 31`, which as a signed `int` is negative and is not a valid array length. So `1 << 30` is the largest power-of-two table OpenJDK can allocate.

`resize` encodes that:

* if `table.length` is already `MAXIMUM_CAPACITY`, it sets `threshold` to `Integer.MAX_VALUE` and **returns the same array**;
* otherwise it tries `oldCap << 1` (and will allocate `1 << 30` when doubling from `1 << 29`).

After the table is at the ceiling, the load-factor rule no longer grows it. Mappings can still be added; bins just get denser. [[What rule governs when HashMap grows its number of buckets]] is the usual `size > capacity × loadFactor` test — it does not apply once threshold has been pinned to `Integer.MAX_VALUE`.

> [!warning] Max buckets is not max keys
> `1 << 30` is array length. `size()` is mapping count. You can have more entries than buckets; they share bins. You cannot have more than `Integer.MAX_VALUE` mappings (`size` is `int`), and you will usually run out of memory first. Do not quote “two billion keys” as the bucket limit. [[What is the internal structure of HashMap]]

> [!tip] Interview answer
> **OpenJDK `HashMap` tables are power-of-two arrays from 16 buckets by default up to `1 << 30`. A constructor argument above that is clamped; only a negative capacity throws. At the ceiling, `resize` keeps the same array and stops doubling. That number is buckets, not `size()`.**
