<!--
reps: 0
priority: 0
-->
#Java/Collections/Iteration/FailFast #Java/Collections/List/ArrayList #Java/Collections/Map/HashMap #SRS

# What counts as a structural modification for fail-fast iterators?

> [!abstract] Short answer
> **Adding or deleting entries in the collection (plus, on `ArrayList`, an explicit backing-array resize).** Replacing a list element with `set`, or replacing a `HashMap` value for a key that is **already** present, is **not** structural. Fail-fast iterators throw `ConcurrentModificationException` when they detect a structural change they did not make (`Iterator.remove` / list-iterator `add` are the usual exceptions). “Any update while iterating” is too broad.

## Add/delete, not every write

The phrase is defined **per implementation**, not on `Iterator`. Two canonical definitions:

**`ArrayList`:** a structural modification is any operation that adds or deletes one or more elements, **or explicitly resizes the backing array**. Merely setting an element’s value is not. Fail-fast `iterator` / `listIterator` throw CME if the list is structurally modified after the iterator is created, except through **that** iterator’s `remove` or `add` [[What is fail-fast iterator behavior in Java collections]].

**`HashMap`:** a structural modification is any operation that **adds or deletes one or more mappings**. Merely changing the value associated with a key the map **already contains** is not. Collection-view iterators are fail-fast except through that iterator’s `remove` [[What is ConcurrentModificationException]].

`AbstractList.modCount` is the usual detector: it counts structural modifications. If it changes unexpectedly, `next` / `remove` / `previous` / `set` / `add` throw CME. Subclasses increment it in `add`/`remove` (and other structural methods). A `set` that only overwrites a slot should not bump it.

`HashSet.add` of an element already in the set leaves the set unchanged (`false`) — no new mapping, not a structural add. Mutating fields on an element already in the collection is not a collection modification at all.

OpenJDK `ArrayList.ensureCapacity` increments `modCount` only when it actually `grow`s. That matches “explicitly resizes the backing array”: a no-op ensure does not count; a real grow does, even with no `add`/`remove`.

```d2
direction: down
coll: "fail-fast collection" {
  width: 240
  height: 50
}
yes: "add / remove / clear\nArrayList array resize\nnew HashMap key" {
  width: 300
  height: 90
  style.fill: "#ffebee"
}
no: "List.set\nHashMap put existing key\nmutate element fields" {
  width: 300
  height: 90
  style.fill: "#e8f5e9"
}
own: "this iterator.remove\nlistIterator.add" {
  width: 280
  height: 70
  style.fill: "#fff3e0"
}

coll -> yes
coll -> no
coll -> own
```

**Fig. 1.** Structural change is about the collection’s **shape** (and ArrayList’s array size), not every assignment. The driving iterator’s own `remove`/`add` is still a structural change — just the one fail-fast allows.

```java
class StructuralVsNot {
    static void list(java.util.ArrayList<String> list) {
        list.set(0, "x");          // not structural
        list.add("y");             // structural
        list.ensureCapacity(64);   // structural only if the array actually grows
    }

    static void map(java.util.HashMap<String, Integer> map) {
        map.put("a", 1);           // new mapping → structural
        map.put("a", 2);           // same key, new value → not structural
        map.remove("a");           // structural
    }
}
```

**Listing 1.** `set` / in-place `put` do not add or delete entries. `add` / first `put` / `remove` do. Call `set` only on a non-empty list.

> [!warning] “Update” is not automatically structural
> Dump wording that lumps **updating** with add/remove is wrong for `HashMap` value replace and `ArrayList.set`. A new key or `add` is structural. `entry.setValue` on a mapping that already exists is the same non-structural value change.

> [!warning] The iterator’s own `remove` is still structural — just allowed
> `Iterator.remove()` after `next()` deletes an element. Fail-fast permits **that** iterator to do it. `list.remove` / `map.put` of a **new** key during the same walk is the CME path [[How do you remove an element from a collection while iterating]], [[Can you modify a collection while iterating with a for-each loop]].

> [!tip] Interview answer
> **Structural means add or delete (and ArrayList explicitly resizing its array) — not `List.set` and not `HashMap.put` of an existing key.** Fail-fast iterators watch that via `modCount` and throw CME unless the change was that iterator’s `remove` (or list-iterator `add`). Replacing a value in place is not a structural modification.
