<!--
reps: 0
priority: 0
-->
#Java/Language/Primitives #SRS

# Why must a local primitive variable be initialized before use in Java?

> [!abstract] Short answer
> Locals are **not** given a default. Fields and array **components** are: `0`, `0.0`, `false`, `'\u0000'`, or `null`. A local `int` (or `boolean`, `char`, …) must be **definitely assigned** on every path that reads it — initialization or assignment the compiler can prove. Otherwise it is a **compile-time error**. You never observe a “garbage `int`” or a silent `0`.

## Defaults for fields; proof for locals

Every variable must have a value before that value is used. Class variables, instance variables, and array components get a default when the object or array is created. Method and constructor **parameters** get the argument. A local declared by a statement does not: it must be given a value by its declarator or by assignment, checked with **definite assignment**. That analysis requires an assignment on **every** execution path to the read. It follows statement structure (`if`/`while`/`&&`/`||`/`?:`) and does not generally evaluate your arithmetic to decide “this branch is dead.” [[What default values do wrapper-typed fields receive in Java]] is the field/`null` side; [[Why cannot a Java primitive variable be null]] is why a local `int` is not “unset”; [[What is the difference between int and Integer in Java]] is primitive vs wrapper local.

```d2
direction: down
use: "read a variable" {
  width: 200
  height: 40
}
field: "field / array slot\ndefault 0, false, '\\0', null" {
  width: 300
  height: 70
  style.fill: "#e8f5e9"
}
local: "local (statement)\nmust be definitely assigned" {
  width: 300
  height: 70
  style.fill: "#fff8e1"
}
err: "some path has no assignment\n→ compile-time error" {
  width: 300
  height: 70
  style.fill: "#ffebee"
}

use -> field
use -> local
local -> err
```

**Fig. 1.** A field `int n;` is `0`. A local `int n;` cannot be read until every path assigns `n`.

`int[] a = new int[1];` is fine: the **local** `a` is assigned the array; `a[0]` is a component and defaults to `0`. `int n; if (cond) n = 1; System.out.println(n);` fails unless `cond` is a boolean constant the rules treat as always true. Pattern-declared locals (pattern matching) are initialized by matching and are not under this check. Blank `final` **fields** use the same definite-assignment idea; ordinary fields do not. A local `Integer` has the same “must assign” rule; assigning `null` then unboxing is a later NPE, not a missing initializer. [[What method does the compiler insert when unboxing an Integer]] is that NPE; [[What happens when a ternary operator unboxes a null Integer in Java]] is another null-unbox site.

```java
public final class LocalMustBeAssigned {
    int field;                 // 0

    public void show(boolean cond) {
        int localVariable = 100; // initializer — definitely assigned
        System.out.println(localVariable);
        System.out.println(field);

        int n;
        if (cond) {
            n = 1;
        } else {
            n = 2;
        }
        System.out.println(n);   // OK: both branches assign

        int missing;
        // System.out.println(missing); // compile-time error

        int[] slots = new int[1];
        System.out.println(slots[0]); // 0 — component default
    }
}
```

**Listing 1.** Locals need a proven assignment. The field and the array slot do not. An uninitialized local `int` does not compile as `0`.

> [!warning] “It might be 0” is the wrong mental model
> Reading `int x;` in a method is not undefined C behavior and not a default `0`. The compiler refuses the read. `if (flag) x = 1;` then using `x` still fails when `flag` is a runtime `boolean` — definite assignment is not your unit test. Do not “initialize to 0” unless `0` is a real domain value.

> [!tip] Interview answer
> Fields and array elements get language defaults; local variables do not. The compiler requires definite assignment: every path that reads a local must have written it. That is why `int x; System.out.println(x);` is a compile error, not a print of `0`.
