<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/Hashtable #Java/Collections/Map/HashMap #Java/Legacy #SRS

# What is `java.util.Dictionary` and how does `Hashtable` relate to it?

> [!abstract] Short answer
> **`Dictionary` is the obsolete 1.0 abstract class for a key–value table.** `Hashtable` is its concrete subclass (`extends Dictionary`) and, since 1.2, also a `Map`. `Map` **replaced** `Dictionary` (which was a class, not an interface). `HashMap` extends `AbstractMap`, not `Dictionary`. Do not write new dictionaries; implement `Map`.

## Obsolete parent; `Hashtable` is the live subclass

`Dictionary`: abstract parent of any class, such as `Hashtable`, that maps keys to values. Every key and value is an object; in one dictionary each key maps to at most one value. Implementations should use `equals` to decide if two keys are the same. Any **non-null** object may be a key or value. `put` throws `NullPointerException` if the key or value is null. `Since: 1.0`. [[Does Hashtable allow null keys or values]]

Official note: this class is **obsolete**. New implementations should implement `Map` rather than extending `Dictionary`. `Map` “takes the place of the `Dictionary` class, which was a totally abstract class rather than an interface.” [[What is the Map interface in Java]] [[Is Hashtable deprecated]]

`Hashtable` extends `Dictionary` and implements `Map` (retrofit in Java 2 / 1.2). You can still write `Dictionary d = new Hashtable()` and walk `keys()` / `elements()` with `Enumeration`. Those methods are the `Dictionary` API. Collection views (`keySet`, …) are the `Map` API; their iterators are fail-fast, while `keys()`/`elements()` enumerations are not. [[In which Java version was Hashtable introduced]] [[Are Hashtable enumerations fail-fast]] [[In which Java version was Iterator introduced]]

```d2
direction: down
dict: "Dictionary (abstract)\nobsolete, 1.0\nkeys()/elements()" {
  width: 280
  height: 80
  style.fill: "#fff3e0"
}
ht: "Hashtable\nextends Dictionary\nimplements Map (1.2)" {
  width: 280
  height: 80
  style.fill: "#e3f2fd"
}
am: "AbstractMap" {
  width: 200
  height: 50
  style.fill: "#c8e6c9"
}
hm: "HashMap\nextends AbstractMap" {
  width: 240
  height: 70
  style.fill: "#c8e6c9"
}

dict -> ht
am -> hm
```

**Fig. 1.** Two lineages. `Hashtable` is both a `Dictionary` and a `Map`. `HashMap` never was a `Dictionary`.

```java
Dictionary<String, Integer> dictionary = new Hashtable<>();
dictionary.put("one", 1);          // NPE if key or value is null
Enumeration<Integer> values = dictionary.elements();
Enumeration<String> keys = dictionary.keys();

Map<String, Integer> map = new HashMap<>(); // AbstractMap, permits nulls
```

**Listing 1.** Conceptual dump sample: the compile-time type is `Dictionary`; the runtime type is `Hashtable`. Prefer `Map` + `HashMap` / `ConcurrentHashMap` for new code. [[What is the difference between HashMap and Hashtable]] [[Can you unsynchronize a Hashtable]]

`Properties` is a `Hashtable` subclass, so it is still a `Dictionary` too. That is a compatibility leftover, not a reason to extend `Dictionary` yourself.

> [!warning] “Dictionary is just the old name for Map”
> `Map` is an interface with collection views and optional operations. `Dictionary` is an abstract class with `Enumeration keys()` / `elements()`. Assigning a `Hashtable` to `Dictionary` does not make it a recommended API. Calling `Hashtable` legacy while using `new Hashtable()` as your `Dictionary` is the same class.

> [!tip] Interview answer
> **`Dictionary` is the obsolete 1.0 abstract key–value class; `Hashtable` extends it.** Since 1.2 `Hashtable` also implements `Map`, which replaced `Dictionary`. `HashMap` extends `AbstractMap`. New code implements `Map`, does not extend `Dictionary`, and does not pick `Hashtable` for a new map.
