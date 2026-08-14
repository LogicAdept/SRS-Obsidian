<!--
reps: 0
priority: 0
-->
#Java/Collections/Map #SRS

# What is the main purpose of the `Map` interface?

> [!abstract] Short answer
> **To look up a value by a key**, with at most one mapping per key. A `List` is indexed by position; a `Set` is a group of unique elements; a `Map` answers “what is stored under this key?” The Collections Framework overview calls `Map` and its offspring **not true collections**: they are a second family, with views so you can still walk keys, values, or entries as collections. [[What is the Map interface in Java]]

## Associative lookup, not a bag of elements

`Map`: an object that maps keys to values; no duplicate keys; each key maps to at most one value. The fundamental operations are `get` (the value for this key, or `null`) and `put` (associate this key with this value; replace if the key is already present). `containsValue` is specified as probably **linear** in the map size for most implementations — searching by value is not the point.

```text
List   element at index i
Set    is this element in the group?
Map    value for this key
```

**Listing 1.** Three jobs. `List` allows duplicate elements; `Set` forbids them; `Map` forbids duplicate **keys** and still allows duplicate values.

```d2
direction: down
q: "What do I have?" {
  width: 220
  height: 60
  style.fill: "#e3f2fd"
}
list: "sequence / index" {
  width: 200
  height: 60
  style.fill: "#fff3e0"
}
set: "unique elements" {
  width: 200
  height: 60
  style.fill: "#e8f5e9"
}
map: "key → unique slot\nfor a value" {
  width: 220
  height: 70
  style.fill: "#ffe0b2"
}
q -> list
q -> set
q -> map
```

**Fig. 1.** Pick `Map` when the identifier is an object (`String` id, enum, …), not an `int` position and not “membership only.”

The framework needed a small set of core interfaces. `Collection` covers groups of elements (`Set`, `List`, queues). Key-to-value tables were the other group, replacing the obsolete abstract class `Dictionary`. Views (`keySet`, `values`, `entrySet`) exist so maps **interoperate** with collection algorithms without making `Map` extend `Collection`.

## What purpose does not mean

It does not mean “store two equal keys.” A second `put` of an equal key **replaces**. It does not mean “find by value in constant time.” It does not pick `HashMap` vs `TreeMap`: those are implementations of the same purpose with different order and cost. [[What is a HashMap]]

> [!warning] “I need unique pairs, so Map”
> Uniqueness is on the **key**. Two keys can map to the same value. If both sides must be unique, that is two maps or a different model, not `Map` by itself.

> [!tip] Interview answer
> **`Map` exists to associate a unique key with a value and retrieve it with `get`. It is not a `Collection` of elements; the framework treats maps as a second family with collection views. Use `List` for index order and `Set` for unique elements.**
