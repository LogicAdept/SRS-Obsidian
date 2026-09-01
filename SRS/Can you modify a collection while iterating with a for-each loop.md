<!--
reps: 0
priority: 0
-->
#Java/Collections/Iteration #Java/Language/Loops #SRS

# Can you modify a collection while iterating with a for-each loop?

> [!abstract] Short answer
> **Not by calling `add` / `remove` on the collection from the loop body.** Enhanced `for` over an `Iterable` is a hidden iterator: `iterator()` / `hasNext()` / `next()`. That name is not in scope, so the body cannot call `Iterator.remove()`. Any other structural change while that iterator is live is unspecified; on fail-fast types (`ArrayList`, `HashSet`, …) the next `next()` is usually `ConcurrentModificationException`. Mutating the **element objects** is not a structural change. To delete during a walk, use an explicit iterator or `removeIf`.

## Hidden iterator, same contract

```d2
direction: down
foreach: "for (E e : coll)" {
  width: 280
  height: 50
  style.fill: "#eceff1"
}
hidden: "#i = coll.iterator()\nwhile #i.hasNext(): e = #i.next()" {
  width: 320
  height: 80
  style.fill: "#e3f2fd"
}
ok: "element field mutators\nList.set (not structural)" {
  width: 300
  height: 70
  style.fill: "#e8f5e9"
}
cme: "coll.remove / add\n→ unspecified / CME" {
  width: 300
  height: 70
  style.fill: "#ffebee"
}
hiddenRm: "Iterator.remove()\nunreachable from this body" {
  width: 300
  height: 70
  style.fill: "#fff3e0"
}
foreach -> hidden
hidden -> ok
hidden -> cme
hidden -> hiddenRm
```

**Fig. 1.** For-each over a collection is the iterator contract with a compiler-generated `#i`. The allowed in-walk delete is `#i.remove()` after `next()`, which this syntax cannot name.

The language rewrite is `for (I #i = Expression.iterator(); #i.hasNext(); ) { T x = #i.next(); Statement }`. `#i` is synthetic. `Iterator.remove()` is the specified way to change the backing collection during iteration (once per `next()`). Behavior is unspecified if the collection is modified in any other way while this iterator is in progress, unless the class documents a concurrent-modification policy [[What happens if you call iterator.remove on a collection]], [[How would you explain the enhanced for each loop in Java]].

Fail-fast JRE collections treat that “other way” as a bug: `ArrayList` / `HashSet` iterators throw `ConcurrentModificationException` if the collection is structurally modified after the iterator is created, except through that iterator’s own `remove` (and `ListIterator.add`). A **structural** modification adds or deletes elements (or resizes the backing array). Setting an element’s fields, or `List.set`, is not structural [[What counts as a structural modification for fail-fast iterators]], [[What is ConcurrentModificationException]].

A single thread is enough: `list.remove` inside enhanced `for` is “modifies a collection directly while iterating with a fail-fast iterator” [[How can a single-threaded program get ConcurrentModificationException]].

```java
class ForEachStructuralRemove {
    static void cmeOnNext(java.util.List<String> list) {
        for (String s : list) {
            if (s.equals("a")) {
                list.remove(s);
            }
        }
    }
}
```

**Listing 1.** `ArrayList` of `"a"`, `"b"`, `"c"`: after removing `"a"`, the next `next()` throws `ConcurrentModificationException`. This is not `Iterator.remove()`.

```java
class ForEachElementMutation {
    static void renameInPlace(java.util.List<StringBuilder> list) {
        for (StringBuilder sb : list) {
            sb.setLength(0);
            sb.append("x");
        }
    }
}
```

**Listing 2.** The list still has the same three slots. Only the objects in those slots change. Fail-fast iterators do not treat this as concurrent modification.

The legal delete: an explicit `Iterator` and `remove()` after `next()`, or `Collection.removeIf` (Java 8; default implementation does the same) [[How do you remove an element from a collection while iterating]].

> [!warning] For-each cannot call `Iterator.remove()`
> The iterator exists but is compiler-generated. `list.remove(s)` in that body is the collection mutator, not the iterator’s. Prefer `while (it.hasNext())` / `it.remove()`, or `removeIf`.

> [!warning] CME is best-effort, not a loop rule
> `ArrayList.Itr.hasNext()` is `cursor != size` and does **not** check `modCount`. Removing the **second-to-last** element in a for-each can end the loop without another `next()`, so no exception, and the last element is skipped. Fail-fast is not a guarantee you can program against. `CopyOnWriteArrayList` iterators are a snapshot: they never throw CME; `list.remove` during for-each mutates the live list, not the array the loop is walking, and the iterator’s own `remove` throws `UnsupportedOperationException`.

> [!tip] Interview answer
> **Do not structurally modify a collection from a for-each body.** The loop is a hidden iterator; `coll.remove` / `add` is unspecified and typically `ConcurrentModificationException` on fail-fast types. Use `Iterator.remove()` after `next()`, or `removeIf`. Changing fields on the current element is fine — that is not a structural modification.
