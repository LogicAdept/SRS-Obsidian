<!--
reps: 0
priority: 0
-->
#Java/Collections #Java/Exceptions/Unchecked #SRS

# How would you explain give when which collection `UnsupportedOperationException`?

> [!abstract] Short answer
> **When you call a mutator that this collection does not implement.** `add`/`remove`/`clear` are optional. Unmodifiable lists (`Collections.emptyList()`, `List.of`, `Collections.unmodifiableList`) throw `UnsupportedOperationException` on those calls. It is a `RuntimeException`, not a checked “please catch me.”

## Optional operations, not a broken `ArrayList`

The collections interfaces mark many mutators **optional**. An implementation that does not support `add` **should** throw `UnsupportedOperationException`. An **unmodifiable** collection specifies that **all** mutators throw it ([[What is ConcurrentModificationException]], [[What is NoSuchElementException]]).

Typical sources:

- **`Collections.emptyList()` / `emptySet()` / `emptyMap()`** — immutable empties. `emptyList().add(0)` throws.
- **`List.of` / `Set.of` / `Map.of`** — unmodifiable; add, remove, and **replace** all throw.
- **`Collections.unmodifiableList(list)`** (and siblings) — a **view**. Mutators on the view throw; the **backing** list can still change, and those changes show through.
- **`Arrays.asList(array)`** — **fixed-size**, not fully unmodifiable. `add`/`remove` throw; **`set` is allowed** and writes through to the array.

`ArrayList` itself supports `add`. You get UOE from the **wrapper or factory**, not because “lists cannot grow.” Copy-on-write iterators also refuse `remove` ([[How do you avoid ConcurrentModificationException while iterating a collection]]).

Unmodifiable is not **immutable** if the **elements** are mutable.

```d2
direction: down
call: "list.add(x)" {
  width: 240
  height: 50
}
al: "ArrayList — ok" {
  width: 240
  height: 50
  style.fill: "#e8f5e9"
}
uoe: "emptyList / List.of / unmodifiable*\nUnsupportedOperationException" {
  width: 340
  height: 70
  style.fill: "#ffebee"
}
call -> al
call -> uoe
```

**Fig. 1.** Same `List` type at compile time. The runtime object decides whether `add` exists.

```java
class Demo {
    static void empty() {
        java.util.List<Integer> list = java.util.Collections.emptyList();
        list.add(0);
    }

    static void fixedSize() {
        java.util.List<String> list = java.util.Arrays.asList("a", "b");
        list.set(0, "z");
        list.add("c");
    }
}
```

**Listing 1.** `empty()` throws on `add`. `fixedSize()`: `set` succeeds; `add` throws `UnsupportedOperationException`.

> [!warning] `List` in the variable type does not mean `add` works
> `List<Integer> list = Collections.emptyList()` compiles. The exception is at **run time**.

> [!warning] `Arrays.asList` is not `List.of`
> Fixed-size: no `add`. `set` is fine. `List.of` forbids `set` as well.

> [!tip] Interview answer
> **`UnsupportedOperationException` means this collection does not support that mutator — empty lists, `List.of`, unmodifiable views, or `Arrays.asList` for `add`.** It is unchecked. `ArrayList.add` does not throw it; the factory or wrapper you actually have does.
