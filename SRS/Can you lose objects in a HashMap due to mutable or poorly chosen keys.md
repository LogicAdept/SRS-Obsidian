<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/HashMap #Java/HashCodeEquals #Java/Immutability #Java/Language/Records #Java/Versions/8 #Java/Versions/16 #SRS

# Can you lose objects in a `HashMap` due to mutable or poorly chosen keys?

> [!abstract] Short answer
> **Yes, but the key and value do not disappear from memory.** If state used by a key's `equals` or `hashCode` changes after `put`, the mapping can become unreachable through ordinary key-based operations. `HashMap` retains the insertion-time hash in its node, while a later lookup computes a hash from the key's current state. The lookup usually selects another bin; even if it selects the same bin, the stored-hash check prevents a match. Iteration still sees the node.

## How the loss happens

`HashMap` stores, in each `Node`, the **spread hash computed at `put` time** together with a reference to the key object. A lookup computes a new spread hash from the key's **current** state and selects the bin using `hash & (n - 1)`. Within that bin, a node is eligible only when its stored hash equals the lookup hash and its key is identical or equal. See [[What is the internal structure of HashMap]].

```d2
direction: down
put: "put(k, v)\nhash1 = spread(k.hashCode())\nbucket1 = hash1 & (n-1)\nNode stored with hash1" {
  width: 320
  height: 110
  style.fill: "#e3f2fd"
}
mutate: "External code mutates k\nso k.hashCode() changes" {
  width: 300
  height: 90
  style.fill: "#fff3e0"
}
get: "get(k)\nhash2 = spread(k.hashCode())\nbucket2 = hash2 & (n-1)" {
  width: 320
  height: 100
  style.fill: "#e3f2fd"
}
other: "bucket2 != bucket1\noriginal node is not visited" {
  width: 290
  height: 80
  style.fill: "#ffebee"
}
same: "bucket2 == bucket1\nnode.hash1 != hash2\nstored-hash check fails" {
  width: 300
  height: 90
  style.fill: "#ffebee"
}
miss: "No key match\nget returns null" {
  width: 240
  height: 75
  style.fill: "#ffebee"
}
entry: "Original Node\nstill sits in its bin\nreachable via iteration" {
  width: 280
  height: 90
  style.fill: "#e8f5e9"
}
put -> mutate
mutate -> get
get -> other
get -> same
other -> miss
same -> miss
put -> entry: stores
```

**Fig. 1.** After key mutation, a lookup may inspect another bin. If both hashes happen to select the same bin, the stored hash still differs, so `HashMap` rejects the node before `equals`.

```java
class Key {
    int id;
    Key(int id) { this.id = id; }

    @Override
    public int hashCode() { return id; }

    @Override
    public boolean equals(Object o) {
        if (!(o instanceof Key)) return false;
        Key other = (Key) o;
        return other.id == id;
    }
}

Map<Key, String> map = new HashMap<>();
Key k = new Key(1);
map.put(k, "value");

k.id = 2;             // mutate field used by hashCode
map.get(k);           // null — lookup hash 2 does not match stored hash 1
map.get(new Key(1));  // null — bucket 1 holds a Node whose key.id is now 2
map.size();           // still 1
map.entrySet().iterator().hasNext(); // true — iteration still finds it
```

**Listing 1.** Mutating a key field after `put` makes the entry unreachable by key lookup, yet iteration still walks the table and finds the node.

> [!warning] Mutation breaks map-key assumptions
> A map's behavior is **not specified** if a stored key is mutated in a way that affects `equals` comparisons. Hash-based maps also rely on the `equals`/`hashCode` contract and on those results remaining stable while the key is stored. An unreachable mapping is therefore a consequence of violating the key requirements, not a `HashMap` defect.

## Other ways to lose or duplicate entries

### Broken `equals` / `hashCode` contract

If two keys are equal but produce different hash values, `HashMap` does not treat them as the same key: it checks the stored hash before calling `equals`. The hashes may select different bins; even if their bin indexes coincide, the stored-hash check still prevents a match. `put` can therefore create separate mappings for keys that `equals` considers equal. This violates the key contract, not the `HashMap` implementation — see [[How would you explain the equals and hashCode contract together in Java]].

```java
class Bad {
    final int id;
    final int hash;

    Bad(int id, int hash) {
        this.id = id;
        this.hash = hash;
    }

    @Override
    public boolean equals(Object o) {
        if (!(o instanceof Bad)) return false;
        Bad other = (Bad) o;
        return other.id == id;
    }

    @Override
    public int hashCode() { return hash; } // deliberately violates the contract
}

Map<Bad, String> m = new HashMap<>();
Bad first = new Bad(1, 10);
Bad second = new Bad(1, 20);

m.put(first, "a");
m.put(second, "b");
m.size();                 // 2, although first.equals(second) is true
m.get(new Bad(1, 30));    // null
```

**Listing 2.** Equal keys with deliberately different hashes become separate mappings because `HashMap` filters candidates by their stored hash before testing equality.

### Constant or skewed `hashCode`

A constant `hashCode` does not lose entries, but every key collides into one bin. In Java 8+, the bin starts as a linked list. Treeification is considered when an insertion encounters at least `TREEIFY_THRESHOLD = 8` existing nodes, but it requires a table capacity of at least `MIN_TREEIFY_CAPACITY = 64`; otherwise `HashMap` resizes first. List lookup is `O(n)`. A tree bin can provide `O(log n)` lookup when keys can be ordered, while some same-hash, non-comparable keys may still require a broader search. See [[When does a hashCode collision occur in a HashMap]].

## Recovery and prevention

While the key remains in its changed state, ordinary key lookup cannot recover the original mapping. Restoring the key's original equality and hash state may make it reachable again, but relying on that is fragile. Iteration can still find and remove the mapping:

```java
map.entrySet().removeIf(e -> e.getKey() == k);
```

**Listing 3.** Iterator-based cleanup walks the whole table, so it still sees the orphaned node.

> [!example] Use immutable keys
> Prefer keys whose equality and hash state cannot change: `String`, boxed primitives such as `Integer` and `Long`, or records composed only of primitives and immutable values. Records are only **shallowly immutable**: a final component can still reference a mutable `List`, array, or domain object whose changing state alters the record's generated `equals` and `hashCode`. Use immutable components or defensive copies.

```java
record Key(int id) {}
Map<Key, String> map = new HashMap<>();
map.put(new Key(1), "value");
map.get(new Key(1)); // works — hash and equals are stable
```

**Listing 4.** In Java 16+, this record is a stable key because its only component is a primitive `int`. `HashSet` uses elements as keys in an internal map, so [[How is HashSet implemented in terms of HashMap]] inherits the same stability requirement.

> [!tip] Interview answer
> **Yes, but the mapping is not deleted. `HashMap` stores the insertion-time hash and computes a fresh hash for lookup; after key mutation, the lookup may inspect another bin or fail the stored-hash check in the same bin, while iteration still sees the node. Use keys with stable `equals` and `hashCode` state; a record is safe only when its components are stable too. A broken `equals`/`hashCode` contract can create separate mappings for equal keys, whereas a constant hash primarily damages performance.**

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Что будет, если использовать как ключ изменяемый объект и потом его изменить?**

Объект «потеряется». hashCode станет другим, и при поиске мы попадём не в тот bucket.

**Можно ли использовать как ключ изменяемый объект (например, массив)?**

Технически можно, но опасно: если изменить объект после добавления — его hashCode может измениться, и найти элемент станет невозможно.
