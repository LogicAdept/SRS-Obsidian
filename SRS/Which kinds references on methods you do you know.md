<!--
reps: 0
priority: 0
-->
#Java/Lambdas #Java/Versions/8 #SRS

# Which kinds references on methods you do you know

> [!abstract] Short answer
> **Four kinds of method reference (`::`), Java 8.** (1) **Static** — `Integer::parseInt`. (2) **Bound instance** — `System.out::println` (receiver evaluated at `::`). (3) **Unbound instance** — `String::length` (first SAM argument is the receiver). (4) **Constructor / array** — `ArrayList::new`, `int[]::new`. The dump’s three bullets collapse (2) and (3) into one “instance” line. `super::name` is a bound-like form. Not a method call yet.

## The dump’s three, plus the split interviewers want

A method reference names an invocation (or a `new`) **without running it**. Evaluating `::` yields a functional-interface instance; the method runs later when the SAM is invoked ([[What is method reference]], [[What is lambda what and specifics using lambda]]).

**Static:** `Type::staticMethod` — no receiver. Example from the language: `System::currentTimeMillis`.

**Instance with a receiver already (bound):** `expr::instanceMethod`. The Primary is evaluated **now**. `System.out::println`, `"abc"::length`. If that Primary is `null`, `NullPointerException` happens at the `::`, not at `accept` ([[What does the System.out println method reference mean]]).

**Instance of an arbitrary object (unbound):** `Type::instanceMethod`. The SAM’s first argument is `this`. `String::length` is this form — **not** static. Same idea: `List::size` ([[What kinds of method references exist in Java]]).

**Constructor / array:** `ClassType::new`, `ArrayType::new` (`ArrayList<String>::new`, `int[]::new`). Overload of constructors is chosen from the target functional interface, not from fake syntax like `Arrays::sort(int[])`.

`super::toString` / `TypeName.super::name` exist; they need an enclosing instance (not a static context).

```d2
root: "method reference ::" {
  shape: rectangle
}
st: "static\nInteger::parseInt" {
  shape: rectangle
}
bound: "bound instance\nSystem.out::println" {
  shape: rectangle
}
unb: "unbound instance\nString::length" {
  shape: rectangle
}
ctor: "constructor / array\nArrayList::new  int[]::new" {
  shape: rectangle
}
root -> st
root -> bound
root -> unb
root -> ctor
```

**Fig. 1.** Dump = static + instance + constructor. Interviews split instance into **bound** vs **unbound**.

```java
ToIntFunction<String> unbound = String::length;
Consumer<String> bound = System.out::println;
LongSupplier stat = System::currentTimeMillis;
Supplier<ArrayList<String>> ctor = ArrayList::new;
IntFunction<int[]> array = int[]::new;
```

**Listing 1.** One example of each kind. `String::length` takes a `String` (the receiver). `System.out::println` already has `out`.

> [!warning] “Instance” is two kinds
>
> Treating `String::length` as static because `String` is a class name is the usual miss. Bound vs unbound also differ on **when** the receiver is evaluated. You cannot write `ContainingClass::method(int)` to pick an overload — use a lambda if the target type is too loose.

> [!tip] Interview answer
>
> **Four: static, bound instance, unbound instance, constructor (`::new`, including arrays).** Dump lists three and folds both instance forms together. Give `Integer::parseInt`, `System.out::println`, `String::length`, `ArrayList::new`. Java 8; same deferred object as a lambda.
