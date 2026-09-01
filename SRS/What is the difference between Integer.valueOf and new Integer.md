<!--
reps: 0
priority: 0
-->
#Java/Language/Primitives #Java/Language/Wrappers/Autoboxing/Cache #SRS

# What is the difference between `Integer.valueOf` and `new Integer`?

> [!abstract] Short answer
> **`valueOf(int)` is the boxing factory** and **reuses** interned instances for **-128..127** (and any raised cache high). **`new Integer(int)` always allocates** a distinct object and **never** participates in that cache. Autoboxing compiles to `valueOf`, not `new`. The constructors have been **deprecated for removal since Java 9**; they are **not** gone in Java 17 or 21. Prefer `valueOf` / boxing; never write `new Integer`.

## Cache vs always-new

`Integer.valueOf(int)` returns the cached instance when the value is in range; otherwise it allocates. `new Integer(int)` skips the cache every time. That is why identity tests diverge ([[How can you extend the Integer autobox cache maximum]], [[What method does the compiler insert when autoboxing an int]]).

```d2
direction: down
val: "valueOf(100)\ncache hit, same object" {
  width: 260
  height: 70
  style.fill: "#e8f5e9"
}
neu: "new Integer(100)\nalways a fresh object" {
  width: 260
  height: 70
  style.fill: "#ffebee"
}
```

**Fig. 1.** Same payload `100`; only `valueOf` can return an interned instance.

```java
Integer a = Integer.valueOf(100);
Integer b = Integer.valueOf(100);
Integer c = new Integer(100);     // deprecated; distinct object
Integer d = new Integer(100);

boolean cached = (a == b);        // true: cache
boolean news = (c == d);          // false: two allocations
boolean mix = (a == c);           // false: cache vs new

Integer boxed = 100;              // autoboxing → valueOf(100), same as a
```

**Listing 1.** Conceptual: `==` is identity. Do not use it as value equality.

`valueOf(String)` parses, then calls `valueOf(int)`, so it **can** hit the cache. `new Integer(String)` parses and **still** allocates ([[What is the difference between Integer.parseInt and Integer.valueOf]], [[What are the different ways of creating a Java wrapper instance]]).

The `Integer(int)` / `Integer(String)` constructors are `@Deprecated(since = "9", forRemoval = true)`. They remain in current JDKs so old dumps compile with warnings. They were **not** removed in Java 17 ([[Why were Integer constructors deprecated]]).

Outside the cache (`valueOf(128)` twice, unless you raised `AutoBoxCacheMax`) identity need not match even for `valueOf`. Prefer `equals` / `intValue()`.

> [!warning] `new Integer(100) == new Integer(100)` is false
> Both are in the cache **range**, but `new` never reads the cache. Interview `==` snippets that mix `new` with boxing are testing that, not arithmetic. `new Integer` is also a different identity from a boxed `100` in the same method.

> [!tip] Interview answer
> **`valueOf` can return a cached `Integer`; `new Integer` always creates a new one.** Autoboxing uses `valueOf`, which is why `Integer a = 100; Integer b = 100; a == b` can be true. The constructors are deprecated since 9 and still present — do not use them, and do not claim they vanished in 17.
