<!--
reps: 0
priority: 0
-->
#Java/Language/Primitives #Java/Language/Wrappers #SRS

# Why does `Character` reject an `int` constructor argument?

> [!abstract] Short answer
> `Character` has **only a `char` constructor** (deprecated). `124` is an **`int`**. Constructor arguments use **invocation** conversion, which **does not** narrow a constant `int` to `char`. So `new Character(124)` does not compile, even though `124` fits in a `char`. Write `'C'`, `(char) 124`, or assign `Character c = 124` (assignment *does* allow that narrowing then box). Prefer `Character.valueOf`.

## No `Character(int)`, and no implicit narrow on `new`

`Integer` has `Integer(int)`. `Character` never did: it wraps a 16-bit `char`, and the only constructor is `Character(char)` ([[What are the different ways of creating a Java wrapper instance]]).

`124` without a suffix or cast has type `int`. Turning `int` into `char` is a **narrowing** primitive conversion. Assignment of a **constant** that fits (`char c = 124`, `Character boxed = 124`) is allowed. **Invocation** (constructors and methods, including `valueOf(char)`) is not ([[What are the autoboxing rules when assigning a primitive to a wrapper]]).

```d2
direction: down
lit: "124 is int" {
  width: 160
  height: 40
}
newc: "new Character(124)\ninvocation — error" {
  width: 260
  height: 70
  style.fill: "#ffebee"
}
assign: "Character c = 124\nassignment — OK" {
  width: 260
  height: 70
  style.fill: "#e8f5e9"
}
cast: "(char) 124 then construct" {
  width: 260
  height: 50
  style.fill: "#e3f2fd"
}
lit -> newc
lit -> assign
lit -> cast
```

**Fig. 1.** Same literal; the conversion *context* decides whether narrowing happens.

```java
Character c1 = new Character('C');     // char argument — legal, deprecated
// Character c2 = new Character(124);  // compile error: int ↛ char here
Character c3 = new Character((char) 124);
Character c4 = 124;                    // assignment: constant fits → narrow + box
Character c5 = Character.valueOf((char) 124);
// Character c6 = Character.valueOf(124); // same invocation error
```

**Listing 1.** Conceptual: quotes, cast, or assignment boxing — not a bare `int` to `new`.

`124` is well inside `'\u0000'`..`'\uFFFF'`. The failure is **not** overflow. `Byte` / `Short` constructors show the same trap: `new Byte(1)` is an `int` argument to `Byte(byte)`.

The constructor is deprecated for removal since 9; autoboxing/`valueOf` is the supported path ([[What method does the compiler insert when autoboxing an int]]). `valueOf` still takes `char`, so the cast (or a `char` variable) remains.

> [!warning] `Character c = 124` is not the same as `new Character(124)`
> Interviewers mix the two. Assignment boxing may narrow a constant `int` into `Character`. `new` is a constructor call and will not. Answering “124 is too big for `char`” is wrong.

> [!tip] Interview answer
> **`Character` only constructs from `char`, and `new` will not silently narrow an `int` literal.** Use `'C'`, a cast, or assignment `Character c = 124`. Prefer `valueOf`. The number fits; the conversion context does not allow it.
