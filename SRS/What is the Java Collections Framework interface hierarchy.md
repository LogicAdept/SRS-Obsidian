<!--
reps: 0
priority: 0
-->
#Java/Collections #SRS

# What is the Java Collections Framework interface hierarchy?

> [!abstract] Short answer
> The framework has **two separate interface trees**. The element tree: `Iterable` → `Collection` → `Set`, `List`, `Queue`, with `SequencedCollection` (Java 21) inserted between `Collection` and `List`, and `Set` → `SortedSet` → `NavigableSet`. The mapping tree starts at `Map`: `Map` → `SortedMap` → `NavigableMap`, plus `SequencedMap` (Java 21). `Deque` extends `Queue`; `Map` extends neither `Collection` nor `Iterable`.

## The element tree and the mapping tree

Each edge below is verifiable in the type signature of the Javadoc page: `Collection<E> extends Iterable<E>`, `Deque` "extends the `Queue` interface", `NavigableSet` extends `SortedSet`. Java 21 added `SequencedCollection` for containers with encounter order — it declares `getFirst`/`getLast`, default `addFirst`/`addLast` (throwing `UnsupportedOperationException` unless overridden) and `reversed()`, which returns a reverse-ordered view. `List` and `SequencedSet` are its subinterfaces; `LinkedHashSet` is the JDK's `SequencedSet`.

```d2
direction: down
iterable: "Iterable<E>" {
  width: 240
  height: 64
  style.fill: "#e3f2fd"
}
collection: "Collection<E>" {
  width: 240
  height: 64
  style.fill: "#e3f2fd"
}
sequenced: "SequencedCollection<E>\n(Java 21)" {
  width: 280
  height: 72
  style.fill: "#fff3e0"
}
list: "List<E>" {
  width: 180
  height: 60
  style.fill: "#e8f5e9"
}
sset: "SequencedSet<E>\n(Java 21)" {
  width: 220
  height: 60
  style.fill: "#e8f5e9"
}
set: "Set<E>" {
  width: 180
  height: 60
  style.fill: "#e8f5e9"
}
sortedset: "SortedSet<E>" {
  width: 200
  height: 60
  style.fill: "#e8f5e9"
}
navset: "NavigableSet<E>" {
  width: 220
  height: 60
  style.fill: "#e8f5e9"
}
queue: "Queue<E>" {
  width: 180
  height: 60
  style.fill: "#e8f5e9"
}
deque: "Deque<E>" {
  width: 180
  height: 60
  style.fill: "#e8f5e9"
}
map: "Map<K, V>\nseparate root" {
  width: 250
  height: 70
  style.fill: "#ffebee"
}
sortedmap: "SortedMap<K, V>" {
  width: 210
  height: 60
  style.fill: "#ffebee"
}
navmap: "NavigableMap<K, V>" {
  width: 230
  height: 60
  style.fill: "#ffebee"
}
seqmap: "SequencedMap<K, V>\n(Java 21)" {
  width: 240
  height: 60
  style.fill: "#ffebee"
}

iterable -> collection
collection -> sequenced
collection -> set
collection -> queue
sequenced -> list
set -> sset
sequenced -> sset
set -> sortedset
sortedset -> navset
queue -> deque
map -> sortedmap
sortedmap -> navmap
map -> seqmap
```

**Fig. 1.** Two roots: `Collection` (elements, reached from `Iterable`) and `Map` (key-value mappings). `Sequenced*` interfaces (Java 21) cover encounter order.

```java
List<String> list = new ArrayList<>();
System.out.println(list instanceof SequencedCollection); // Java 21

Deque<Integer> deque = new ArrayDeque<>();
System.out.println(deque instanceof Queue);              // Deque extends Queue

System.out.println(new LinkedHashSet<String>() instanceof SequencedSet);
```

**Listing 1.** Three hierarchy edges as runtime checks. Verified on JDK 21 — output: `true` / `true` / `true`.

## Why the two-tree shape matters

The split answers "is a `TreeMap` a `Collection`?" — no: it is a `NavigableMap`, outside the element tree, though its views (`keySet`, `values`, `entrySet`) hand back real collections. The nested levels also carry contracts you must not flatten: `SortedSet` adds ordering to `Set`, and `NavigableSet` adds ceiling/floor/headSet/tailSet navigation ([[What NavigableSet operations does TreeSet provide]]) — `TreeSet` implements all three names.

> [!warning] Do not memorize the hierarchy as "Collection has four children"
> `Collection`'s direct children in the JDK also include the concurrency interfaces (`BlockingQueue`, `TransferQueue`) and `SequencedCollection`; `Deque` extends `Queue` but nothing connects `Deque` to `List`. And `Map` is not "below" `Collection` — the rationale has its own card: [[Why does Map not extend the Collection interface]].

> [!tip] Interview answer
> **There are two trees: `Iterable` → `Collection` → `Set`/`List`/`Queue` (with `SortedSet` → `NavigableSet` under `Set`, `Deque` under `Queue`, and `SequencedCollection` from Java 21), and a separate `Map` tree with `SortedMap` → `NavigableMap` and `SequencedMap`.** `Map` is deliberately outside the element hierarchy; everything else is an element container that inherits `Iterable`'s for-each support.
