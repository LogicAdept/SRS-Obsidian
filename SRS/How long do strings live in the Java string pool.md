<!--
reps: 0
priority: 0
-->
#Java/String #Java/JVM/Memory/Heap #SRS

# How long do strings live in the Java string pool

> [!abstract] Short answer
> **As long as the interned `String` object is reachable — not “until the JVM exits.”** `String.intern`’s pool does not keep a strong pin on the instance. HotSpot’s string table stores a **weak handle**; when nothing else refers to that `String`, GC can clear it and a later `intern` of the same characters may allocate a **new** interned object. Literals stay reachable through the class’s run-time constant pool while the class is loaded (bootstrap classes never unload).

## Reachability, not a permanent generation forever

The intern pool is a private table of canonical `String`s (`equals` match → same instance). That is an identity cache, not a second immortal heap. The interned object is an ordinary heap `String` ([[Which memory region holds the string pool in Java]]).

HotSpot (`StringTable`) inserts a `WeakHandle`. Table lookup treats `peek() == null` as a **dead** entry and cleans those after GC. A concurrent intern can fail to see a just-collected entry and retry. So interned strings **are** garbage-collected; the table is not a GC root that keeps them alive.

What **does** keep them alive:

- A live local, field, or collection holding the interned reference.
- A loaded class’s run-time constant pool, which points at the interned instance for each `CONSTANT_String` ([[How do string literals enter the Java string pool]]). That lasts until the class can be unloaded — only if its defining loader can be reclaimed. Bootstrap-loaded classes **cannot** be unloaded, so JDK and application literals from those classes live for the VM lifetime.
- Your own `intern()` result, until you drop it.

A unique `intern()` of data you then forget (log lines, tokens, XML) can be collected. Filling the table with distinct interned strings still competes for **heap** (`-Xmx`); it is not a separate PermGen leak on modern HotSpot.

Java 7 moved interned strings **out of PermGen onto the Java heap**. Java 8 removed PermGen (class metadata → Metaspace). The old interview line “interned strings live in PermGen until the JVM dies” describes neither current layout nor even old GC: interned strings were collected when PermGen was collected. G1 **string deduplication** is a different table; HotSpot will not deduplicate a string **after** it has been interned.

```d2
direction: down
obj: "Interned String\n(Java heap object)" {
  width: 260
  height: 50
}
strong: "Strong refs\nCP of loaded class · fields · stacks" {
  width: 320
  height: 50
}
table: "StringTable WeakHandle\npeek() null → dead entry" {
  width: 300
  height: 50
}
gc: "Unreachable?\nGC may collect; intern may recreate" {
  width: 300
  height: 50
}

strong -> obj: "keeps alive"
table -> obj: "does not pin"
obj -> gc: "no strong refs"
```

**Fig. 1.** The intern table tracks interned instances weakly. Lifetime follows ordinary reachability, plus class-constant-pool refs for literals.

```java
public class InternLifetimeDemo {
    static final String LITERAL = "lives with this class";

    static String internAndKeep(String built) {
        return built.intern(); // lives as long as the returned ref (and equals-matches)
    }

    static void internAndDrop(String built) {
        built.intern(); // if built is unique and dropped, HotSpot may collect it
    }
}
```

**Listing 1.** Literals are rooted by the class. An `intern()` you discard is not promised to stay in the pool. Do not write tests that assume a given GC cycle.

> [!warning] Intern is not immortality
> `s.intern() == t.intern()` holds for two live interned strings with equal content. It does **not** mean a pooled object survives after you drop every strong reference. Do not intern unbounded unique text to “save memory.” Do not mix this up with G1 string deduplication. Bootstrap literals are long-lived because **those classes** never unload, not because the pool is eternal.

> [!tip] Interview answer
> **Interned strings live while they are reachable.** HotSpot’s intern table holds only a weak handle, so unused interned objects can be collected from the heap. Literals stay alive with their loaded class; bootstrap classes never unload. They are not immortal PermGen entries on Java 7+.
