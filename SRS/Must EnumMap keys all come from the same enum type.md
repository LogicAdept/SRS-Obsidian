<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/EnumMap #Java/Language/Enum #SRS

# Must `EnumMap` keys all come from the same enum type?

> [!abstract] Short answer
> **Yes.** Every key in one `EnumMap` must be a constant of **one** enum class, chosen when the map is created (`new EnumMap<>(Color.class)` or inferred from a non-empty map). Mixing `Color` and `Size` is a compile-time error on a parameterized map, and a `ClassCastException` if you bypass generics. That single universe is why the map can be an array indexed by `ordinal()` ([[How does EnumMap store mappings internally]]).

## The type is fixed at construction

The class JavaDoc: all keys come from a single enum type specified **explicitly or implicitly** at creation.

- Explicit: `new EnumMap<Color, String>(Color.class)` — `keyType` is `Color.class`.
- From another `EnumMap`: same `keyType` as the source.
- From a plain `Map`: the key type is taken from a key already in that map, so the map **must contain at least one mapping** or construction throws `IllegalArgumentException`. An empty `HashMap` cannot tell the constructor which enum you meant.

`put` runs `typeCheck`: the key’s class must be `keyType`, or its superclass must be `keyType` (constant-specific class bodies are anonymous subclasses of the enum, still the same type). Otherwise `ClassCastException`. `get` / `containsKey` treat a wrong-type key as absent rather than throwing.

```d2
direction: down
ctor: "new EnumMap<>(Color.class)" {
  width: 280
  height: 55
  style.fill: "#e3f2fd"
}
ok: "Color.RED, Color.GREEN" {
  width: 260
  height: 50
  style.fill: "#e8f5e9"
}
bad: "Size.S\ncompile error / CCE" {
  width: 240
  height: 60
  style.fill: "#ffcdd2"
}

ctor -> ok
ctor -> bad
```

**Fig. 1.** One map, one enum class, one `vals[]` whose length is that type’s constant count.

```java
enum Color { RED, GREEN }
enum Size { S, M }

class Demo {
    void oneType() {
        java.util.EnumMap<Color, String> m =
                new java.util.EnumMap<>(Color.class);
        m.put(Color.RED, "r");
        // m.put(Size.S, "s"); // does not compile: Size is not Color

        java.util.EnumMap<Color, String> copy =
                new java.util.EnumMap<>(m); // Color, inferred
    }
}
```

**Listing 1.** Generics plus `Color.class` lock the universe. `EnumSet` has the same one-type rule ([[What is the difference between EnumMap and EnumSet]]).

```java
java.util.Map<Color, String> empty = java.util.Map.of();
// new java.util.EnumMap<>(empty); // IllegalArgumentException: specified map is empty
```

**Listing 2.** Conceptual: a non-`EnumMap` source must already contain a key so `keyType` can be inferred.

A `HashMap<Object, V>` or `HashMap<Enum<?>, V>` can hold `Color.RED` and `Size.S` together because it hashes whatever you pass. That is not a reason to do it, and it is exactly what `EnumMap` refuses ([[Why prefer EnumMap when the keys are enum constants]]).

> [!warning] Constant-specific bodies are still the same enum
> `PLUS { … }` has `getClass()` equal to an anonymous subclass. It is **not** a second key type. `typeCheck` allows `key.getClass().getSuperclass() == keyType` so those constants still `put`.

> [!warning] Raw types fail at `put`, not at “hash collision”
> Casting to a raw `EnumMap` and inserting another enum does not park the value in a mysterious bucket. `put` throws `ClassCastException` (`Size != Color`). `get` on a foreign key returns `null`.

> [!tip] Interview answer
> **Yes — one `EnumMap` is one enum type, fixed when you construct it.** That is how the value array can be indexed by `ordinal()`. `HashMap` can mix types because it does not care; `EnumMap` will not. Pass `TheEnum.class`, or copy a map that already has a key of that type.
