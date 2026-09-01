<!--
reps: 0
priority: 0
-->
#Java/Collections/Iteration/FailFast #SRS

# Is `Enumeration` fail-fast?

> [!abstract] Short answer
> **No — not the `Hashtable` / `Vector` enumerations, and not as an `Enumeration` contract.** `Hashtable.keys()` / `elements()` and `Vector.elements()` are **not** fail-fast: if the collection is structurally modified after the enumeration is created, the results are **undefined**. Fail-fast on those same types is the **`Iterator`** from the collection views (`keySet()`, `iterator()`, `listIterator()`), which may throw `ConcurrentModificationException`. “Fail-safe” is dump slang here, not a snapshot guarantee.

## Not fail-fast ≠ fail-safe

`Enumeration` itself does not specify fail-fast or `ConcurrentModificationException`. The documented cursors are the legacy ones: Vector’s `elements()`, Hashtable’s `keys()` and `elements()`. Both class specs say those enumerations are **not fail-fast** and that structural modification during the walk leaves the results **undefined** [[Are Hashtable enumerations fail-fast]].

On the same objects, **iterators are fail-fast**: Hashtable collection-view iterators and Vector `iterator` / `listIterator` throw `ConcurrentModificationException` if the structure changes except through that iterator’s `remove` (or `add` on the list iterator). Fail-fast is **best-effort**, not a lock, and not a reason to catch CME for control flow [[What is fail-fast iterator behavior in Java collections]], [[What is ConcurrentModificationException]].

Interview tables that call Enumeration **fail-safe** mean only “does not throw CME.” They do **not** mean a copy-on-write snapshot (`CopyOnWriteArrayList` is the snapshot iterator). Undefined traversal is **less** safe than a fail-fast iterator that aborts, not more [[What is the difference between fail-fast and fail-safe iterators]].

`Iterator.remove()` exists; `Enumeration` has no remove. `Enumeration.asIterator()` (Java 9) adapts names only — its `remove` throws `UnsupportedOperationException` [[What is the difference between Enumeration and Iterator in Java]].

There is no platform spec that Enumeration is “twice as fast” or uses less memory than Iterator. Do not quote that.

```d2
direction: down
ht: "Hashtable / Vector" {
  width: 240
  height: 50
  style.fill: "#e3f2fd"
}
en: "keys() / elements()\nnot fail-fast\n→ undefined" {
  width: 260
  height: 80
  style.fill: "#fff3e0"
}
it: "view iterator()\nfail-fast\n→ CME (best-effort)" {
  width: 260
  height: 80
  style.fill: "#e8f5e9"
}

ht -> en
ht -> it
```

**Fig. 1.** Same collection, two cursors. Fail-fast is an **iterator** property on these classes, not an `Enumeration` property.

```java
class EnumerationNotFailFast {
    static void bothCursors(java.util.Hashtable<String, Integer> table) {
        java.util.Enumeration<String> e = table.keys(); // not fail-fast
        while (e.hasMoreElements()) {
            e.nextElement();
        }
        java.util.Iterator<String> it = table.keySet().iterator(); // fail-fast
        while (it.hasNext()) {
            it.next();
        }
    }
}
```

**Listing 1.** `keys()` is the enumeration. `keySet().iterator()` is the fail-fast view iterator. Structural `put`/`remove` during the first walk is undefined; during the second, typically CME.

> [!warning] “Fail-safe Enumeration” does not mean a snapshot
> The spec’s words are **not fail-fast** and **undefined**. You can still see torn or repeated entries. Copy-on-write / concurrent weakly consistent iterators are a different contract.

> [!warning] Fail-fast Iterator is not “other threads cannot modify”
> Hashtable methods are synchronized; that does not make `keys()` fail-fast, and it does not make `keySet()` iteration a lock against another thread. CME is a bug detector, not mutual exclusion.

> [!tip] Interview answer
> **No. `Hashtable` / `Vector` enumerations are not fail-fast — mutation during the walk is undefined, not CME.** Fail-fast is their **iterators**. Calling Enumeration fail-safe is sloppy: it is not a snapshot, and it is not safer than Iterator. Iterator can `remove`; Enumeration cannot.
