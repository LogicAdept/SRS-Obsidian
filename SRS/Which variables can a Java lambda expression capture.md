<!--
reps: 0
priority: 0
-->
#Java/Lambdas #Java/Language/Modifiers/Final #SRS

# Which variables can a Java lambda expression capture?

> [!abstract] Short answer
> **Enclosing instance (and static) members freely; enclosing locals and parameters only if `final` or effectively final, and definitely assigned.** Effectively final means you could add `final` without a new error: no later assignment, `++`, or `--` on that variable. The **reference** is frozen, not the object: `p.age = 40` is legal; `p = …` is not. `this` in the body is the enclosing instance, not the lambda.

## Locals are captured; fields are `this`

A lambda may use names from the surrounding context. `this` / `super` mean the **enclosing** class, the same as outside the lambda ([[How would you explain lambda expressions in Java]]). Fields and methods of that instance (and of enclosing types, via `Outer.this`) are not “effectively final locals” — they are accessed through `this`. The tutorial’s `this.x` is the inner class field, not a captured local.

What **is** restricted: a local variable, method/constructor/lambda parameter, or exception parameter that the lambda **uses but does not declare**. That variable must be `final` or effectively final, and it must be definitely assigned before the lambda body. The point of the restriction is to avoid capturing a location whose value is still changing ([[How would you explain effectively final]]).

Effectively final (not declared `final`):

- With an initializer: never appears on the left of `=` and never as `++` / `--`.
- Without an initializer: assigned at most once, when definitely unassigned, and never `++` / `--`.
- A parameter is treated like a local that already has an initializer.

If you can add `final` and the program still compiles, it was effectively final. A `final` (or effectively final) **reference** always refers to the same object; the object’s fields and array components may still change.

```d2
direction: down
ok: "fields via this\nstatic members" {
  width: 240
  height: 50
  style.fill: "#e8f5e9"
}
local: "enclosing local / param" {
  width: 240
  height: 45
  style.fill: "#fff3e0"
}
ef: "final or effectively final\nand definitely assigned" {
  width: 280
  height: 50
  style.fill: "#e3f2fd"
}
bad: "later = or ++ on the variable" {
  width: 260
  height: 45
  style.fill: "#fce4ec"
}
ok -> local: "also"
local -> ef: "required"
local -> bad: "compile error"
```

**Fig. 1.** Capture is the local/parameter rule. Mutating `p.age` through a frozen `p` is allowed ([[What does this code snippet print to the console 2]]). Enhanced-`for` vs counted `for`: the loop variable `s` is a **new** variable each iteration (legal); `i++` in a classic `for` is not effectively final.

Lambda parameters sit in the **same** scoping level as the enclosing method. `(x) ->` cannot redeclare an enclosing local `x`. Unlike an inner class, a lambda does not open a nested scope that can shadow those names.

```java
import java.util.function.IntSupplier;
import java.util.function.Supplier;

class Demo {
    int field = 1;

    void m(int x) {
        int y = 1;
        IntSupplier s = () -> x + y + this.field; // x, y effectively final
        this.field = 9; // field write is fine
        // y = 2; // then () -> x + y would not compile
        // IntSupplier bad = () -> { y = 3; return y; };

        String[] arr = { "a", "b" };
        for (String elt : arr) {
            Supplier<String> each = () -> elt; // legal: distinct elt each trip
        }
        for (int i = 0; i < arr.length; i++) {
            // Supplier<String> no = () -> arr[i]; // i is not effectively final
        }
    }
}
```

**Listing 1.** Same facts as the spec’s `m1` / `m5` / `m9` / `m10` examples. `y = 2` after the lambda, or `y = 3` inside it, both destroy effective-finality. Related wording: [[Which variables can lambda expressions access in Java]].

> [!warning] Assignment inside the lambda counts
> `z = 99` in the body makes `z` not effectively final, even if that assignment is the only write. The compiler error is “must be final or effectively final.” Mutating fields of the object `z` refers to, or an array component `z[0]`, is not an assignment to `z`.

> [!warning] Definitely assigned before the body
> `int y; foo(() -> x + y);` is illegal even if some `if` assigned `y` — `y` must be definitely assigned **before** the lambda. A blank local that is assigned on every path, then captured, is fine (`if (…) y = 1; else y = 2;`).

> [!tip] Interview answer
> **A lambda can use enclosing fields through `this`, and can capture enclosing locals and parameters only when they are `final` or effectively final and already assigned.** Effectively final means the variable is never reassigned or incremented. The captured binding is the variable, not a snapshot of object state — you may mutate the object, not retarget the variable.
