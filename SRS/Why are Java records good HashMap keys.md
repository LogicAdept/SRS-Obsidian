<!--
reps: 0
priority: 0
-->
#Java/Language/Records #Java/Collections/Map/HashMap #Java/HashCodeEquals #Java/Immutability #SRS

# Why are Java records good HashMap keys?

> [!abstract] Short answer
> Because the compiler already supplies **value-based `equals` and `hashCode` over every component**, and those component fields are **`private final`**. Two `new Point(0, 0)` instances are the same map key without a hand-written pair. That is the same reason [[Why is String a common choice for HashMap keys]] — stable content equality. It is **shallow**: a mutable component (`List`, array) mutated after `put` still breaks the `Map` contract.

## Value equality without writing the pair

```d2
direction: down
need: "HashMap key needs\nstable equals + hashCode" {
  width: 280
  height: 70
  style.fill: "#e3f2fd"
}
rec: "record Point(int x, int y)\nfinal fields, derived pair" {
  width: 280
  height: 70
  style.fill: "#e8f5e9"
}
ok: "put(new Point(0,0))\nget(new Point(0,0))" {
  width: 260
  height: 70
  style.fill: "#e8f5e9"
}
need -> rec
rec -> ok
```

**Fig. 1.** `Map` lookup is `key.equals(k)` after `hashCode` picks a bin. A record’s implicit pair is defined on the component **fields** ([[What methods does the compiler generate for a Java record]]), so a second instance with the same header looks up the first.

`java.util.Map`: great care if a key is mutated in a way that changes `equals` while it sits in the map. A record cannot rebind component fields or grow a hidden instance field ([[Are Java record fields final]]). Implicit `equals` is null-safe on references (both null → equal) and uses wrapper `compare` for primitives — not a dump-specific `Objects.hash` / `31 * h` formula. `java.lang.Record` leaves the **mix** of component hashes unspecified.

```java
record Point(int x, int y) {}

Map<Point, String> labels = new HashMap<>();
labels.put(new Point(0, 0), "origin");
labels.get(new Point(0, 0)); // "origin"
```

**Listing 1.** Distinct instances, same components, same key — like `new String("id")`.

```java
record Box(List<Integer> values) {}
List<Integer> list = new ArrayList<>(List.of(1, 2));
Box key = new Box(list);
map.put(key, "a");
list.add(3);           // equals/hashCode of the key changed
map.get(key);          // unspecified — often null / lost
```

**Listing 2.** Shallow immutability. Same failure mode as [[Why are mutable keys such as byte arrays risky in a HashMap]]. Prefer `List.copyOf` in a compact constructor, or do not use a mutable type as a component of a map key.

Array components use **`Object.equals` / `Object.hashCode`** (identity). Two `record R(int[] a)` values with `new int[]{1, 2}` vs `new int[]{1, 2}` do **not** match. If you need content equality, declare `equals` / `hashCode` with `Arrays.equals` / `Arrays.hashCode` and keep both in step ([[Why should equals and hashCode be overridden together]]). You cannot cache `hashCode` in an extra instance field.

> [!warning] Mutable components still lose entries
> Records are good keys when the components are primitives, `String`, or other immutable records. `List`, arrays, and JavaBeans inside the header are the same hazard as a mutable class key ([[What requirements apply to keys used in a HashMap]]).

> [!warning] Do not quote a `hashCode` formula
> Dumps that pick `Objects.hash` versus a `31`-multiply chain are describing a compiler, not the language. Equal records must share a hash; the mixing is unspecified and is not stored in an instance field.

> [!tip] Interview answer
> **Records make good `HashMap` keys because `equals` and `hashCode` are generated from all `final` components, so a new instance with the same values finds the same entry.** That holds only while those components stay immutable. Arrays compare by reference; mutating a `List` component after `put` is the usual lost-key bug.
