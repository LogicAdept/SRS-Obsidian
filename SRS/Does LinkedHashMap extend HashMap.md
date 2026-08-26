<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/LinkedHashMap #Java/Collections/Map/HashMap #SRS

# Does `LinkedHashMap` extend `HashMap`?

> [!abstract] Short answer
> **Yes.** In the Java SE API, `LinkedHashMap` is declared as a subclass of `HashMap`. It keeps the hash-table map mechanics and adds a doubly-linked list through its entries so encounter order is defined. Since Java 21 it also implements `SequencedMap`.

## Class relationship

```d2
direction: down
map: "Map / SequencedMap (21+)" {
  width: 260
  height: 70
  style.fill: "#e3f2fd"
}
hm: "HashMap\nbuckets, hash, equals" {
  width: 260
  height: 70
  style.fill: "#fff3e0"
}
lhm: "LinkedHashMap\nextends HashMap\n+ entry before/after links" {
  width: 280
  height: 90
  style.fill: "#e8f5e9"
}

map -> hm
hm -> lhm
```

**Fig. 1.** `HashMap` lists `LinkedHashMap` among its direct known subclasses. Lookup still goes through the table; iteration follows the list.

```java
public class LinkedHashMap<K,V>
        extends HashMap<K,V>
        implements SequencedMap<K,V> {
    // ...
}
```

**Listing 1.** Conceptual class header matching the Java SE 21 declaration (package `java.util`).

Because it **is-a** `HashMap`, constructors reuse capacity and load factor, and `instanceof HashMap` is true for a `LinkedHashMap`. Behavioral differences (order, access-order, `removeEldestEntry`) live in the subclass; see [[What is the difference between HashMap and LinkedHashMap]] and [[What are LinkedHashMap ordering guarantees]].

## What “linked list” means here

The javadoc’s phrase is **hash table and linked list** implementation of `Map`: a doubly-linked list **running through all of its entries**, not a separate `java.util.LinkedList` that replaces the table.

```java
// Conceptual OpenJDK shape (Java 8+)
static class Entry<K,V> extends HashMap.Node<K,V> {
    Entry<K,V> before, after;
}
```

**Listing 2.** Conceptual entry type: bin `next` from `HashMap.Node`, plus `before`/`after` for encounter order (`head` eldest, `tail` youngest).

> [!warning] “Hash table” ≠ `Hashtable`
> Interview dumps sometimes say “Hashtable and linked list.” The official wording is a **hash table** (the `HashMap` structure) **plus** entry links. `LinkedHashMap` does **not** extend `Hashtable`.

> [!tip] Interview answer
> **Yes — `LinkedHashMap` extends `HashMap`.** It inherits the bucket table and adds a doubly-linked list across entries for insertion- or access-order iteration. That list is not `LinkedList` as the map’s storage, and it is not built on `Hashtable`.
