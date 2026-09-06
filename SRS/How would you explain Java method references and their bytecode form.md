<!--
reps: 0
priority: 0
-->
#Java/MethodReferences #Java/Bytecode #Java/Lambdas #SRS

# How would you explain Java method references and their bytecode form?

> [!abstract] Short answer
> **A method reference is `TypeOrExpr::name` (or `::new`): it names a method or constructor without calling it yet.** Evaluating it yields a functional-interface instance. The compiler emits **`invokedynamic`** (opcode 186) whose bootstrap is typically `LambdaMetafactory.metafactory`. Unlike a lambda, the implementation `MethodHandle` **is the referenced method** — no desugared synthetic body. A bound receiver is a **capture** argument, evaluated once when the `::` expression runs.

## `::` in the language, `invokedynamic` in the class file

A method reference is a poly expression, legal only in assignment, invocation, or cast context. Evaluation produces a functional-interface object; the named method runs later, when that object’s SAM is invoked ([[What is method reference]], [[What is functional interface]]).

Four source shapes (same meaning as a one-call lambda):

| Kind | Syntax | SAM vs method |
| --- | --- | --- |
| Static | `ContainingClass::staticMethod` | all SAM args → method args |
| Bound instance | `expr::instanceMethod` | SAM args → method args; receiver is `expr` |
| Unbound instance | `ContainingType::instanceMethod` | first SAM arg is the receiver |
| Constructor / array | `ClassName::new`, `int[]::new` | SAM args → constructor / length |

`String::compareToIgnoreCase` is `(a, b) -> a.compareToIgnoreCase(b)`. `Person::compareByAge` is `(a, b) -> Person.compareByAge(a, b)`. `HashSet::new` is `() -> new HashSet<>()`. `super::name` and `TypeName.super::name` exist too. You cannot write `Arrays::sort(int[])` — overload resolution uses the **target** function type; use a lambda for a tighter match ([[What kinds of method references exist in Java]], [[How would you explain lambda expressions in Java]]).

`ReferenceType::identifier` is searched twice (arity `n` and `n-1`) because it might be static **or** unbound instance. If both a static method and an instance method apply, it is a compile-time error (the `C::size` case). Bound form `expr::m`: `expr` is evaluated **immediately**; `null` throws `NullPointerException` then, not at `accept`. That expression is **not** re-evaluated on later SAM calls. A lambda does not evaluate a qualifier that way.

```d2
direction: down
src: "String::length\nSystem.out::println" {
  width: 260
  height: 55
  style.fill: "#e3f2fd"
}
indy: "invokedynamic\nbootstrap metafactory" {
  width: 280
  height: 55
  style.fill: "#fff3e0"
}
link: "Linkage → CallSite factory" {
  width: 260
  height: 45
  style.fill: "#e8f5e9"
}
cap: "Capture → function object" {
  width: 260
  height: 45
  style.fill: "#e8f5e9"
}
inv: "Invocation → referenced method" {
  width: 280
  height: 45
  style.fill: "#f3e5f5"
}
src -> indy
indy -> link
link -> cap
cap -> inv
```

**Fig. 1.** Source `::` becomes one `invokedynamic`. Linkage builds a `CallSite`; capture (with any bound receiver) produces the SAM object; invocation calls the implementation handle. Bound `System.out::println`: [[What does the System.out println method reference mean]].

Bytecode: `invokedynamic` indexes a dynamically-computed call site. Resolution binds a `CallSite` to **that** instruction, then invokes its target handle (as `MethodHandle.invokeExact`) with the stack capture args. `LambdaMetafactory` methods are the usual **bootstrap**: they take the target interface, the SAM name/type, and a **direct** `MethodHandle` for the implementation.

Three phases:

1. **Linkage** — bootstrap runs; may load a hidden implementation class; returns a `CallSite` factory.
2. **Capture** — the `CallSite` target runs (the `invokedynamic`); extra parameters beyond the SAM are **captured** (bound receiver). May allocate a new object or reuse one. **Identity is unpredictable** (`==`, locking, `identityHashCode` are not stable).
3. **Invocation** — the SAM call invokes the implementation handle with captured args plus SAM args.

API note for translation: a lambda body is **desugared** to a method, then `invokedynamic` points at that method. A method reference **skips desugaring** — the handle is the referenced method or constructor. `factoryType` parameters are capture types; its return type is the functional interface. Invariant: capture arity `K` plus SAM arity `N` equals implementation arity `M` (instance handles already include the receiver). If the implementation is an instance method and `K > 0`, the first capture argument must be non-`null`.

```java
import java.util.ArrayList;
import java.util.List;
import java.util.function.Consumer;
import java.util.function.Function;
import java.util.function.Supplier;

class Demo {
    static void kinds() {
        Supplier<List<String>> ctor = ArrayList::new;
        Function<String, Integer> unbound = String::length;
        Consumer<String> bound = System.out::println;
        Function<Integer, String> stat = String::valueOf;
        List<String> names = ctor.get();
        names.add("ab");
        names.forEach(bound);
        int n = unbound.apply("ab"); // 2
        // String s = null;
        // Function<Integer, Integer> boom = s::length; // NPE now, not at apply
    }
}
```

**Listing 1.** Constructor, unbound instance, bound instance, static. Conceptual class-file shape: `invokedynamic #BootstrapMethods[LambdaMetafactory.metafactory]` returning the SAM type; `System.out::println` pushes `System.out` as the capture argument before that instruction.

> [!warning] Bound `expr::m` NPEs when the reference is created
> `s::length` with `s == null` throws at the `::` expression, because a Primary qualifier is evaluated then and a null Primary is always NPE (the referenced method cannot be `static`). `list.forEach(s::m)` still evaluates `s` once, even if `forEach` never calls `accept`. Unbound `String::length` has no qualifier to NPE at creation.

> [!warning] Do not trust `==` on the function object; do not assume a synthetic method
> Capture may reuse an instance. `==` / locking on the SAM object is not a contract. A method reference does **not** compile to `invokevirtual` of `length` at the `::` site — that call happens later through the metafactory object. `Type::name` is an error if both a static and an instance method apply. Checked exceptions on the referenced method still need to be covered by the target SAM ([[Can a lambda throw a checked exception]]).

> [!tip] Interview answer
> **A method reference is a named one-call lambda: static, bound instance, unbound instance (`receiver` first), or `::new`.** The class file uses `invokedynamic` bootstrapped by `LambdaMetafactory`; the implementation handle is the referenced method, not a desugared lambda body. A bound receiver is captured when the `::` expression runs — `null` throws then — and the function object’s identity is not specified.
