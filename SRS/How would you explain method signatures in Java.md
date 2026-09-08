<!--
reps: 0
priority: 0
-->
#Java/Language #Java/OOP/Polymorphism #SRS

# How would you explain method signatures in Java?

> [!abstract] Short answer
> A method **signature** is the **name**, the **type parameters** if any, and the **formal parameter types**. It is **not** the return type, `throws`, parameter names, or `public` / `static` / `final`. Two methods in one class with **override-equivalent** signatures are a compile-time error, even if one is `abstract`. Overload vs override is decided from signatures: [[How would you explain Overload vs Override]].

## What is in the signature

Two methods or constructors `M` and `N` have the **same** signature when they have the same name, the same type parameters, and the same formal parameter types after adapting `N`’s parameters to `M`’s type parameters.

The signature of `m1` is a **subsignature** of `m2` when they are the same, or when `m1`’s signature is the **erasure** of `m2`’s. That lets a pre-generics `List toList(Collection c)` still override a later `<T> List<T> toList(Collection<T> c)`. Two signatures are **override-equivalent** when either is a subsignature of the other.

Everything else is a separate check:

| In the signature | Not in the signature |
| --- | --- |
| Method / constructor name | Return type (`void`, primitive, class) |
| Type parameters (`<T>`) | `throws` types |
| Formal **parameter types**, in order | Parameter **names** |
| Last parameter `String...` is still `String[]` | `public` / `protected` / `private` |
| | `static`, `final`, `synchronized`, `native` |

`String...` and `String[]` denote the **same** parameter type, so you cannot declare both in one class. Changing only the return type is **not** an overload: it collides ([[Can you declare a narrower return type when overriding a method]]). Changing parameter types, count, or type order **is** an overload ([[How would you explain method overloading in Java]]). An instance method with a subsignature of an inherited instance method **overrides** ([[How would you explain method overriding in Java]]). Access and `throws` are extra override rules, not signature pieces ([[Can you when override method modifier access type type or their count or their order order elements throws]]).

```d2
direction: down
sig: "name + type params\n+ parameter types" {
  width: 280
  height: 60
  style.fill: "#e3f2fd"
}
same: "override-equivalent\nin one class → compile error" {
  width: 300
  height: 60
  style.fill: "#ffebee"
}
diff: "same name, not equivalent\n→ overload" {
  width: 280
  height: 60
  style.fill: "#e8f5e9"
}
sig -> same
sig -> diff
```

**Fig. 1.** The compiler compares signatures, not “the whole declaration line.”

```java
class Printer {
    void print(int n) {}
    void print(String s) {}          // overload: different parameter types

    // String print(int n) { return ""; }  // same signature as print(int) — illegal
    // void print(int n) throws Exception {} // still print(int) — illegal
    // void print(int value) {}            // names are not in the signature — illegal
}

class ColorPrinter extends Printer {
    @Override
    void print(int n) {}             // override: subsignature of print(int)

    void print(int n, int m) {}      // overload of the inherited name
}
```

**Listing 1.** `print(int)` and `print(String)` are two signatures. A second `print(int)` with a different return type or `throws` is not a new signature.

A constructor has a signature too (`this` / `super` resolution uses it). Constructors overload; they do not override. `static` vs instance is **not** a signature difference: you still cannot declare both `static void m(int)` and `void m(int)` in one class.

> [!warning] Return type is not how Java overloads
> Interview shorthand “signature = name + parameters + return type” is C++ / JVM-descriptor thinking. In the **language**, `int f()` and `String f()` in one class do not compile. Covariant returns are an **override** rule on top of a matching signature, not a second overload.

> [!warning] Erasure can make two source shapes one signature
> `void m(List<String> x)` and `void m(List<Integer> x)` are override-equivalent after erasure (`List`). The class cannot hold both. A raw `void m(List x)` can be a subsignature of a generic `void m(List<T> x)`, which is how old subclasses keep overriding.

> [!tip] Interview answer
> **A Java method signature is the name plus the formal parameter types — not the return type, not `throws`, not the names of the parameters.** Same name and same parameter types in one class is a clash. Different parameter types is overloading; a subclass instance method with that same signature is overriding.
