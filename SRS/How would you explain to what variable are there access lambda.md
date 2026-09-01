<!--
reps: 0
priority: 0
-->
#Java/Lambdas #Java/Versions/8 #SRS

# How would you explain to what variable are there access lambda

> [!abstract] Short answer
> **A lambda sees the enclosing class, plus `final` or effectively final locals.** Names, `this`, and `super` mean the **surrounding** context — not a new anonymous-class `this`. Locals, formals, and `catch` parameters used from the body must be `final` or effectively final and definitely assigned. Instance fields and statics are fine because they go through the enclosing class. You cannot call the target functional interface’s `default` methods as `this.foo()` — `this` is not the lambda.

## Enclosing names, frozen locals

The body runs later, but name lookup is the same as the code around the lambda (lambda parameters add new names). That is **not** how an anonymous class works: inside `new Foo() { ... }`, `this` is the new object; inside `() -> ...`, `this` is the enclosing instance. If you need the lambda to “talk about itself,” use an anonymous class or a method reference ([[How would you explain lambda expressions in Java]], [[Which variables can lambda expressions access in Java]], [[Which variables can a Java lambda expression capture]]).

A local, method/constructor/lambda parameter, or exception parameter **used but not declared** in the lambda must be `final` or **effectively final**. Effectively final means you could add `final` without a compile error: at most one assignment, no `++` / `--`. The local must also be **definitely assigned** before the lambda is created. Reassigning after the lambda is written still breaks “effectively final” even if the write sits below the lambda in the method.

Classic `for (int i = 0; ...; i++)` indexes are one variable for the whole loop — capturing `i` is illegal if `i` is incremented. Enhanced-`for` variables are **per iteration**, so capturing `s` from `for (String s : list)` is legal ([[How would you explain effectively final]]).

Instance fields and statics have no effectively-final rule of that kind. Assigning `this.n = 1` inside the lambda is allowed; the captured thing is `this`, not a copy of `n`. A captured **reference** may still mutate the object (`list.add`); you just cannot reassign the variable `list`.

Default methods on the **target** functional interface are not in scope as `this.andThen(...)`. The lambda is not an instance of that interface from the language’s point of view of `this`. An anonymous class implementing the same interface can call those defaults ([[How would you explain default interface methods since Java 8]]).

```d2
direction: down
encl: "enclosing class\nthis / fields / statics" {
  width: 260
  height: 55
  style.fill: "#e8f5e9"
}
loc: "locals / params / catch\nfinal or effectively final" {
  width: 280
  height: 55
  style.fill: "#e3f2fd"
}
lam: "lambda body" {
  width: 200
  height: 50
  style.fill: "#fff8e1"
}

encl -> lam
loc -> lam
```

**Fig. 1.** `this` is the outer object. Locals are a frozen snapshot of the variable (same binding), not a live cell you can reassign.

```java
import java.util.List;
import java.util.function.Consumer;

class Box {
    int n;
    static int S = 1;

    void m(int x, List<String> list) {
        int y = 1;
        Consumer<String> c = s -> {
            n++;                 // field via enclosing this — legal
            System.out.println(x + y + S + s);
            list.add(s);         // mutate object; do not reassign list
        };
        for (String item : list) {
            Consumer<String> once = s -> System.out.println(item);
            once.accept(s);
        }
        // for (int i = 0; i < 3; i++) { () -> i; }  // illegal: i not effectively final
        // y = 2;                                    // would make the lambda illegal
        // c = s -> this.andThen(c);                 // this is Box, not Consumer
    }
}
```

**Listing 1.** Locals `x` / `y` / enhanced-`for` `item` are effectively final. `n` and `S` are the enclosing class. Classic `for` index `i` is not capturable once incremented.

> [!warning] `this` is not the lambda
> Dump wording that lambdas are “just like anonymous classes” is wrong for `this` / `super` / unqualified `toString()`. That is why a lambda cannot invoke the functional interface’s `default` methods on itself. Use an anonymous class when you need that.

> [!warning] Effectively final is the variable, not the object
> `list.add` is legal; `list = other` is not. A write anywhere in the method (`y++` after the lambda) makes `y` non-capturable. `null` is irrelevant — the rule is assignment count, not nullity. The captured local must already be definitely assigned.

> [!tip] Interview answer
> **Locals: `final` or effectively final (and definitely assigned). Fields and statics: yes, via enclosing `this`.** `this` in a lambda is the outer instance, unlike an anonymous class. Enhanced-`for` items are capturable; a classic `for` index usually is not. Default methods of the SAM type are not `this.foo()` from the lambda.
