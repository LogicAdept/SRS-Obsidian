<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/HashMap #Java/Arrays #Java/HashCodeEquals #Java/Immutability #SRS

# Why are mutable keys such as `byte[]` risky in a `HashMap`?

> [!abstract] Short answer
> **The `Map` contract leaves behavior unspecified if you change a key so that `equals` comparisons change while it sits in the map.** `Object.hashCode` is allowed to change in exactly that case. `HashMap` then typically cannot find the node. Mutability is not the bug by itself: a raw `byte[]` uses identity `equals`, so rewriting cells does **not** trip that clause. The interview example is risky when `equals` / `hashCode` **read those cells** (`List`, `Date`, a wrapper around a live array). [[Can you lose objects in a HashMap due to mutable or poorly chosen keys]]

## The clause that makes mutation a key bug

`Map` (Java SE 21): great care if mutable objects are keys; behavior is **not specified** if the object is changed in a manner that affects `equals` comparisons while it is a key. A map must not contain itself as a key. `Object.equals` consistency and `Object.hashCode` stability are both qualified the same way: they hold **provided no information used in `equals` comparisons is modified**.

```d2
direction: down
key: "Key already in HashMap" {
  width: 260
  height: 60
  style.fill: "#e3f2fd"
}
q: "Does this mutation change\nequals / hashCode?" {
  width: 280
  height: 80
  style.fill: "#fff3e0"
}
yes: "Unspecified Map behavior\nlookup typically misses\niteration still sees the node" {
  width: 300
  height: 90
  style.fill: "#ffebee"
}
no: "Identity keys (Object, raw byte[])\nget(same reference) still hits" {
  width: 300
  height: 80
  style.fill: "#e8f5e9"
}
key -> q
q -> yes: yes
q -> no: no
```

**Fig. 1.** The risk is **equals-relevant** mutation, not “the object has setters.”

`List.equals` / `List.hashCode` are content-based (same size, same elements in order; hash `31 * hash + (e==null ? 0 : e.hashCode())`). `Date.equals` / `hashCode` use `getTime()`. `setTime` after `put` is the same class of bug. `Map.of` is unmodifiable as a map, yet the javadoc still warns that **mutable keys or values** can make even that map look inconsistent.

```java
List<Integer> listKey = new ArrayList<>(List.of(1, 2));
map.put(listKey, "v");
listKey.add(3);            // equals/hashCode now see [1, 2, 3]
map.get(listKey);          // unspecified; typically null
map.get(List.of(1, 2));    // typically null — stored key no longer equals that list
```

**Listing 1.** Conceptual `ArrayList` key. The mapping is not deleted; key-based `get` is what breaks. Mechanics: [[Can you lose objects in a HashMap due to mutable or poorly chosen keys]].

## Where `byte[]` fits

A `byte[]` is mutable in its **components**. It is **not** a content key. Array types inherit `Object.equals` / `Object.hashCode`, so assigning `a[i] = …` does not change equality or the identity hash. `map.get(a)` with the same reference still hits. That is why raw arrays are a **poor** key for “these bytes,” and a **Map-contract** risk only after you wrap them with `Arrays.equals` / `Arrays.hashCode` on the caller’s array. Clone, then hash the copy. [[Why is a byte array a poor or unsafe choice for a HashMap key]]

```java
byte[] a = { 1, 2 };
map.put(a, "v");
a[0] = 9;
map.get(a);                // still "v" — identity key
map.get(new byte[] { 1, 2 }); // null — never was content equality
```

**Listing 2.** Conceptual contrast with Listing 1. Same “mutate the array” story, different `equals`.

> [!warning] “Mutable, therefore lost”
> Identity keys can still be mutated; the map keeps finding **that instance** with a rewritten payload. Unspecified loss needs `equals` to see the change. `HashSet` elements are `HashMap` keys, so the same clause applies there.

> [!tip] Interview answer
> **`Map` does not specify what happens if you mutate a key’s `equals` state in place. `List` and `Date` do that; a raw `byte[]` does not, because it compares by identity. Content-hash a copy, or use an immutable key. The entry usually remains visible to iteration.**
