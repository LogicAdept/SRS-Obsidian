<!--
reps: 0
priority: 0
-->
#Java/Language/Primitives #Java/Language/Wrappers #SRS

# What default values do wrapper-typed fields receive in Java?

> [!abstract] Short answer
> A field whose type is a wrapper — `Integer`, `Double`, `Boolean`, `Character`, and the rest — is a **reference**, so it defaults to **`null`**. Numeric wrappers do **not** default to `0`, and `Boolean` does **not** default to `false`. Those zeros and `false` / `'\u0000'` are the defaults for the **primitive** field types `int`, `boolean`, `char`, and so on.

## Fields get a type’s default; wrappers are references

Every class variable, instance variable, and array component is initialized to a default when the field or array is created. For **all reference types** that default is `null`. Wrapper classes are ordinary reference types, so an uninitialized `Integer n;` field is `null`, not `Integer.valueOf(0)`.

Primitive fields are different ([[What default values do Java fields receive when not explicitly initialized]], [[Why cannot a Java primitive variable be null]]):

| Field type | Default |
| --- | --- |
| `byte` / `short` / `int` | `0` |
| `long` | `0L` |
| `float` / `double` | `+0.0` (`0.0f` / `0.0d`) |
| `char` | `'\u0000'` |
| `boolean` | `false` |
| any wrapper (`Integer`, `Boolean`, …) | **`null`** |

```d2
direction: down
prim: "int count\ndefault 0" {
  width: 200
  height: 70
  style.fill: "#e8f5e9"
}
wrap: "Integer count\ndefault null" {
  width: 200
  height: 70
  style.fill: "#ffebee"
}
```

**Fig. 1.** Same “count” idea: primitive field is zero; wrapper field is a null reference.

```java
class Counters {
    int primitive;          // 0
    Integer boxed;          // null — not 0
    boolean flag;           // false
    Boolean boxedFlag;      // null — not false
    int[] ints;             // null (the array reference)
    Integer[] integers;     // null (the array reference)
}

Counters c = new Counters();
// c.boxed.intValue();      // NullPointerException
int exploded = c.boxed;     // unboxing null → NullPointerException
```

**Listing 1.** Conceptual: wrapper fields start as `null`; using them as primitives unboxes and throws.

`Integer[] integers = new Integer[3];` is a created array whose **components** are also `null` (three null references). That is not an `int[3]` of zeros.

## Locals are not fields

A **local** `Integer x;` has no default. The compiler demands definite assignment before use, the same as a local `int`. Do not answer this question with “locals are null” — only fields, statics, and array components get defaults ([[Why must a local primitive variable be initialized before use in Java]]).

> [!warning] Unboxing a default wrapper is an NPE
> `Integer n;` as a field looks harmless. `int x = n;` or `n + 1` inserts `intValue()` on `null` and throws `NullPointerException`. That is why dumps that list **`0` for `Integer` fields** are describing **`int`**, not the wrapper ([[Why are Integer and Boolean wrapper types dangerous in Java]], [[How do you convert a wrapper to a primitive with xxxValue methods]]).

> [!tip] Interview answer
> **Wrapper-typed fields default to `null` because they are references.** Primitive fields default to `0`, `0.0`, `false`, or `'\u0000'`. Saying `Integer` defaults to `0` mixes those two tables. Unboxing that `null` is a `NullPointerException`; a local wrapper has no default at all.
