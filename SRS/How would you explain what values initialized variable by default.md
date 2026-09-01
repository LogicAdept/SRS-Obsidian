<!--
reps: 0
priority: 0
-->
#Java/Language/Primitives #SRS

# How would you explain what values a variable is initialized with by default?

> [!abstract] Short answer
> **Only fields and array components get defaults.** Numerics become zero (`0`, `0L`, `(byte)0`, …; `float`/`double` **positive** `0.0`), `char` is `'\u0000'`, `boolean` is `false`, references (`String` included) are `null`. Locals have **no** default: using them without an assignment is a compile-time error.

## Who gets a default, and what it is

Every variable must have a value before it is used. That does **not** mean every variable is zeroed.

**Class variables, instance variables, and array components** are given a default when they are created (class prepared, object allocated, array allocated) ([[What default values do Java fields receive when not explicitly initialized]]):

| Type | Default |
| --- | --- |
| `byte` | `(byte)0` |
| `short` | `(short)0` |
| `int` | `0` |
| `long` | `0L` |
| `float` | `0.0f` (positive zero) |
| `double` | `0.0d` (positive zero) |
| `char` | `'\u0000'` |
| `boolean` | `false` |
| any reference | `null` |

Wrapper fields are references, so they default to `null`, not `0` ([[What default values do wrapper-typed fields receive in Java]]).

**Parameters** (method, constructor, exception, lambda) are initialized from the argument or the thrown object — not from that table.

**Local variables** declared by a statement must be definitely assigned before use ([[Why must a local primitive variable be initialized before use in Java]]). There is no hidden `0`. A pattern variable is initialized by a successful match.

```d2
direction: down
v: "variable" {
  width: 140
  height: 40
  style.fill: "#fff3e0"
}
created: "field / array component\ncreated → default" {
  width: 280
  height: 70
  style.fill: "#e8f5e9"
}
local: "local from a statement\nmust assign before use" {
  width: 280
  height: 70
  style.fill: "#ffebee"
}
arg: "parameter\n← argument" {
  width: 220
  height: 55
  style.fill: "#e3f2fd"
}

v -> created
v -> local
v -> arg
```

**Fig. 1.** Defaults apply when the variable is created as part of a class, object, or array — not to ordinary locals.

```java
class Point {
    static int npoints;   // 0 when the class is prepared
    int x, y;             // 0 per instance
    Point root;           // null per instance
}

public final class DefaultInit {
    public static void main(String[] args) {
        System.out.println(Point.npoints); // 0
        Point p = new Point();
        System.out.println(p.x);           // 0
        System.out.println(p.root);        // null

        boolean[] flags = new boolean[1];
        System.out.println(flags[0]);      // false

        // int local;
        // System.out.println(local);      // compile error: not definitely assigned
    }
}
```

**Listing 1.** Static/instance/array slots get defaults. A bare local `int` does not.

> [!warning] “Variables default to zero” is false for locals, and `0.0` is not every numeric
> `int n; System.out.println(n);` does not compile. `Integer boxed;` as a field is `null`; unboxing it NPEs. `float`/`double` default to **positive** zero, written `0.0f` / `0.0d`, not an integer `0`. `char` is the null character, which prints as nothing, not the character `'0'`.

> [!tip] Interview answer
> **Fields and array elements get language defaults: numeric zero, `'\u0000'`, `false`, or `null`.** Locals do not — the compiler demands a definite assignment. Parameters take the argument, not that table. Wrapper fields are `null`, not `0`.
