<!--
reps: 0
priority: 0
-->
#Java/Lambdas #Java/Versions/8 #Java/MethodReferences #SRS

# What is method reference

> [!abstract] Short answer
> **A method reference is `TypeOrExpr::name` (or `::new`) — a poly expression that becomes a functional-interface instance without calling the method yet.** Same deferred idea as a lambda. The dump’s three bullets miss the common fourth form: **`String::length` is an unbound instance method** (the first SAM argument is the receiver), not a static method. Overload resolution uses the target FI, not a signature you write next to `::`.

## `::` names a call, then the SAM runs it

A method reference refers to invoking a method (or constructing an object/array) **without performing that invocation**. Evaluating it produces a functional-interface instance; the referenced method runs later, when the SAM is invoked ([[How would you explain lambda expressions in Java]], [[What is functional interface]], [[What kinds of method references exist in Java]]).

It is a poly expression: assignment, invocation, or cast context only. You cannot write `Arrays::sort(int[])` to pick an overload — the FI’s function type feeds overload resolution. If that is too loose, use a lambda.

Forms the language actually has:

| Form | Example | When the SAM runs |
| --- | --- | --- |
| Static | `System::currentTimeMillis` | no receiver |
| Bound instance | `System.out::println` | receiver is the Primary, evaluated **now** |
| Unbound instance | `String::length` | first SAM argument is the receiver |
| Constructor / array | `ArrayList::new`, `int[]::new` | deferred `new` |
| `super` | `super::toString` | enclosing instance |

The dump example is legal: `Measurable a = String::length;` then `a.length("abc")` is `3`. The SAM name (`length`) need not match a static method; `String.length()` is an **instance** method. `s -> s.length()` is the equivalent lambda ([[What does the System.out println method reference mean]]).

A bound Primary is evaluated when the reference is created. If it is `null`, that evaluation throws `NullPointerException` immediately — not later at `accept`. Static methods cannot be referenced with a Primary qualifier.

“Always prefer a reference, it is more efficient” is **style**, not a guarantee. Implementations may allocate or reuse instances the same way they do for lambdas. Prefer `::` when it is an existing method with no extra logic; keep a lambda when you need a capture, a cast, or an overload the FI cannot pick ([[How would you explain Java method references and their bytecode form]]).

```d2
direction: down
syn: "ReceiverOrType :: name" {
  width: 260
  height: 45
  style.fill: "#fff8e1"
}
fi: "functional interface instance" {
  width: 260
  height: 45
  style.fill: "#e8f5e9"
}
run: "SAM invoke → real method / new" {
  width: 280
  height: 45
  style.fill: "#e3f2fd"
}

syn -> fi: "evaluate :: (not the method)"
fi -> run: "deferred"
```

**Fig. 1.** Same deferred story as a lambda. Bound receivers (`System.out`) are resolved at `::`, unbound receivers (`String::length`) at the SAM call.

```java
interface Measurable {
    int length(String string);
}

class Demo {
    static void refs() {
        Measurable a = String::length;
        a.length("abc"); // 3
        java.util.function.Consumer<String> p = System.out::println;
        p.accept("abc");
        java.util.function.Supplier<java.util.ArrayList<String>> s = java.util.ArrayList::new;
        // Arrays::sort(int[])  // not legal syntax
    }
}
```

**Listing 1.** Dump `String::length` is unbound instance, not static. `System.out::println` evaluates `out` at `::`. `::new` is a constructor reference.

> [!warning] `String::length` is not a static reference
> The dump’s first bullet (`Class::staticMethod`) does not describe that example. Unbound instance: SAM is `int apply(String)` / `int length(String)` and the string is `this`. Mixing that up with `Integer::parseInt` (truly static) is the usual interview miss.

> [!warning] The qualifier is not always lazy
> `obj::foo` NPEs if `obj` is null **when the reference is created**. `Type::foo` does not evaluate an instance yet. You cannot pin an overload in the `::` token; use a lambda if the FI is ambiguous.

> [!tip] Interview answer
> **Method reference = `Class::method`, `obj::method`, `Class::instanceMethod` (receiver = first arg), or `Class::new`.** It implements a functional interface without calling the method at `::`. Equivalent to a lambda that only forwards. Prefer it for a straight existing method; it is not magically faster, and it is not a static call just because the class name sits on the left.
