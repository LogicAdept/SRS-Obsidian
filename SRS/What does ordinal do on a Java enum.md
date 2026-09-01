<!--
reps: 0
priority: 0
-->
#Java/Language/Enum #SRS

# What does `ordinal` do on a Java enum?

> [!abstract] Short answer
> **`ordinal()` is the constant’s zero-based position in the enum declaration.** The first name is `0`, the next `1`, and so on. The method is `final` on `java.lang.Enum`. It exists for structures such as `EnumMap` / `EnumSet`, not as a business key: insert or reorder a constant and every later number changes.

## Declaration position, not a stored id

The compiler creates each constant by calling `Enum(String name, int ordinal)` — programmers cannot invoke that constructor, and an enum constructor cannot write `super(...)` ([[Can you declare a constructor inside a Java enum]]). `ordinal()` just returns that `int`. `name()` is the identifier; `ordinal()` is the place in the list.

```d2
direction: down
src: "enum Size { S, M, L, XL }" {
  width: 280
  height: 50
  style.fill: "#e3f2fd"
}
ord: "S→0  M→1  L→2  XL→3" {
  width: 280
  height: 50
  style.fill: "#e8f5e9"
}
use: "EnumMap index, compareTo" {
  width: 260
  height: 50
  style.fill: "#fff3e0"
}

src -> ord -> use
```

**Fig. 1.** Ordinals are a layout of the source file. They are not a stable external protocol.

```java
enum Size { S, M, L, XL }

class Demo {
    int demo() {
        return Size.S.ordinal(); // 0
        // Size.M.ordinal() -> 1
        // Size.XL.ordinal() -> 3
    }
}
```

**Listing 1.** First declared constant is always `0` for that type. A different enum’s `0` is unrelated.

`compareTo` is `final` and uses this same declaration order ([[Can you override compareTo on a Java enum]], [[What is the difference between ordinal and compareTo on a Java enum]]). Adding or reordering constants is binary-compatible for callers, but it **renumbers** ordinals ([[Can you add constants to a Java enum at runtime]]).

`EnumMap` indexes `vals[key.ordinal()]` ([[How does EnumMap store mappings internally]]). `EnumSet` bit vectors use the same positions. That is the “sophisticated data structure” use the API calls out. Most application code should prefer the constant itself, `name()`, or an explicit field you control.

> [!warning] Do not persist `ordinal()` as a column or wire value
> Insert `Size.XS` at the top and yesterday’s `0` is no longer `S`. A named constant or a dedicated `int code` field on the constant survives reordering; `ordinal()` does not.

> [!warning] `switch (e.ordinal())` is the same trap
> `case 0` tracks source order, not the name. Switch on the enum value ([[Can you use a Java enum in a switch]]).

> [!tip] Interview answer
> **`ordinal()` returns the zero-based index of the constant in the enum declaration.** It is `final` on `Enum`, and `compareTo` uses that same order. Use it for `EnumMap`/`EnumSet`, not as a database id — reordering constants changes the numbers.
