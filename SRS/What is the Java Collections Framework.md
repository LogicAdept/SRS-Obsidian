<!--
reps: 0
priority: 0
-->
#Java/Collections #SRS

# What is the Java Collections Framework?

> [!abstract] Short answer
> The Java Collections Framework (JCF) is the **unified architecture in `java.util` and `java.util.concurrent`** for representing and manipulating groups of objects. It combines three pillars: **interfaces** (`Collection`, `Map` and their subinterfaces), **reusable implementations** (`ArrayList`, `HashMap`, …), and **polymorphic algorithms** — the static methods of `Collections` such as `sort` and `binarySearch`, plus wrapper factories. It arrived in Java 1.2 and replaced the ad-hoc `Vector`/`Hashtable` era.

## Three pillars, one framework

The Javadoc describes the framework as interfaces, implementations, and algorithms operating through them. A fourth convenience layer rides on top: **wrapper collections** produced by `Collections.unmodifiableList`, `Collections.synchronizedMap` and friends — views that delegate to a backing collection instead of storing elements. The `Collection` root covers element containers ([[What is collection]]), while `Map` models key-to-value mappings as a separate hierarchy; both are part of the same framework even though `Map` does not extend `Collection` ([[Why does Map not extend the Collection interface]]).

```d2
direction: right
interfaces: "Interfaces\nCollection · Map · List · Set · Queue" {
  width: 300
  height: 80
  style.fill: "#e3f2fd"
}
impls: "Implementations\nArrayList · HashSet · TreeMap · ArrayDeque" {
  width: 330
  height: 80
  style.fill: "#fff3e0"
}
algos: "Algorithms & wrappers\nCollections.sort · unmodifiableList" {
  width: 330
  height: 80
  style.fill: "#e8f5e9"
}
interfaces -> impls: "implemented by"
algos -> interfaces: "operate on"
```

**Fig. 1.** Code programs against interfaces; implementations provide storage; `Collections` supplies algorithms and views.

Java 21 refined the interface pillar with `SequencedCollection` and `SequencedMap` — common `getFirst`/`addFirst`/`reversed` operations for collections and maps with encounter order. The exact family tree is its own card: [[What is the Java Collections Framework interface hierarchy]]. The concurrent half of the framework lives in `java.util.concurrent`: `ConcurrentHashMap`, `CopyOnWriteArrayList`, blocking queues.

```java
List<String> names = new ArrayList<>(List.of("beta", "alpha"));
Collections.sort(names);                       // polymorphic algorithm
System.out.println(names);

List<String> guarded = Collections.unmodifiableList(names); // wrapper view
System.out.println(guarded.getFirst());        // Java 21 sequenced API
```

**Listing 1.** Interfaces, implementation, algorithm and wrapper in four lines. Verified on JDK 21 — output: `[alpha, beta]` / `alpha`.

> [!warning] "Collections Framework = only things extending Collection" is a popular lie
> `Map` is a first-class framework member without extending `Collection`, and the legacy `Vector`, `Hashtable`, `Stack` predate the framework but still implement it today. Conversely, `java.util.Arrays` helpers are framework-adjacent but live outside `Collections`.

> [!tip] Interview answer
> **The JCF is the standard library architecture for object groups: a small set of interfaces (`Collection`, `Map`, `List`, `Set`, `Queue`), general-purpose implementations (`ArrayList`, `HashMap`, `TreeMap`, …), and reusable algorithms and wrappers in `Collections`.** It separates what a container does (interface) from how it stores elements (implementation), so code written against `List` survives an implementation swap, and Java 21 added the `Sequenced*` interfaces for encounter-order operations.
