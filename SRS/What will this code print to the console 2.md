<!--
reps: 0
priority: 0
-->
#Java/Language/Wrappers/Autoboxing #Java/Language/Primitives #Career/Interview/Exercises #SRS

# What will this code print to the console 2?

> [!abstract] Short answer
> **Nothing — it does not compile.** `(Integer) t.intValue()` is a **cast of the call**, not a cast of `t`. `t` is `Object`, and `Object` has no `intValue`. Group the cast (`((Integer) t).intValue() / 10`) or unbox in the `/` (`(Integer) t / 10`). Then **`101 / 10` is integer division** and **`println` writes `10`**.

## The cast does not cover `t`

A cast is a **unary** operator. A method call is a **primary**. Without extra parentheses the operand of `(Integer)` is **`t.intValue()`**, so the compiler searches **`intValue` on `Object`** and stops. Parenthesizing the cast makes a primary, so `.intValue()` is searched on **`Integer`**, where it exists ([[How do you convert a wrapper to a primitive with xxxValue methods]]).

`/` is **looser** than the cast, so `(Integer) t / 10` already means `((Integer) t) / 10`. After the narrowing cast, `/` requires a primitive numeric operand, so the `Integer` is **unboxed** (`intValue()`) ([[What is unboxing]], [[What method does the compiler insert when unboxing an Integer]]). Integer division **rounds toward 0**, so `101 / 10` is `10`, not `10.1` ([[How does numeric promotion work in Java arithmetic expressions]]).

```d2
direction: down
broken: "(Integer) t.intValue()\ncast of the call" {
  width: 280
  height: 70
  style.fill: "#ffebee"
}
search: "search intValue on Object" {
  width: 260
  height: 50
  style.fill: "#fff8e1"
}
fail: "compile-time error\nno such method" {
  width: 240
  height: 60
  style.fill: "#ffebee"
}
fix: "((Integer) t).intValue()\nor (Integer) t / 10" {
  width: 280
  height: 70
  style.fill: "#e8f5e9"
}
ten: "unbox 101, then 101 / 10 → 10" {
  width: 280
  height: 50
  style.fill: "#e3f2fd"
}
broken -> search -> fail
fix -> ten
```

**Fig. 1.** The quiz line never reaches `/`. The grouped cast (or cast-then-divide) does, and prints `10`.

```java
public class ConsolePrint2Broken {
    public static void main(String[] args) {
        Object t = new Integer(101);           // deprecated; not the compile error
        int k = (Integer) t.intValue() / 10;   // does not compile
        System.out.println(k);
    }
}
```

**Listing 1.** Conceptual — this class is rejected. `intValue` is not a member of `Object`.

```java
public class ConsolePrint2 {
    public static void main(String[] args) {
        Object t = 101;                  // box int → Integer, then widen to Object
        int k = (Integer) t / 10;        // narrowing cast, unbox, integer divide
        System.out.println(k);           // 10
    }
}
```

**Listing 2.** One compiling repair. `Object t = 101` is assignment boxing plus a widening reference ([[When does autoboxing occur in Java]]). Same printed result: `int k = ((Integer) t).intValue() / 10` with `t` still an `Integer`.

The `new Integer(101)` line is legal with a **deprecation warning** (`since = "9"`, for removal). Autoboxing / `valueOf` is the supported factory ([[Why were Integer constructors deprecated]]). Swapping `new Integer` for `101` does **not** by itself make Listing 1 compile.

> [!warning] Extra parentheses, or it never runs
> Interview answers that jump to **`10`** are describing a **fixed** snippet. As written, there is **no console output**. `(Integer) t.intValue()` is **not** `((Integer) t).intValue()`.

> [!warning] A successful cast can still throw
> `(Integer) t / 10` is a **checked** narrowing cast, then unbox. A non-`Integer` runtime type is `ClassCastException` ([[When can a ClassCastException be thrown in Java]]). A `null` `Integer` is `NullPointerException` on `intValue()`.

> [!tip] Interview answer
> **It does not print — `Object` has no `intValue`, and the cast applies to the call, not to `t`.** Write `((Integer) t).intValue() / 10` or `(Integer) t / 10`. Then you unbox `101` and integer-divide by `10`, so the console shows `10`.
