<!--
reps: 0
priority: 0
-->
#Java/Language #Java/OOP/Polymorphism #SRS

# How would you explain method overloading in Java?

> [!abstract] Short answer
> A method name is **overloaded** when two methods of a class (both declared, both inherited, or one of each) have the **same name** but signatures that are **not override-equivalent**. That is legal by itself: return types and `throws` need not match. The compiler picks **which signature** to call from the **argument count and compile-time types**. If that signature is an instance method, **run-time** lookup still chooses the implementation ([[How would you explain dynamic runtime polymorphism in Java]]). vs override: [[How would you explain Overload vs Override]]. Constructors: [[What is constructor overloading in Java]].

## Same name, different signature

A **signature** is the name, type parameters if any, and **formal parameter types**. It is **not** the return type, `throws` clause, parameter names, or `static` vs instance. Two signatures are **override-equivalent** when one is a subsignature of the other (same after adapting type parameters, or one is the erasure of the other). Two methods with override-equivalent signatures in one class are a **compile-time error**, even if one is `abstract`.

Overloading is the other case: same name, **not** override-equivalent. A subclass can **override** one overload and still **inherit** the others. An instance method may overload a `static` method if the signatures differ ([[Can an instance method overload a static method in Java]]). Changing only the return type is **not** an overload; it collides ([[Can you declare a narrower return type when overriding a method]]).

**Which overload.** Invocation uses the compile-time types of the arguments. Applicability is tried in three phases: **strict** (no boxing, no varargs), then **loose** (boxing/unboxing, still no varargs), then **variable arity**. If several methods remain in that phase, the **most specific** wins. Primitive widening among those phases: [[In what order is chosen candidate from list overloaded methods when call with primitive argument]]. After the signature is fixed, instance dispatch is still virtual for **that** signature.

```d2
direction: right
ct: "compile time\nname + argument types\n→ one signature" {
  width: 220
  height: 55
  style.fill: "#e3f2fd"
}
rt: "run time\ninstance method\n→ body in run-time class" {
  width: 240
  height: 55
  style.fill: "#e8f5e9"
}
ct -> rt: "if instance"
```

**Fig. 1.** Overload resolution chooses a signature before virtual lookup chooses a body.

```java
class Printer {
    void print(int n) {}
    void print(String s) {}
    static void print(double d) {}
}

class ColorPrinter extends Printer {
    @Override
    void print(int n) {}
}

class Use {
    static void go() {
        Printer p = new ColorPrinter();
        p.print(1);
        p.print("hi");
        Printer.print(1.0);
    }
}
```

**Listing 1.** Three `print` overloads. `p.print(1)` binds `print(int)` at compile time, then runs `ColorPrinter.print(int)`. `print(double)` is a `static` overload, not an override.

> [!warning] Return type and parameter names do not overload
> `int m(String s)` and `void m(String t)` have the same signature. So do `m(int... a)` and `m(int[] a)` for override-equivalence. You need a different parameter-type list (or arity that is not override-equivalent).

> [!warning] The compile-time type of the argument, not the run-time object, picks the overload
> `void f(Object o)` vs `void f(String s)`: `Object x = "hi"; f(x);` calls `f(Object)`. Cast or a more specific variable type is what changes the overload. After that, override can still replace the body.

> [!warning] Adding `m(Object...)` can steal calls that used to hit `m(Object)`
> A varargs overload is a fixed-arity `m(Object[])` in the first phase. `m(null)` may become ambiguous or prefer the array form. Boxing is a later phase than primitive widening.

> [!tip] Interview answer
> Overloading is several methods with the same name and different parameter-type lists in one class (including inherited ones). The compiler chooses the signature from the static types of the arguments; return type alone is not enough to distinguish them. If the chosen method is an instance method, the JVM still dispatches to the run-time class for that signature. Do not mix that compile-time choice with overriding, which replaces a method of the same signature.
