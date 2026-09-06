<!--
reps: 0
priority: 0
-->
#Java/Lambdas #Java/FunctionalInterfaces #Java/Versions/8 #SRS

# How would you explain lambda expressions in Java?

> [!abstract] Short answer
> **A lambda is an anonymous method that implements a functional interface:** parameters, `->`, and a body that is one **expression** or a **block**. Evaluating `() -> …` creates (or reuses) a SAM object; it does **not** run the body. The body runs later, when that object’s functional method is invoked. Java 8. Target typing fills in the type from assignment, a method argument, or a cast.

## A method without a name, a type from context

A lambda is “like a method”: formal parameters plus a body expressed in terms of those parameters. It is always a poly expression, legal only in an **assignment**, **invocation**, or **casting** context whose target is a functional interface ([[What is functional interface]], [[How would you explain core functional interfaces in java.util.function]]). Congruence: same arity as the SAM; an explicitly typed lambda’s parameter types must **exactly** match; the body must be void-compatible or value-compatible with the SAM result.

Syntax: `(params) -> body`. `->` binds very loosely. Zero parameters use `()`. One inferred parameter may drop the parentheses (`s -> s.isEmpty()`). Mix inferred and declared types in one list is illegal (`(x, int y) -> …`). Type arguments on the lambda itself are not allowed.

The body is either a **single expression** (its value is the result) or a **block**. `return` is a statement, so it needs braces. A value-compatible block must `return` (or throw / loop forever) on every path. A void method invocation may be an expression body without braces. A statement expression such as `list.add(s)` can target **either** `Predicate` (boolean result kept) or `Consumer` (result discarded), depending on the target type.

```d2
direction: down
src: "(s) -> s.length()\npoly expression" {
  width: 240
  height: 55
  style.fill: "#e3f2fd"
}
tgt: "target type\nFunction / Predicate / …" {
  width: 260
  height: 55
  style.fill: "#fff3e0"
}
obj: "SAM instance\nbody not run yet" {
  width: 240
  height: 50
  style.fill: "#e8f5e9"
}
run: "apply / test / accept\nruns the body" {
  width: 240
  height: 50
  style.fill: "#f3e5f5"
}
src -> tgt
tgt -> obj: "evaluation"
obj -> run: "later invocation"
```

**Fig. 1.** Evaluation materializes a functional-interface object. Execution of the body is a later SAM call. How large that body can be: [[How much logic can a single lambda expression cleanly express]]. Compact form when the body is one existing method: [[How would you explain Java method references and their bytecode form]].

`this` / `super` in the body mean the **enclosing** instance, not the lambda. Locals captured from the enclosing scope must be final or effectively final and definitely assigned ([[How would you explain effectively final]], [[Which variables can a Java lambda expression capture]]). Checked exceptions the body can throw must be covered by the target SAM ([[Can a lambda throw a checked exception]]).

Use a lambda for a **single unit of behavior** you pass as data (per-element action, completion, error). If you need a constructor, a named type, fields, extra methods, or `this` as the function itself, use a local / anonymous class or a method reference ([[How would you explain nested classes in Java and when to use each kind]]).

The compiler typically desugars the body to a method and emits **`invokedynamic`** bootstrapped by `LambdaMetafactory`. The identity of the resulting object is **unspecified**: evaluation may allocate or reuse; `==`, locking, and `identityHashCode` are not a contract. `ClassCastException` can still occur at invocation if a bridge must check erased parameter types.

```java
import java.util.ArrayList;
import java.util.List;
import java.util.function.Consumer;
import java.util.function.Function;
import java.util.function.Predicate;

class Demo {
    static void explain() {
        List<String> list = new ArrayList<String>();
        Predicate<String> p = s -> list.add(s);
        Consumer<String> c = s -> list.add(s);
        Function<String, Integer> len = s -> s.length();
        Function<String, Integer> block = s -> { return s.length(); };
        list.forEach(x -> System.out.println(x));
        boolean added = p.test("a");
        c.accept("b");
        int n = len.apply("hi");
        // s -> return s.length(); // illegal: return is a statement
        // (x, int y) -> x + y;    // illegal: mixed inferred / declared
    }
}
```

**Listing 1.** `list.add(s)` is a statement expression: `Predicate` keeps the `boolean`, `Consumer` discards it. Expression and block forms of the same function. `forEach` is invocation-context target typing.

> [!warning] Creating the lambda is not calling it
> `Function<String, Integer> f = s -> s.length();` does not call `length`. `f.apply("hi")` does. Do not use `==` on the SAM object to mean “same lambda text.” A bound method reference evaluates its qualifier immediately; a lambda does not have that qualifier.

> [!warning] The body is checked against the SAM, not the surrounding `try`
> Parameter types of an explicitly typed lambda must match the function type exactly — no extra boxing/contravariance there. Result expressions *are* in assignment context, so boxing of the result is allowed. `this` in the body is the enclosing class; you cannot recurse with `this` as the lambda. Capture is a snapshot of effectively final locals, not live variables.

> [!tip] Interview answer
> **A Java 8 lambda is `(params) -> expression-or-block` that implements a functional interface inferred from context.** Evaluating it yields a SAM instance; the body runs when `apply` / `test` / `accept` is called. Use it for one unit of behavior; use a method reference when that behavior is already a named method, and a class when you need fields, extra methods, or a real `this`.
