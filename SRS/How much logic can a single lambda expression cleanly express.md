<!--
reps: 0
priority: 0
-->
#Java/Lambdas #SRS

# How much logic can a single lambda expression cleanly express?

> [!abstract] Short answer
> **As much as one method body — but the point of a lambda is one unit of behavior.** The language allows either a **single expression** or a **block** (loops, `if`, locals, several `return`s). There is no statement-count cap. Use a lambda for a **simple** functional-interface instance you pass as code; if you need a name, fields, extra methods, a constructor, or `this` meaning the function itself, use a method / method reference or a class instead.

## Expression body versus block body

A lambda is “like a method”: parameters plus a body that is an **expression** or a **block**. Evaluating the lambda does **not** run the body; that happens later when the functional method is invoked ([[How would you explain lambda expressions in Java]], [[What is functional interface]]).

An **expression** body is evaluated and that value is the result (`() -> 42`, `x -> x + 1`). A **`return` statement is not an expression** — it belongs in a **block** (`{ return …; }`). A void method invocation may be an expression body without braces (`email -> System.out.println(email)`).

A **block** body is a normal `{ … }` block. It may be as large as any method body. The spec’s own example is a block with `if` / `else`, a `for` loop, a local, and two `return`s. That compiles; “one line only” is not a language rule.

A block must be **void-compatible** (every `return` is `return;`) or **value-compatible** (the block cannot complete normally, and every `return` is `return` *Expression*`;`). A mix is a compile-time error: `() -> { if (…) return "done"; System.out.println("done"); }` is neither.

```d2
direction: down
cue: "how much logic?" {
  width: 220
  height: 45
  style.fill: "#e3f2fd"
}
lang: "expression or block\nno size limit" {
  width: 260
  height: 60
  style.fill: "#e8f5e9"
}
fit: "one unit of behavior\nsimple FI instance" {
  width: 260
  height: 60
  style.fill: "#fff3e0"
}
else: "named method / ::\nor local / anonymous class" {
  width: 280
  height: 60
  style.fill: "#f3e5f5"
}
cue -> lang
cue -> fit
fit -> else: "fields, extra methods,\nthis = the function"
```

**Fig. 1.** The compiler accepts a fat block. “Cleanly” means one behavior you pass as data. Recursion via `this`, extra methods, or fields: [[What is method reference]], [[How would you explain nested classes in Java and when to use each kind]].

`this` / `super` in a lambda mean the **enclosing** context, not the lambda. If the function must refer to itself, use a method reference or an anonymous class. Captured locals must still be final or effectively final ([[How would you explain effectively final]]). Checked throws follow the target SAM, not the size of the block ([[Can a lambda throw a checked exception]]).

Official “when to use”: encapsulate a **single unit of behavior** to pass to other code (per-element action, completion, error). Use a lambda when you need a **simple** functional-interface instance and you do **not** need a constructor, a named type, fields, or additional methods. Those needs are why local and anonymous classes exist.

```java
import java.util.function.IntSupplier;
import java.util.function.IntUnaryOperator;

class Demo {
    static IntUnaryOperator expression() {
        return x -> x + 1;
    }

    static IntUnaryOperator sameAsBlock() {
        return (int x) -> { return x + 1; };
    }

    static IntSupplier complex(boolean early) {
        return () -> {
            if (early) return 12;
            int result = 15;
            for (int i = 1; i < 10; i++) {
                result *= i;
            }
            return result;
        };
    }

    static void voids() {
        Runnable empty = () -> {};
        Runnable print = () -> System.out.println("done");
        // IntUnaryOperator bad = x -> return x + 1; // return is a statement
        // IntSupplier neither = () -> {
        //     if (early) return 12;
        //     System.out.println("done");
        // }; // neither void- nor value-compatible
    }
}
```

**Listing 1.** Expression and block forms of the same increment. `complex` is the spec’s multi-statement shape (parameterized so both arms are reachable). `print` needs no braces because the body is a void invocation.

> [!warning] `return` without braces does not compile
> `x -> return x;` is illegal: `return` is a statement. Use `x -> x` or `x -> { return x; }`. A block that sometimes `return`s a value and sometimes falls out the bottom is neither void-compatible nor value-compatible — also a compile-time error, even if you think of it as “almost a method.”

> [!warning] A legal block can still be the wrong tool
> A lambda may contain a loop and several returns; that does not make it a good API at the call site. If the body needs a name, tests, fields, extra methods, or to mean `this` as the function, extract a method (`Foo::bar`) or write a class. “Simple lambda” is the documented use; the grammar is not a style ceiling.

> [!tip] Interview answer
> **The body is one expression or a block — there is no statement limit; a block can loop and return like a method.** Prefer a lambda for one unit of behavior, usually a short expression you pass as an argument. When you need braces for `return` or several statements, that is still legal; when you need a name, fields, extra methods, or `this` as the function itself, use a method reference or a class.
