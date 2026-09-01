<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/TreeMap #Java/Collections/Map/HashMap #Java/Collections/Sorting #Java/Language/Enum #SRS

# What types can you use as `TreeMap` keys?

> [!abstract] Short answer
> Types the map can **compare**. Natural-order maps (`new TreeMap<>()`): every key must implement **`Comparable`**, and `k1.compareTo(k2)` must not throw. With a constructor **`Comparator`**, keys need only be mutually comparable by that comparator. Usual keys: `String`, wrappers (`Integer`, `Double`, `Character`, …), enums. `null` only if the comparator allows it.

## Mutually comparable, not “anything `Object`”

The no-arg and `TreeMap(Map)` constructors document the rule: keys **must implement `Comparable`**, and all pairs must be mutually comparable. The official counterexample is putting a **string** into a map whose keys are **integers** — `put` throws `ClassCastException`. A `Comparator` constructor replaces `compareTo` with `compare`; the same CCE rule applies to that `compare` ([[How do you customize TreeMap key order]]).

That is why dumps say keys must be **orderable** and **homogeneous**. `HashMap` does not sort: `get` matches with `equals`, so unrelated types can sit in one hash map. A `TreeMap<Object, V>` still blows up at `put` when two keys cannot be compared — generics do not save you.

`Integer`, `String`, `Double`, and `Character` all implement `Comparable` (`compareTo`). `Enum` implements `Comparable`; `compareTo` orders constants of the **same** enum type by declaration order. `Enum`’s class comment also points at specialized maps for enum keys ([[Can you use a Java enum with TreeSet or TreeMap]]).

Custom types: implement `Comparable` (a `Person` ordered by `id` is the usual sketch) **or** pass a `Comparator` and skip `Comparable` on the class. The ordering should be consistent with `equals` ([[Why must TreeMap ordering be consistent with equals]]). Do not mutate comparison fields after `put` ([[What happens if you mutate a TreeMap key after insertion]]).

```d2
direction: down
key: "candidate key type" {
  width: 220
  height: 50
  style.fill: "#e3f2fd"
}
nat: "natural-order TreeMap\nComparable + mutually comparable" {
  width: 300
  height: 70
  style.fill: "#e8f5e9"
}
cmp: "TreeMap(comparator)\ncompare must not CCE" {
  width: 280
  height: 70
  style.fill: "#fff3e0"
}
key -> nat
key -> cmp
```

**Fig. 1.** Two legal routes. Mixing a `String` with `Integer` keys is the documented `ClassCastException`. Null keys: [[Can TreeMap have null keys or null values]].

```java
import java.util.Comparator;
import java.util.TreeMap;

class Demo {
    record Person(int id, String name) implements Comparable<Person> {
        public int compareTo(Person o) { return Integer.compare(id, o.id); }
    }

    static void naturalAndComparator() {
        var byNatural = new TreeMap<Integer, String>();
        byNatural.put(2, "b");
        byNatural.put(1, "a");

        var byName = new TreeMap<Person, String>(
                Comparator.comparing(Person::name));
        byName.put(new Person(1, "Ann"), "x");
    }

    static void mixedTypesThrow() {
        var m = new TreeMap<Object, String>();
        m.put(1, "int");
        m.put("one", "str"); // ClassCastException — Integer vs String
    }
}
```

**Listing 1.** Wrappers work via `Comparable`. `Person` uses natural order on `id`, or a name `Comparator`. The `Object` map is legal Java and still throws at the second `put`.

> [!warning] `ClassCastException` is a `put`-time check
> The map does not “sort hashing.” It compares the new key with keys already in the tree. Incomparable types fail then, not at construction. Raw / `Object` keys hide this from the compiler.

> [!warning] Enum keys: `TreeMap` works, `EnumMap` exists
> Enums are `Comparable`, so `TreeMap<MyEnum, V>` is legal. The `Enum` specification still points you at specialized enum maps/sets when the key (or element) type is one enum class.

> [!tip] Interview answer
> **Natural-order `TreeMap` keys must be `Comparable` and mutually comparable — `String`, wrappers, enums. Otherwise pass a `Comparator`. Mixing a `String` and an `Integer` is the textbook `ClassCastException`. `HashMap` can mix types because it uses `equals`, not sort. Null keys need a null-friendly comparator.**
