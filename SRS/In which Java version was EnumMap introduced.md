<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/EnumMap #Java/Versions/5 #Java/Language/Enum #SRS

# In which Java version was `EnumMap` introduced?

> [!abstract] Short answer
> **Java 5 (`Since: 1.5`).** It shipped with language enums: `java.lang.Enum` is also 1.5, and `Enum.ordinal` is documented for structures such as `EnumMap` and `EnumSet`. It is not a Java 8 collections add-on.

## 1.5 is the collections companion of `enum`

The `EnumMap` javadoc marks the class `Since: 1.5`. Keys must be a single enum type specified at construction — a type that did not exist in the language before 5. `Enum` itself is `Since: 1.5`. The `Enum` overview points at specialized map/set implementations when the key or element type is an enum; `ordinal()` is “designed for use by sophisticated enum-based data structures, such as `EnumSet` and `EnumMap`.” [[How do you create an EnumMap]] [[What special collections exist for Java enums]] [[Why prefer EnumMap when the keys are enum constants]]

`ConcurrentHashMap` is also 1.5. Earlier maps: `Hashtable` 1.0, `HashMap` / `WeakHashMap` 1.2, `IdentityHashMap` / `LinkedHashMap` 1.4. None of those are enum-specialized. [[In which Java version was ConcurrentHashMap introduced]] [[In which Java version was IdentityHashMap introduced]]

```d2
direction: right
j12: "1.2\nHashMap\nWeakHashMap" {
  width: 180
  height: 80
  style.fill: "#e3f2fd"
}
j14: "1.4\nLinkedHashMap\nIdentityHashMap" {
  width: 200
  height: 80
  style.fill: "#fff3e0"
}
j15: "1.5\nenum, Enum,\nEnumMap, CHM" {
  width: 220
  height: 90
  style.fill: "#c8e6c9"
}

j12 -> j14
j14 -> j15
```

**Fig. 1.** `EnumMap` arrives with the `enum` keyword, not with Java 8 streams or Java 21 sequenced maps.

```java
enum State { NEW, RUNNING }

// Legal from Java 5 onward
EnumMap<State, String> m = new EnumMap<>(State.class);
m.put(State.NEW, "boot");
```

**Listing 1.** Conceptual: the `Class`-token constructor is the 1.5 API. [[In what order does EnumMap iterate]]

Do not treat “JDK 5 language features” as a dump checklist unless each item is sourced. Enums and `EnumMap` are the pair the javadocs actually tie together.

> [!warning] “EnumMap came with Java 8 Map.of / default methods”
> `Since: 1.5` is the class, not `Map`’s Java 8 defaults. You could `put` enum keys in a `HashMap` in 1.2; `EnumMap` is the compact array map that requires the 1.5 enum type. `1.5` and “Java 5” are the same release.

> [!tip] Interview answer
> **`EnumMap` was added in Java 5 (`1.5`), together with the `enum` language feature.** `java.lang.Enum` is 1.5, and `ordinal` exists for `EnumMap` / `EnumSet`. It is not a Java 8 collection.
