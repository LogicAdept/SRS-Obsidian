<!--
reps: 0
priority: 0
-->
#Java/Immutability #Java/Collections #Java/OOP #SRS

# How are immutable objects used in Java APIs?

> [!abstract] Short answer
> Core APIs treat **values that must be shared** as immutable (or unmodifiable) objects: `String`, wrapper types, `java.time`, and factory-made lists/sets/maps. Callers **share** them as keys, messages, and return values without copying. Mutating operations **return a new instance** (`plus`, `with`, `concat`) instead of setters. **Unmodifiable** is not always **immutable**: `Collections.unmodifiableList` is a **view** of a live list; `List.of` forbids structural change but still reflects mutable **elements**. Why String: [[Why is java.lang.String immutable and final]]. Why immutability: [[Why is immutability valuable in Java programs]].

## Share values; copy on “change”

`String` is constant: its character sequence does not change, so instances can be shared. Literals and text blocks refer to `String` objects; `+` builds a new `String` when the result is not a constant expression. APIs take and return `String` for names, paths, messages, and map keys because sharing is safe.

Wrapper classes such as `Integer` are **value-based**: `equals`/`hashCode`/`toString` follow the wrapped value, factories may reuse instances, and you must not synchronize on them or rely on `==`. Prefer `valueOf` over deprecated constructors: [[Why were Integer constructors deprecated]]. `List.of` / `List.copyOf` lists are also value-based.

`java.time` (Java 8+) states that its types are **immutable and thread-safe**. Method prefixes encode that contract: `of`/`parse` create, `with`/`plus`/`minus` return another object, `get`/`is` read. Those types are meant to cross process and database boundaries as ISO values (birthday as `LocalDate`, timestamp as `Instant`).

```d2
direction: down
need: "API must share a value\n(key, message, timestamp, snapshot)" {
  width: 320
  height: 50
  style.fill: "#e3f2fd"
}
imm: "immutable type\nString, Integer, LocalDate" {
  width: 280
  height: 50
  style.fill: "#e8f5e9"
}
unmod: "unmodifiable collection\nList.of / copyOf" {
  width: 280
  height: 50
  style.fill: "#e8f5e9"
}
view: "unmodifiable view\nCollections.unmodifiableList" {
  width: 300
  height: 50
  style.fill: "#fff3e0"
}
need -> imm
need -> unmod
need -> view: "backing list still mutable"
```

**Fig. 1.** Platforms pick immutability for shareable values, unmodifiable factories for snapshots, and views when wrapping an existing collection.

```java
import java.time.LocalDate;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Map;

class Api {
    static Map<String, Integer> counts() {
        return Map.of("ok", 1); // unmodifiable, value-based, no nulls
    }

    static LocalDate expiry(LocalDate start) {
        return start.plusMonths(1); // new instance; start unchanged
    }

    static List<String> snapshot(List<String> live) {
        return List.copyOf(live); // independent; later live.add does not appear
    }

    static List<String> viewOf(List<String> live) {
        return Collections.unmodifiableList(live); // reads through
    }
}
```

**Listing 1.** Typical API shapes: internable keys, time arithmetic that returns a new value, `copyOf` as a defensive snapshot, `unmodifiableList` as a live view.

`List.of` / `copyOf`: no `add`/`set`/`remove` (always `UnsupportedOperationException`); no `null` elements; if an **element** is mutable, the list can **appear** to change. `Collections.unmodifiableList` forbids mutators on the **view** but still **reads through** to the backing list — mutating that list is visible. Hash-based maps require stable `hashCode`; immutable keys (`String`, wrappers) keep that contract: [[Why should equals and hashCode be overridden together]].

> [!warning] Unmodifiable view ≠ snapshot
> `Collections.unmodifiableList(live)` does not freeze `live`. A caller who still has `live` can `add`, and iterators on the view see it. For a frozen copy, use `List.copyOf(live)` (and do not put mutable elements in it if you need a true freeze).

> [!warning] Do not synchronize on `Integer`, `LocalDate`, or `List.of` results
> Value-based instances may be reused; identity-sensitive locking is unsupported and may fail in a later JDK. Lock a private mutex object instead.

> [!warning] Mutable elements punch through an “immutable” list
> `List.of(new StringBuilder("a"))` cannot replace the element slot, but `builder.append("x")` still changes what `get(0)` shows. Immutability of the **container** is not immutability of the **payload**.

> [!tip] Interview answer
> Java APIs use immutable types wherever a value is shared: String, wrappers, and java.time objects, with operations that return a new instance instead of mutating. Collection factories like List.of return unmodifiable, value-based lists for snapshots; Collections.unmodifiableList is only a view of a still-mutable list. Never treat unmodifiable plus mutable elements as a deep freeze, and never synchronize on value-based instances.
