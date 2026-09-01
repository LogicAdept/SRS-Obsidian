<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/IdentityHashMap #Java/Collections/Map/HashMap #Java/HashCodeEquals #Java/Immutability #SRS

# Must `IdentityHashMap` keys be immutable?

> [!abstract] Short answer
> **No — not for lookup.** `HashMap` needs a stable `equals`/`hashCode` while the object is a key. `IdentityHashMap` treats two keys as the same **if and only if** `k1 == k2`, and it buckets with **`System.identityHashCode`**, which ignores field values and any `hashCode` override. Mutating the object’s fields does not hide the mapping. You still look it up with the **same reference**.

## Why `HashMap` cares and this map does not

The general `Map` contract leaves behavior unspecified if you change a key **in a way that affects `equals` comparisons** while it remains in the map. `HashMap` is that kind of map: after `hashCode` picks a bucket, `get` / `containsKey` use null-safe `equals`. Change a field that participates in those methods and the table can miss the entry (wrong bucket, or `equals` no longer matches). That is why value keys are usually immutable. [[What requirements apply to keys used in a HashMap]] and [[Can you lose objects in a HashMap due to mutable or poorly chosen keys]] cover that failure.

`IdentityHashMap` is documented as **not** a general-purpose `Map`: it replaces object-equality with reference-equality. Java SE 21:

```text
IdentityHashMap  same key  ⇔  (k1 == k2)
HashMap          same key  ⇔  (k1==null ? k2==null : k1.equals(k2))

bucket index     System.identityHashCode(key)
                 (not key.hashCode())

get / containsKey   true iff some stored k has (key == k)
```

**Listing 1.** Documented key test. Field mutation cannot change `==` for that instance, and `identityHashCode` is the default identity hash even when `hashCode` is overridden.

```d2
direction: down
mutate: "Mutate fields on the\nsame instance you put" {
  width: 280
  height: 80
  style.fill: "#e3f2fd"
}
hm: "HashMap\nhashCode / equals changed\nget often misses" {
  width: 280
  height: 90
  style.fill: "#ffebee"
}
ihm: "IdentityHashMap\nstill key == stored k\nget hits" {
  width: 280
  height: 90
  style.fill: "#e8f5e9"
}

mutate -> hm
mutate -> ihm
```

**Fig. 1.** Same object, mutated state: value hashing can lose the key; identity hashing still finds it.

```java
import java.util.HashMap;
import java.util.IdentityHashMap;
import java.util.Map;

final class MutableId {
    int id;
    MutableId(int id) { this.id = id; }

    @Override
    public boolean equals(Object o) {
        if (!(o instanceof MutableId)) {
            return false;
        }
        return id == ((MutableId) o).id;
    }

    @Override
    public int hashCode() {
        return id;
    }
}

Map<MutableId, String> byValue = new HashMap<>();
Map<MutableId, String> byRef = new IdentityHashMap<>();
MutableId key = new MutableId(1);
byValue.put(key, "v");
byRef.put(key, "v");

key.id = 2; // changes equals/hashCode; reference unchanged

byValue.get(key);              // typically null — contract unspecified
byRef.get(key);                // "v" — still key == stored key
byRef.get(new MutableId(2));   // null — different reference
```

**Listing 2.** Conceptual: mutating `id` breaks `HashMap` lookup; `IdentityHashMap` still hits on the original instance and misses on a fresh equal copy. [[How does IdentityHashMap decide whether two keys are the same]] and [[Does IdentityHashMap use the hashCode method]] are the two halves of that rule.

`null` is a legal key here as well; there is no instance to mutate.

> [!warning] “Need not be immutable” is not “mutate freely”
> Identity still **is** the reference. `get(new MutableId(2))` misses even when `equals` would be true. Rebinding a variable to a new object is a different key, not a field update. If the same instance is also a `HashMap` key, mutating it still leaves that map unspecified. Immutability remains a good default for value maps; this class is the exception because it never consults `equals`/`hashCode` on the key.

> [!tip] Interview answer
> **No.** `IdentityHashMap` matches with `==` and hashes with `System.identityHashCode`, so the usual “keep `equals`/`hashCode` stable” rule does not apply to lookup. Mutating fields on the stored instance does not hide the entry. You still have to pass that same object; a new equal instance is a miss, and `HashMap` still requires stable keys.
