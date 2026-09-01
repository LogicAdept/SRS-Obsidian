<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/ConcurrentHashMap #Java/Versions/5 #SRS

# In which Java version was `ConcurrentHashMap` introduced?

> [!abstract] Short answer
> **Java 5 (`@since 1.5`).** Same wave as `java.util.concurrent` and `CopyOnWriteArrayList`. It is not a Java 6 collections add-on. `Hashtable` is older (`@since 1.0`). Java 7 segment locks and the Java 8 CAS / `synchronized` rewrite are later implementations of the same class.

## 1.5 is the class; later numbers are APIs and internals

The class page still says **Since: 1.5**. A few members are newer: the `(initialCapacity, loadFactor)` constructor is **1.6**; `mappingCount()`, `newKeySet()`, and the parallel bulk methods are **1.8**. Those dates do not move the type’s birth.

```d2
direction: right
j5: "1.5\nConcurrentHashMap\nclass added" {
  width: 200
  height: 80
  style.fill: "#e8f5e9"
}
j7: "Java 7\nSegment locks" {
  width: 180
  height: 80
  style.fill: "#fff8e1"
}
j8: "Java 8\nCAS + synchronized(bin)" {
  width: 220
  height: 80
  style.fill: "#fff3e0"
}
j5 -> j7
j7 -> j8
```

**Fig. 1.** Introduction is 1.5. Stripe locks and bin CAS are redesigns, not new types.

`Hashtable` predates the Collections Framework ([[In which Java version was Hashtable introduced]]; drawbacks: [[How would you explain drawbacks of the legacy Hashtable class]]). Concurrent map locking in 7 vs 8: [[How does ConcurrentHashMap use Segment locks in Java 7]], [[How does ConcurrentHashMap use CAS and synchronized in Java 8]], [[Why did ConcurrentHashMap drop segment locks in Java 8]]. Retrievals never locked the whole table, from the first spec onward ([[Does ConcurrentHashMap get lock the whole table]]).

```text
ConcurrentHashMap          @since 1.5   class
CopyOnWriteArrayList       @since 1.5   same jsr.166 / concurrent package
Hashtable                  @since 1.0
ConcurrentHashMap(cap, lf) @since 1.6   one constructor
mappingCount / bulk ops    @since 1.8   extra API
```

**Listing 1.** Dump lists that park `ConcurrentHashMap` in Java 6 collide with the class `@since` and with `CopyOnWriteArrayList`’s `@since 1.5`.

```java
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.CopyOnWriteArrayList;

class Demo {
    static void j5Types() {
        ConcurrentHashMap<String, Integer> map = new ConcurrentHashMap<String, Integer>();
        CopyOnWriteArrayList<String> list = new CopyOnWriteArrayList<String>();
        map.put("a", 1);
        list.add("a");
    }
}
```

**Listing 2.** Both types compile on a Java 5-era `java.util.concurrent` mental model; the rewrite years do not change the import.

> [!warning] “Java 6 concurrent collections” is the wrong bucket
> `ConcurrentHashMap` and `CopyOnWriteArrayList` are **1.5**. Java 6 added other library pieces; it did not introduce this map. Do not use a later constructor or `mappingCount` `@since` as the class’s birthday.

> [!warning] Java 7 / 8 answers are not the introduction
> Segment locks and per-bin CAS are how `put` is implemented in those releases. Interview follow-ups about stripes vs bins still start from “the class arrived in 1.5.”

> [!tip] Interview answer
> **`ConcurrentHashMap` has been in the JDK since Java 5 (`@since 1.5`), with `Hashtable` dating to 1.0.** Java 6 is a common wrong bucket for the whole concurrent-collections package. Java 7 and 8 changed locking inside the same class — they did not add it.
