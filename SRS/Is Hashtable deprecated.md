<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/Hashtable #Java/Collections/Map/HashMap #Java/Collections/Map/ConcurrentHashMap #Java/Legacy #SRS

# Is `Hashtable` deprecated?

> [!abstract] Short answer
> **No — the class is not `@Deprecated`.** It has been in Java since 1.0. The javadoc still recommends **not** using it for new maps: `HashMap` if you do not need thread safety, `ConcurrentHashMap` if you do. The parent `Dictionary` is marked **obsolete**. “Legacy / not recommended” is not the same as `@Deprecated`.

## Still in the JDK; replacements are named

`Hashtable` implements `Map` (since Java 2 / 1.2) and is synchronized, unlike the post-1.2 collection implementations. OpenJDK `jdk-21-ga` declares `public class Hashtable` with **no** `@Deprecated` on the type or its methods. The class javadoc’s advice is substitution, not a deprecation banner. [[In which Java version was Hashtable introduced]] [[Can you unsynchronize a Hashtable]] [[What is the difference between HashMap and Hashtable]]

`Dictionary` (`Since: 1.0`): “This class is obsolete. New implementations should implement the `Map` interface, rather than extending this class.” `Hashtable` still extends it. That obsolete note is on the **parent**, not an `@Deprecated` on `Hashtable`. [[What is java.util.Dictionary and how does Hashtable relate to it]]

```d2
direction: down
ht: "Hashtable\nnot @Deprecated\nsynchronized Map" {
  width: 280
  height: 80
  style.fill: "#fff3e0"
}
hm: "HashMap\nif no thread safety" {
  width: 260
  height: 70
  style.fill: "#c8e6c9"
}
chm: "ConcurrentHashMap\nif concurrent" {
  width: 260
  height: 70
  style.fill: "#e3f2fd"
}

ht -> hm
ht -> chm
```

**Fig. 1.** Official path is replace the type. Absence of `@Deprecated` does not mean “pick Hashtable.”

```java
Hashtable<String, Integer> legacy = new Hashtable<>(); // compiles; not deprecated
Map<String, Integer> local = new HashMap<>();
ConcurrentHashMap<String, Integer> shared = new ConcurrentHashMap<>();
```

**Listing 1.** Conceptual: all three compile on Java 21. Only the last two match the Hashtable javadoc’s recommendations. [[Why is ConcurrentHashMap faster than Hashtable]] [[How would you explain drawbacks of the legacy Hashtable class]] [[Is java.util.HashMap thread safe]]

It still appears in “Map implementations” lists because it implements `Map`. That is inventory, not a default. No null keys or values. `keys()` / `elements()` are 1.0 `Enumeration`s (not fail-fast); collection-view iterators are fail-fast.

> [!warning] “Obsolete, so @Deprecated, so the compiler will warn”
> You will not get a deprecation warning on `new Hashtable()`. “Not recommended” is the HashMap/CHM sentence. Calling the class obsolete mixes it up with `Dictionary`. Do not keep `Hashtable` in new code just because it is not annotated.

> [!tip] Interview answer
> **`Hashtable` is not `@Deprecated`.** It is a 1.0 synchronized map; the docs tell you to use `HashMap` or `ConcurrentHashMap` instead. `Dictionary` is obsolete. Legacy and “not recommended” are not the same as the annotation.
