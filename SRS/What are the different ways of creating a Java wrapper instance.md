<!--
reps: 0
priority: 0
-->
#Java/Language/Primitives #Java/Language/Wrappers #SRS

# What are the different ways of creating a Java wrapper instance?

> [!abstract] Short answer
> Three practical paths: **autoboxing** (`Integer y = 10`), **`valueOf` factories** (`Integer.valueOf(10)`, `Integer.valueOf("10")`, `Integer.valueOf("111", 2)`), and the **deprecated constructors** (`new Integer(10)`, `new Integer("10")`). Prefer `valueOf` / boxing: they can reuse interned instances. `xxxValue()` methods go the **other** way (wrapper → primitive) and do not create wrappers.

## Three construction paths

Each numeric wrapper (and `Boolean` / `Character`) historically offered a constructor from its primitive and, except `Character`, from `String`. Since Java 9 those constructors are **deprecated for removal**. The replacements are the static factories, which boxing also uses ([[What method does the compiler insert when autoboxing an int]], [[Why were Integer constructors deprecated]]).

```d2
direction: down
src: "primitive or String" {
  width: 220
  height: 50
}
box: "autoboxing\nInteger y = 10" {
  width: 220
  height: 70
  style.fill: "#e8f5e9"
}
factory: "valueOf\nInteger.valueOf(...)" {
  width: 240
  height: 70
  style.fill: "#e3f2fd"
}
ctor: "new Integer(...)\ndeprecated" {
  width: 220
  height: 70
  style.fill: "#ffebee"
}
out: "wrapper instance" {
  width: 200
  height: 50
}
src -> box -> out
src -> factory -> out
src -> ctor -> out
```

**Fig. 1.** Boxing and `valueOf` are the supported ways to obtain a wrapper; `new` still compiles under deprecation.

```java
Integer boxed = 10;                          // autoboxing → valueOf(int)
Integer fromInt = Integer.valueOf(10);       // factory; cache in -128..127
Integer fromDec = Integer.valueOf("55");     // factory from decimal String
Integer fromBin = Integer.valueOf("111", 2); // radix 2 → 7

// Integer viaCtor = new Integer(55);        // deprecated since 9, for removal
// Integer viaStr  = new Integer("55");      // same; does not use the cache

int back = fromInt.intValue();               // wrapper → primitive, not creation
```

**Listing 1.** Conceptual: boxing, `valueOf`, and (avoided) constructors. `intValue` is the reverse conversion ([[How do you convert a wrapper to a primitive with xxxValue methods]]).

`Integer.valueOf(String, int)` is the wrapper counterpart of `parseInt` with a radix: it parses, then boxes. `parseInt` itself returns `int`, not `Integer`.

## Constructor shapes the dumps still quote

| Type | Primitive constructor | `String` constructor | Extra |
| --- | --- | --- | --- |
| `Integer` / `Long` / `Short` / `Byte` / `Double` | matching primitive | yes | — |
| `Float` | `float` **and** `double` | yes | `new Float(55.0)` vs `new Float(55.0f)` |
| `Character` | `char` only | **no** | `new Character(124)` does not compile |
| `Boolean` | `boolean` | yes (`"true"` ignore-case) | — |

`124` is an `int`. Constructor and `valueOf` arguments are **invocation** conversions, which do **not** narrow a constant `int` to `char`/`byte`/`short` ([[What are the autoboxing rules when assigning a primitive to a wrapper]]). Write `(char) 124`, or assign `Character c = 124;` where assignment *does* allow that narrowing then box.

`new Float(55.0)` selected the `double` constructor (`55.0` is `double`); `new Float(55.0f)` selected the `float` one. Both are deprecated; use `Float.valueOf`.

> [!warning] `new` bypasses the cache
> `new Integer(5)` is a distinct object every time. Boxing and `valueOf(int)` must reuse the **-128..127** instances (and `Boolean.TRUE` / `FALSE`). Interview `==` snippets that mix `new` with boxing are testing that difference, not value equality. Prefer `equals` / `intValue()`, and do not write `new` on wrappers.

> [!warning] Constructors are deprecated, not gone
> Java 9 marked them `@Deprecated(since = "9", forRemoval = true)`. They still exist in current JDKs (including 21) so old dumps compile with warnings. They are not a Java 17 removal. New code should use `valueOf` or autoboxing.

> [!tip] Interview answer
> **You create a wrapper by autoboxing, by `valueOf`, or — in old code — by `new`.** `valueOf` and boxing can return cached instances; `new` always allocates and is deprecated since 9. `Character` has no `String` constructor and will not take a bare `int` such as `124`. `xxxValue()` unwraps; it does not construct.
