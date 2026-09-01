<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/Hashtable #Java/Collections/Map/HashMap #Java/Legacy #Java/Versions #SRS

# In which Java version was `Hashtable` introduced?

> [!abstract] Short answer
> **Java 1.0 (`Since: 1.0`).** It predates the Collections Framework. In Java 2 / **1.2** it was retrofitted to implement `Map`. `HashMap` is 1.2; `ConcurrentHashMap` is 1.5. The parent type `Dictionary` and `Enumeration` are also 1.0; `Iterator` is 1.2.

## 1.0 class, 1.2 `Map`

The `Hashtable` javadoc: `Since: 1.0`. As of the Java 2 platform v1.2 it implements `Map`, making it a Collections Framework member. Unlike the new collection implementations, it is synchronized. If you do not need thread safety, use `HashMap`; if you want a concurrent map, use `ConcurrentHashMap`. [[What is the difference between HashMap and Hashtable]] [[Can you unsynchronize a Hashtable]] [[In which Java version was ConcurrentHashMap introduced]]

`Dictionary` is the obsolete abstract parent (`Since: 1.0`); new code should implement `Map` rather than extend `Dictionary`. `Hashtable` still extends it. [[What is java.util.Dictionary and how does Hashtable relate to it]]

```d2
direction: right
j10: "1.0\nHashtable\nDictionary\nEnumeration" {
  width: 220
  height: 90
  style.fill: "#fff3e0"
}
j12: "1.2\nMap retrofit\nHashMap\nIterator" {
  width: 220
  height: 90
  style.fill: "#e3f2fd"
}
j15: "1.5\nConcurrentHashMap" {
  width: 220
  height: 70
  style.fill: "#c8e6c9"
}

j10 -> j12
j12 -> j15
```

**Fig. 1.** `Hashtable` is the 1.0 hash table. “Legacy vs `HashMap`” is a **1.2** story, not the introduction date.

```java
Hashtable<String, Integer> table = new Hashtable<>(); // API since 1.0
table.put("one", 1);
Enumeration<String> keys = table.keys(); // 1.0 Enumeration, not fail-fast

Map<String, Integer> map = new HashMap<>(); // since 1.2
```

**Listing 1.** Conceptual: `keys()` / `elements()` are the 1.0 `Enumeration` API. Collection-view iterators (1.2 `Map`) are fail-fast. [[In which Java version was Iterator introduced]] [[Are Hashtable enumerations fail-fast]]

`Enumeration` (`Since: 1.0`) still documents hashtable keys/values as a motivating example. `Iterator` (`Since: 1.2`) “takes the place of `Enumeration` in the Java Collections Framework.” Same 1.0 / 1.2 split as `Hashtable` / `HashMap`. [[Is Hashtable deprecated]]

> [!warning] “Legacy, so it came in 1.2 with HashMap”
> Interview tables often date **`HashMap`** to 1.2 and only call `Hashtable` “legacy.” The class itself is **1.0**. 1.2 is when it became a `Map`. Do not answer “Java 5” because `ConcurrentHashMap` is the concurrent replacement.

> [!tip] Interview answer
> **`Hashtable` has been in Java since 1.0.** It became a `Map` in 1.2, when `HashMap` and `Iterator` arrived. `ConcurrentHashMap` is 1.5. `Dictionary` and `Enumeration` are the 1.0 parent/iterator pair; both are obsolete relative to `Map` / `Iterator`.
