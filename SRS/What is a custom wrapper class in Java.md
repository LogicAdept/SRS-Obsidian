<!--
reps: 0
priority: 0
-->
#Java/Language/Primitives #Java/Language/Wrappers #SRS

# What is a custom wrapper class in Java?

> [!abstract] Short answer
> A **custom wrapper** is just **your** class that holds a value (often a primitive) behind a field. It is **not** one of the eight `java.lang` wrappers (`Integer`, `Boolean`, …). The compiler will **not** autobox an `int` into it, and `ArrayList<MyInt>` will not accept a bare `int`. Mutability is yours to choose — the dump’s `setValue` type is mutable; `Integer` is not.

## Language wrappers vs a class you wrote

Boxing conversion is a **closed list**: `boolean`↔`Boolean`, `byte`↔`Byte`, `short`↔`Short`, `char`↔`Character`, `int`↔`Integer`, `long`↔`Long`, `float`↔`Float`, `double`↔`Double`. Anything else is an ordinary reference type ([[What are the wrapper types for Java primitives]], [[When does autoboxing occur in Java]]).

A custom wrapper is that ordinary class: a private field, a constructor, accessors, maybe `equals` / `hashCode` / `toString`. Useful as a teaching sketch of “object that carries an `int`,” or as a real domain type (`Money`, `Celsius`). It does not join the language’s boxing table.

```d2
direction: down
prim: "int 55" {
  width: 120
  height: 40
}
lang: "Integer.valueOf(55)\nlanguage wrapper" {
  width: 240
  height: 70
  style.fill: "#e8f5e9"
}
mine: "new MyInt(55)\ncustom class" {
  width: 220
  height: 70
  style.fill: "#e3f2fd"
}
prim -> lang
prim -> mine
```

**Fig. 1.** Same payload; only `Integer` is what autoboxing and `List<Integer>` know.

```java
final class MyInt {
    private int value;                       // not final — dump-style mutable holder
    MyInt(int value) { this.value = value; }
    int getValue() { return value; }
    void setValue(int value) { this.value = value; }
    @Override public String toString() { return Integer.toString(value); }
}

MyInt wrapped = new MyInt(55);
wrapped.setValue(56);
// MyInt boxed = 55;                         // does not compile: no autoboxing to MyInt
// List<MyInt> list = new ArrayList<>();
// list.add(55);                             // does not compile either
```

**Listing 1.** Conceptual: a user wrapper you construct yourself. Contrast `Integer y = 55;`.

Because `MyInt` is mutable, `void bump(MyInt n) { n.setValue(n.getValue() + 1); }` **does** change the caller’s object. `void bump(Integer n) { n++; }` does **not** — `++` rebinds the local reference, and `Integer` has no setter ([[Are Java wrapper types immutable]], [[Can wrapping a primitive let a Java method change the caller value]]).

`toString` that delegates to `Integer.toString` is only formatting. It does not make `MyInt` an `Integer`, a `Number`, or a cached value-based type.

> [!warning] Collections still want the language wrappers
> `List<Integer>` is why `Integer` exists in APIs. Putting a primitive in a collection autoboxes to **those** eight types, not to `MyInt`. If you want `List<MyInt>`, you wrap explicitly. Do not expect `IntegerCache`, `valueOf`, or `==` identity rules to apply.

> [!tip] Interview answer
> **A custom wrapper is a class you write that holds a primitive or another object — not `Integer` and friends.** There is no autoboxing into it. If you add a setter it is mutable, unlike `Integer`. Use the `java.lang` wrappers when the point is collections or APIs; use a custom type when the point is your domain.
