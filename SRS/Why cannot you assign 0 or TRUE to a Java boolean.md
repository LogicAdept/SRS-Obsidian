<!--
reps: 0
priority: 0
-->
#Java/Language/Primitives #Java/Language/Wrappers #SRS

# Why cannot you assign `0` or `TRUE` to a Java `boolean`?

> [!abstract] Short answer
> **`boolean` literals are only `true` and `false`.** `0` is an `int`; there is no integer-to-`boolean` conversion, so `boolean b = 0;` does not compile. `TRUE` is not a literal or a keyword — it is an identifier. `Boolean.TRUE` is a wrapper constant and **does** assign via unboxing.

## Two literals, no C conversions

The `boolean` type has two values, written with the ASCII literals `true` and `false`. Those tokens are **literals**, not keywords. `TRUE` / `FALSE` / `0` / `1` are not on that list. [[What are Boolean.TRUE and Boolean.FALSE]] are `Boolean` objects, not primitive literals.

Assignment to `boolean` allows identity, boxing to `Boolean`, or unboxing from `Boolean`. It does not allow a widening or narrowing conversion from `int`. Casting does not help: there is no conversion between `boolean` and the numeric types. `boolean b = 1;` fails the same way as `= 0`. The C spelling is an expression: `x != 0` ([[Why cannot Java logical operators be applied to integers]]).

`TRUE` with no qualifier is a compile-time error unless some `TRUE` is in scope (a variable, or a static import of `Boolean.TRUE`). The wrapper field is `public static final Boolean TRUE` — the object for primitive `true`. `boolean b = Boolean.TRUE;` compiles because assignment unboxes. `boolean b = null;` does not: `null` is not a primitive value ([[Why cannot a Java primitive variable be null]]).

```d2
direction: down
src: "boolean b =" {
  width: 160
  height: 50
  style.fill: "#fff3e0"
}
ok: "true / false\nor Boolean.TRUE" {
  width: 220
  height: 70
  style.fill: "#e8f5e9"
}
bad: "0, 1, TRUE\ncompile error" {
  width: 200
  height: 70
  style.fill: "#ffebee"
}

src -> ok
src -> bad
```

**Fig. 1.** Primitive assignment accepts `true`/`false` (and unboxing). It does not accept `int` or a bare `TRUE`.

```java
public final class BooleanNotC {
    public static void main(String[] args) {
        boolean yes = true;
        boolean no = false;
        boolean fromWrapper = Boolean.TRUE; // unbox

        // boolean zero = 0;              // compile error: int → boolean
        // boolean one = 1;               // compile error
        // boolean shout = TRUE;          // compile error: not a literal
        // boolean n = null;              // compile error

        System.out.println(yes);
        System.out.println(no);
        System.out.println(fromWrapper);
        System.out.println(Boolean.FALSE.booleanValue());
    }
}
```

**Listing 1.** `true`/`false` are the literals. `Boolean.TRUE` unboxes. `0` and a bare `TRUE` do not compile.

> [!warning] `TRUE` is not `true`, and `Boolean.TRUE` is not a `boolean` literal
> Case matters. `TRUE` is an ordinary identifier. After `import static java.lang.Boolean.TRUE;`, `boolean b = TRUE;` suddenly compiles — that is unboxing the wrapper, not a new primitive literal. `if (0)` and `boolean flag = 1;` stay illegal.

> [!tip] Interview answer
> **Only `true` and `false` are `boolean` literals.** `0` and `1` are `int`s; Java has no C-style conversion to `boolean`. `TRUE` is not a keyword — use `true`, or `Boolean.TRUE` if you mean the wrapper (that unboxes). `boolean b = 0;` and `boolean b = TRUE;` do not compile.
