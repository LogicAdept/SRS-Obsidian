<!--
reps: 0
priority: 0
-->
#Java/Versions/21 #SRS

# What are sequenced collections

> [!abstract] Short answer
> **Sequenced collections (Java 21, JEP 431) fill the API gap around encounter order: new interfaces `SequencedCollection`, `SequencedSet`, `SequencedMap` add `getFirst`/`getLast`, `addFirst`/`addLast`, `removeFirst`/`removeLast`, and `reversed()` — a reverse-ordered view.** `List` and `Deque` are retrofitted, `LinkedHashSet`/`LinkedHashMap` gain the sequenced contracts, `SortedSet`/`SortedMap` join too, and universal wrappers like `Collections.unmodifiableSequence` complement the family. Before 21, "first element of a Set" or "reverse a List view" had no uniform API.

## What the interfaces add and where the traps are

`SequencedCollection` declares the access/mutate pairs and `reversed()`; `SequencedSet` refines `reversed()` to return `SequencedSet`; `SequencedMap` adds `putFirst`/`putLast`, `pollFirstEntry`/`pollLastEntry`, `sequencedKeySet`, `sequencedValues`, `sequencedEntrySet`, and `reversed()`. Retrofitting was surgical: `List`, `Deque` (already had the methods), `LinkedHashSet`, `SortedSet`, `LinkedHashMap`, `SortedMap` implement the interfaces; `HashSet` does **not** (no defined encounter order). Positional access on a `List` is not new — `get(0)`/`get(size-1)` did that ([[What are LinkedHashMap ordering guarantees]]); what is new is the same vocabulary over sets and maps without dropping to iterators.

The contract edges: `reversed()` is a **live view**, not a copy — mutations through either direction show through, and for `SequencedSet` the reversed view is itself a `SequencedSet` whose `addFirst`/`addLast` throw `UnsupportedOperationException` (order is fixed). `getFirst`/`getLast` on an empty collection throw `NoSuchElementException`. `addFirst`/`addLast`/`putFirst`/`putLast` are **optional** — `SortedSet`/`SortedMap` throw `UnsupportedOperationException` because they cannot reposition by their comparator's fiat.

```d2
direction: down
sc: "SequencedCollection\ngetFirst/getLast add/removeFirst/Last reversed()" {
  width: 480
  height: 75
  style.fill: "#e3f2fd"
}
ss: "SequencedSet\nreversed() stays SequencedSet\naddFirst throws for SortedSet" {
  width: 420
  height: 75
  style.fill: "#e8f5e9"
}
sm: "SequencedMap\nputFirst/putLast, pollFirstEntry, reversed()" {
  width: 440
  height: 70
  style.fill: "#e8f5e9"
}
impl: "implementors: List, Deque, LinkedHashSet,\nSortedSet, LinkedHashMap, SortedMap\n(not HashSet — no encounter order)" {
  width: 520
  height: 85
  style.fill: "#fff8e1"
}
sc -> ss
sc -> sm
sc -> impl
```

**Fig. 1.** One root interface with the positional API, two refinements for sets and maps, and the implementor set — `HashSet` stays out for lack of defined order.

```java
import java.util.LinkedHashMap;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.SequencedCollection;
import java.util.SequencedMap;
import java.util.SequencedSet;
import java.util.TreeSet;

public class V23_Sequenced {
    public static void main(String[] args) {
        List<String> list = List.of("a", "b", "c");        // List is SequencedCollection
        System.out.println("reversed view: " + list.reversed());
        System.out.println("getFirst/getLast: " + list.getFirst() + "/" + list.getLast());

        SequencedSet<String> set = new LinkedHashSet<>();
        set.addFirst("lead");
        set.addLast("tail");
        System.out.println("linked set: " + set);

        SequencedMap<String, Integer> map = new LinkedHashMap<>();
        map.putFirst("k", 1);
        System.out.println("map reversed: " + map.reversed());

        try {
            new TreeSet<String>().addFirst("x");
        } catch (UnsupportedOperationException e) {
            System.out.println("SortedSet.addFirst -> UnsupportedOperationException");
        }
        System.out.println("is SequencedCollection: " + (list instanceof SequencedCollection<?>));
    }
}
```

**Listing 1.** Verified on JDK 21 (V23_Sequenced in empirics): `reversed view: [c, b, a]`, `getFirst/getLast: a/c`, `linked set: [lead, tail]`, `map reversed: {k=1}`, `SortedSet.addFirst -> UnsupportedOperationException`, `is SequencedCollection: true` — the view semantics and the optional-method edge in one run (out/V23_Sequenced.txt).

> [!warning] reversed() is a view and SequencedSet reversal forbids reordering
> The traps: mutating through `reversed()` mutates the original — code assuming a snapshot double-applies changes; for `List` the view supports `set`, so writes flow both ways. `reversed()` of a `SequencedSet` rejects `addFirst`/`addLast` (order is derivable, not positional) — a `UnsupportedOperationException` surprise. And `getFirst` on an empty `List` throws `NoSuchElementException`; `Deque` veterans expecting `peekFirst`'s `null` are reading the wrong contract ([[What is the Java Collections Framework interface hierarchy]], [[What was new in Java 21]]).

> [!tip] Interview answer
> **JEP 431 (Java 21) added SequencedCollection/Set/Map: uniform getFirst/getLast, addFirst/addLast, and a live reversed() view — retrofitted onto List, Deque, LinkedHash types, and Sorted collections; HashSet stays out.** Edges: getFirst throws on empty, SortedSet can't reposition, reversed SequencedSet forbids reordering.
