<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Cache #SRS

# How does Spring generate a cache key by default?

> [!abstract] Short answer
> Default is **`SimpleKeyGenerator` (Spring 4.0+)**: **no args → `SimpleKey.EMPTY`**; **one non-null arg → that object**; **several args (or a single null) → `SimpleKey` of the parameters**. The method and target bean are **not** part of the key. Override with SpEL **`key`** or a **`keyGenerator` bean** — not both.

## Parameter-only algorithm

Spring *Default Key Generation*: each cached invocation is mapped to a key. The built-in `KeyGenerator` does:

1. Zero parameters → **`SimpleKey.EMPTY`**
2. One parameter → **that instance** (javadoc: a **single non-null** value; otherwise wrap in `SimpleKey`)
3. More than one → **`SimpleKey`** holding all parameters

`SimpleKey` implements `equals` / `hashCode` / `Serializable`. This works when parameters are **natural keys** with a stable **`equals`/`hashCode`**. Change the strategy by implementing **`KeyGenerator`**.

Pre-4.0 `DefaultKeyGenerator` used **hashCode only** for multi-arg keys (collision bug). `SimpleKeyGenerator` is the compound-key replacement.

```java
@Cacheable("books")
public Book findBook(ISBN isbn) { /* key = isbn */ }

@Cacheable("books")
public Book findBook(String title, String author) { /* key = SimpleKey(title, author) */ }

@Cacheable(cacheNames = "books", key = "#isbn")
public Book findBook(ISBN isbn, boolean includeReviews) { /* reviews ignored */ }
```

**Listing 1.** Default uses **all** parameters; SpEL `key` picks a subset. Customizer: [[How do you set a Spring cache key with SpEL]]. Enablement default: [[What is the EnableCaching annotation]].

```d2
direction: down
n: "args.length" {
  width: 160
  height: 50
  style.fill: "#e3f2fd"
}
z: "SimpleKey.EMPTY" {
  width: 180
  height: 50
  style.fill: "#e8f5e9"
}
o: "the argument" {
  width: 180
  height: 50
  style.fill: "#fff3e0"
}
m: "new SimpleKey(params)" {
  width: 220
  height: 50
  style.fill: "#fce4ec"
}

n -> z: "0"
n -> o: "1 non-null"
n -> m: "2+ or null"
```

**Fig. 1.** `key` and `keyGenerator` on the same annotation are **mutually exclusive** (`Cacheable` javadoc).

> [!warning] Method name is not in the key
> Two methods sharing cache `"books"` and the same argument type **collide**. Use different `cacheNames` or an explicit `key`.

> [!warning] Bad `equals`/`hashCode` on the argument
> A mutable ISBN whose hash changes after `put` is lost in a `ConcurrentHashMap`. Arrays as a **single** key use the array object’s own equality, not deep contents, unless you wrap them.

> [!warning] `SimpleKey` vs some remote caches
> Javadoc: safe with `ConcurrentMapCache`; **not necessarily** with every `Cache` implementation (serialization / Redis key format). Remote stores often need a SpEL string key or a custom generator.

> [!tip] Interview answer
> **Default keys come from method parameters via `SimpleKeyGenerator`:** empty key, the single argument, or a `SimpleKey` of all args — not the method name. Parameters need proper `equals`/`hashCode`. Use `key` SpEL when only some arguments identify the entry.
