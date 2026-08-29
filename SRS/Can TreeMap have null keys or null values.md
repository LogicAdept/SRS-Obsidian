<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/TreeMap #Java/Exceptions/Unchecked #SRS

# Can `TreeMap` have null keys or null values?

> [!abstract] Short answer
> **Null keys: usually no. Null values: yes.** `put`, `get`, `remove`, and `containsKey` throw `NullPointerException` if the key is `null` **and** the map uses natural ordering, or its comparator does not permit null keys. Any number of keys may map to `null`. A comparator that accepts `null` (for example `Comparator.nullsFirst`) is the documented exception to “no null key.”

## Keys are compared; values are not

`TreeMap` is a red-black tree ordered by key `compareTo` (natural order) or by a `Comparator` supplied at construction. A `null` key has to participate in that comparison. Natural order has no `compareTo` to call, so `put(null, v)` is an NPE. A `Comparator` *may* permit null arguments; `put` only NPEs when that comparator does not.

Values are not part of the tree order. `put(k, null)` is not listed as throwing NPE. `get` states that a `null` return can mean “this key is mapped to `null`,” so you distinguish with `containsKey`. `containsValue(null)` is defined with the `(value==null ? v==null : value.equals(v))` test, which matches several mappings to `null`.

```d2
direction: down
key: "put(null, v)" {
  width: 260
  height: 50
  style.fill: "#fff3e0"
}
nat: "natural order\nor comparator forbids null" {
  width: 280
  height: 70
  style.fill: "#ffebee"
}
ok: "comparator permits null\n(e.g. nullsFirst)" {
  width: 280
  height: 70
  style.fill: "#e8f5e9"
}
val: "put(k, null)\nalways stored" {
  width: 260
  height: 70
  style.fill: "#e3f2fd"
}
key -> nat: "NPE"
key -> ok: "one null key"
```

**Fig. 1.** Null **key** depends on the ordering. Null **values** do not. See [[What types can you use as TreeMap keys]] and [[How do you customize TreeMap key order]].

```java
import java.util.Comparator;
import java.util.TreeMap;

class Demo {
    static void naturalOrder() {
        var m = new TreeMap<String, Integer>();
        m.put("a", null);
        m.put("b", null);
        m.containsValue(null); // true
        m.put(null, 1);         // NullPointerException
    }

    static void nullFriendlyKey() {
        var m = new TreeMap<String, Integer>(
                Comparator.nullsFirst(Comparator.naturalOrder()));
        m.put(null, 1);
        m.put("a", null);
    }
}
```

**Listing 1.** Natural-order map: several null values, no null key. `nullsFirst` (Java 8) is a comparator that considers `null` less than non-null, so that map may contain one null key.

Interview tables often contrast this with `HashMap`, which permits the null key and null values ([[Can HashMap store a null key]]). `Hashtable` permits neither ([[Does Hashtable allow null keys or values]]).

> [!warning] “TreeMap does not allow nulls”
> That lumps keys and values. The class specification does **not** ban null values. `put`'s NPE is only for a null **key** under natural order or a comparator that rejects null. `get(k) == null` is ambiguous: missing key **or** a stored null value.

> [!warning] `computeIfAbsent` will not store a null
> If the mapping function returns `null`, no mapping is recorded. That is a `Map` default-method rule on this class, not a ban on `put(k, null)`. Use `put` when you intend a present-but-null value. Equality of keys still follows the map's ordering, which must be consistent with `equals` for a correct `Map` — see [[How does TreeMap decide whether two keys are the same]].

> [!tip] Interview answer
> **Default `TreeMap` (natural order): no null keys — `put(null, v)` throws `NullPointerException` — and yes, any number of null values. A `Comparator` that permits null, such as `Comparator.nullsFirst`, can allow a null key. Do not say “TreeMap forbids nulls”; that confuses keys with values.**
