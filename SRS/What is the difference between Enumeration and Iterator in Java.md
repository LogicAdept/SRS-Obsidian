<!--
reps: 0
priority: 0
-->
#Java/Collections/Iteration #SRS

# What is the difference between `Enumeration` and `Iterator` in Java?

> [!abstract] Short answer
> **`Iterator` (Java 1.2) replaced `Enumeration` (Java 1.0) in the Collections Framework.** Same job — walk a series of elements — with shorter names (`hasNext` / `next` vs `hasMoreElements` / `nextElement`) and an optional **`remove()`**. `Enumeration` has no `remove`. `Iterator.add` does not exist (`ListIterator` does). Prefer `Iterator`; `Enumeration.asIterator()` (Java 9) is an adapter whose `remove` throws `UnsupportedOperationException`.

## Names, `remove`, and where you get them

`Iterator` “takes the place of `Enumeration` in the Java Collections Framework.” Differences the interface itself lists: (1) the caller can remove from the underlying collection with well-defined semantics; (2) method names were improved [[What is the Iterator interface and why do Java collections use it]], [[In which Java version was Iterator introduced]], [[What types of iterators or cursors exist in Java]].

`Enumeration` is the Vector / Hashtable-era cursor: `Vector.elements()`, `Hashtable.keys()` / `elements()`. New code should use `Iterator`. `asIterator()` maps `hasMoreElements`→`hasNext`, `nextElement`→`next`, and `remove`→UOE.

**`remove`:** `Iterator.remove()` deletes the last `next()` (once per `next()`; ISE otherwise; optional) [[How do you remove an element from a collection while iterating]]. `Enumeration` cannot. Neither interface has **`add`** — that needs a list cursor [[Why is there no add method on Iterator]].

**Fail-fast is not “Iterator vs Enumeration”.** `ArrayList.iterator()` is fail-fast. `Hashtable` **view** iterators are fail-fast; `Hashtable.keys()` / `elements()` enumerations are **not** (results undefined if structurally modified). `Vector` has both a fail-fast `iterator()` and a non-fail-fast `elements()` [[Is Enumeration fail-fast]].

`Collection.iterator()` exists on modern collections. `Vector` still offers `elements()` for compatibility; it also implements `Iterable`.

```d2
direction: down
en: "Enumeration 1.0\nhasMoreElements / nextElement" {
  width: 300
  height: 70
  style.fill: "#fff3e0"
}
it: "Iterator 1.2\nhasNext / next / remove" {
  width: 280
  height: 70
  style.fill: "#e8f5e9"
}

en -> it: "names + optional remove"
```

**Fig. 1.** Same traversal idea. `Iterator` adds `remove` and shorter names. Order of iteration is still collection-specific.

```java
class EnumerationVsIterator {
    static void enumeration(java.util.Vector<String> v) {
        java.util.Enumeration<String> e = v.elements();
        while (e.hasMoreElements()) {
            e.nextElement();
        }
    }

    static void iterator(java.util.Collection<String> c) {
        java.util.Iterator<String> it = c.iterator();
        while (it.hasNext()) {
            if (it.next().isEmpty()) {
                it.remove();
            }
        }
    }
}
```

**Listing 1.** `elements()` cannot `remove`. `iterator()` can, after `next()`. `for (String s : v)` uses `iterator()`, not `elements()`.

> [!warning] `Iterator` cannot `add` either
> The Enumeration/Iterator contrast is **`remove` and names**, not insert-at-cursor. `ListIterator.add` is a `List` API.

> [!warning] Legacy class ≠ only `Enumeration`
> `Vector` and `Hashtable` also have fail-fast iterators on their `Collection`/`Map` views. Using `elements()`/`keys()` is the non-fail-fast, undefined-on-mutate walk — not “Iterator is always safer because threads cannot modify.”

> [!tip] Interview answer
> **`Iterator` is the Collections cursor: `hasNext`/`next` plus optional `remove`. `Enumeration` is the 1.0 cursor: long names, no `remove`.** Prefer Iterator. Hashtable/Vector enumerations are not fail-fast; their view iterators are. There is no `Iterator.add`.
