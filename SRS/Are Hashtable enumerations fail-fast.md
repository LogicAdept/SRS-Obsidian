<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/Hashtable #Java/Collections/Iteration/FailFast #SRS

# Are `Hashtable` enumerations fail-fast?

> [!abstract] Short answer
> **No.** `Enumeration`s from `Hashtable.keys()` and `Hashtable.elements()` are **not** fail-fast. If the table is **structurally** modified after the enumeration is created, the walk’s results are **undefined** — the JDK does **not** promise `ConcurrentModificationException`.

## Enumeration vs view iterators on the same map

```d2
direction: right
enum: "keys() / elements()\nEnumeration\nnot fail-fast\n→ undefined if mutated" {
  width: 280
  height: 110
  style.fill: "#fff3e0"
}
views: "keySet / values / entrySet\nIterator\nfail-fast\n→ may throw CME" {
  width: 280
  height: 110
  style.fill: "#ffebee"
}
```

**Fig. 1.** Same `Hashtable`, two traversal contracts: legacy `Enumeration` vs Collections-view `Iterator`.

`Hashtable` class docs (Java SE 21): view iterators from `keySet` / `values` / `entrySet` are **fail-fast** (structural change other than that iterator’s own `remove` → `ConcurrentModificationException` on a best-effort basis). The `Enumeration`s from `keys()` and `elements()` are **explicitly not** fail-fast; structural mutation during enumeration makes results **undefined**. Method docs for `keys()` / `elements()` repeat that wording.

```java
Hashtable<String, Integer> table = new Hashtable<>();
table.put("a", 1);

Enumeration<String> keys = table.keys();
table.put("b", 2); // structural change while enumerating
while (keys.hasMoreElements()) {
    System.out.println(keys.nextElement()); // undefined results — no CME guarantee
}
```

**Listing 1.** Mutation during `keys()` is not a documented CME path; behavior is unspecified.

```java
Iterator<String> it = table.keySet().iterator();
table.put("c", 3);
it.next(); // ConcurrentModificationException (typical, best-effort)
```

**Listing 2.** The same structural put against a **view iterator** is the fail-fast path — opposite of Listing 1.

## Not the same story as `HashMap`

`HashMap` exposes traversal mainly through collection-view **iterators**, which are fail-fast (same idea as [[Are IdentityHashMap iterators fail-fast]]). Interview contrast “`HashMap` Iterator fail-fast vs `Hashtable` Enumeration not” is real for those APIs — but do not forget that **modern `Hashtable` also has fail-fast view iterators**. Prefer views over `keys()` / `elements()`; see [[What is the difference between HashMap and Hashtable]] and [[How would you explain drawbacks of the legacy Hashtable class]].

`Enumeration` itself has `hasMoreElements` / `nextElement` and **no** `remove`. The `Iterator` API note: functionality is duplicated by `Iterator`, which adds an optional `remove`. Prefer [[What is the difference between Enumeration and Iterator in Java]].

> [!warning] “Fail-safe” is not the JDK term
> Docs say **not fail-fast** and **undefined** under structural change. Calling that “fail-safe” (as if you got a safe snapshot) is interview slang. It is **not** CopyOnWrite and **not** `ConcurrentHashMap`’s weakly consistent iterators ([[Are ConcurrentHashMap iterators fail-fast]]).

> [!warning] Do not mix Enumeration and Iterator contracts
> On one `Hashtable`, `keys()`/`elements()` ≠ `keySet().iterator()`. Saying “`Hashtable` is never fail-fast” is wrong — **view iterators are fail-fast**; only the legacy enumerations are not.

> [!tip] Interview answer
> **`Hashtable.keys()` / `elements()` enumerations are not fail-fast** — structural mutation makes the walk undefined, with no CME promise. Collection-view iterators on the same map **are** fail-fast. Prefer those views (or `HashMap` / `ConcurrentHashMap`); do not call the old enumerations “fail-safe snapshots.”
