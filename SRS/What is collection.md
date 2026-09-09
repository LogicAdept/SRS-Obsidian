<!--
reps: 0
priority: 0
-->
#Java/Collections #SRS

# What is a `Collection` in Java?

> [!abstract] Short answer
> A `Collection` is **a group of objects called its elements**: the root interface of the collection hierarchy. It declares the minimum every element-container shares — `add`, `remove`, `contains`, `size`, `iterator`, `toArray` and the bulk operations — while `Set`, `List` and `Queue` are its specialized subinterfaces. The JDK ships no direct `Collection` implementations; you instantiate a `Set`/`List`/`Queue` type and pass it around as `Collection` when maximum generality is needed.

## Where it sits in the hierarchy

`public interface Collection<E> extends Iterable<E>` — extending `Iterable` is what lets any collection feed the for-each loop and `stream()` ([[How are Iterable Iterator and for-each related in Java]]). The JDK provides implementations only of the subinterfaces, exactly because "a collection" is deliberately vague: some allow duplicates, some do not; some are ordered, some are unordered. Collections with a defined encounter order are subtypes of `SequencedCollection` (Java 21).

```d2
direction: right
it: "Iterable<E>\nfor-each, forEach" {
  width: 210
  height: 80
  style.fill: "#e3f2fd"
}
c: "Collection<E>\ngroup of elements" {
  width: 230
  height: 80
  style.fill: "#fff3e0"
}
subs: "Set · List · Queue\n(+ SequencedCollection, Java 21)" {
  width: 320
  height: 80
  style.fill: "#e8f5e9"
}
impls: "JDK: no direct Collection\nimplementations — only\nof subinterfaces" {
  width: 300
  height: 90
  style.fill: "#ffebee"
}
it -> c: "extends"
c -> subs: "specializes"
c -> impls: "not instantiated directly"
```

**Fig. 1.** `Collection` is the root element-container type; concrete classes always implement one of its subinterfaces.

## The contract you get

The root interface fixes vocabulary, not storage: `size()`, `isEmpty()`, `contains(Object)`, `add(E)`, `remove(Object)`, `iterator()`, `toArray`, plus bulk operations `containsAll`, `addAll`, `removeAll`, `retainAll`, `clear`. Two details of that contract matter in interviews. First, `add` returns `true` if the collection changed — a `Set` returns `false` on a duplicate, but any implementation that refuses an element for another reason must throw an exception rather than return `false`. Second, many methods are **optional operations**: an unmodifiable collection defines `add`/`remove` to throw `UnsupportedOperationException` instead of silently doing nothing.

```java
Collection<String> c = new ArrayList<>();
c.add("delta");
c.add("alpha");
c.remove("delta");
System.out.println(c.size() + " " + c.contains("alpha"));
for (String s : c) {          // works: Collection extends Iterable
    System.out.println(s);
}
```

**Listing 1.** Only root-interface methods are used; the loop relies on `Collection` extending `Iterable`. Verified on JDK 21 — output: `1 true` / `alpha`.

The interface also pins down the **standard constructors convention** for implementations: a no-arg constructor creating an empty collection, and a constructor taking a `Collection` that copies its elements — that is how `new ArrayList<>(someSet)` can convert between types. `equals` is left to subinterfaces: `List` compares element-wise in order, `Set` ignores order, and a direct `Collection` (a "bag"/multiset) must not equal a `List` or a `Set`.

> [!warning] `Collection` is not `Collections`
> `java.util.Collection` is the **interface**; `java.util.Collections` is a **static utility class** of algorithms and wrappers. Mixing them up in signatures is a classic interview slip — the distinction is its own card: [[What is the difference between the Collection interface and the Collections utility class]].

> [!tip] Interview answer
> **`Collection` is the root interface for element containers: a group of objects with `add`, `remove`, `contains`, `size`, iteration and bulk operations.** It extends `Iterable`, its main subinterfaces are `Set`, `List` and `Queue`, and the JDK provides no direct implementations — you work with `ArrayList`, `HashSet` and friends, and accept `Collection` as a parameter when the method only needs "some elements".
