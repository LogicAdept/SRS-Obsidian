<!--
reps: 0
priority: 0
-->
#Java/Language #Java/OOP/Polymorphism #SRS

# How would you explain Overload vs Override?

> [!abstract] Short answer
> **Overload:** same name, signatures that are **not** override-equivalent; the compiler picks a signature from the **compile-time** argument types. **Override:** a subclass **instance** method with a **subsignature** of an inherited instance method; the JVM picks the body from the **run-time class**. Overloading: [[How would you explain method overloading in Java]]. Overriding: [[How would you explain method overriding in Java]]. Dispatch: [[How would you explain dynamic runtime polymorphism in Java]].

## Compile-time name vs run-time body

**Overload** is several methods of one class (declared or inherited) sharing a name with different formal-parameter types. Return type, `throws`, and parameter names do **not** distinguish them. Resolution is compile-time: argument count and static types, then strict / boxing / varargs phases. If the chosen signature is an instance method, lookup for **that** signature is still virtual.

**Override** is one signature, a new instance implementation in a subclass (or a concrete method implementing an `abstract` / interface method). Rules: at least as much access ([[Can you use a weaker access modifier when overriding a method]]), no extra **checked** exceptions ([[What happens if an override declares a broader checked exception than the parent]]), return-type-substitutable ([[Can you declare a narrower return type when overriding a method]]). `static` **hides** ([[Can static methods be overridden in Java]]). Constructors **overload**, they do not override ([[Can you override a constructor the same way you override a method]]).

A subclass method with the **same name and different parameters** overloads the inherited name; it does **not** replace the parent method. A subclass method with the **same** parameter types overrides (or errors if it collides with `static` / `final` / a non-substitutable return type).

```d2
direction: down
ol: "overload\ncompile time\nwhich signature?" {
  width: 220
  height: 55
  style.fill: "#e3f2fd"
}
ov: "override\nrun time\nwhich body for that signature?" {
  width: 280
  height: 55
  style.fill: "#e8f5e9"
}
ol -> ov: "instance invoke"
```

**Fig. 1.** Overload chooses a signature. Override chooses which class’s method of that signature runs.

```java
class Printer {
    void print(int n) {}
    void print(String s) {}
}

class ColorPrinter extends Printer {
    @Override
    void print(int n) {}

    void print(double d) {}
}

class Use {
    static void go() {
        Printer p = new ColorPrinter();
        p.print(1);
        p.print("hi");
    }
}
```

**Listing 1.** `print(int)` and `print(String)` overload in `Printer`. `ColorPrinter.print(int)` overrides; `print(double)` is a new overload. `p.print(1)` binds `print(int)` then runs `ColorPrinter.print(int)`. `p.print("hi")` still runs `Printer.print(String)`.

> [!warning] “Cannot widen `throws`” means **checked** exceptions
> An override may add unchecked exceptions. It must not add a checked type that is not a subtype of one already listed on the parent. Overloads have **no** `throws` relationship to each other.

> [!warning] Same name in a subclass is not automatically an override
> `void m(int)` in the parent and `void m(long)` in the child is overloading. `Parent x = new Child(); x.m(1);` still runs `Parent.m(int)` unless the child also overrides `m(int)`.

> [!warning] `static` is hiding, not overriding
> `Parent.m()` vs `Child.m()` with the same signature: the compile-time type of the **qualifier** chooses which `static` method. Constructors can be overloaded; they are never overridden.

> [!tip] Interview answer
> Overloading is several signatures with the same name; the compiler picks one from the static types of the arguments. Overriding is a subclass instance method with the same signature as a parent instance method; the JVM picks the body from the run-time class. An override cannot be less visible and cannot throw extra checked exceptions. A subclass method with different parameter types overloads the name instead of replacing the parent method.
