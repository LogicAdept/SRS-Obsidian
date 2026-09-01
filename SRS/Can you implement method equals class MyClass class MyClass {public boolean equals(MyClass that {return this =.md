<!--
reps: 0
priority: 0
-->
#Java/HashCodeEquals/Implementation #SRS

# Can you implement `equals` as `equals(MyClass that)`?

> [!abstract] Short answer
> **It compiles, but it is not `Object.equals`.** `equals(MyClass)` has a different signature from `equals(Object)`, so it **overloads** instead of **overriding**. `HashMap` / `HashSet` still call the inherited `equals(Object)` (reference equality). Put `@Override` on that method and the compiler rejects it.

## Overload versus override

`Object.equals` is `public boolean equals(Object obj)`. Override requires an **override-equivalent** signature (same name and same parameter types, allowing erasure). `equals(MyClass)` is the same name with a **different** parameter type, so the name is **overloaded**. Overload choice uses the **compile-time** argument type; only then does instance dispatch run for that chosen signature.

```text
Object.equals(Object)     inherited — what collections call
MyClass.equals(MyClass)   extra overload — only when the compiler
                          sees a MyClass (or subtype) argument

@Override
public boolean equals(MyClass that)   // does not compile
```

**Listing 1.** Two methods named `equals`, not one override. [[How do you override equals correctly in Java]] is `equals(Object)` plus `hashCode`. [[What is the Object equals contract]] is what you must implement.

```d2
direction: down
call: "a.equals(x)" {
  width: 220
  height: 60
  style.fill: "#e3f2fd"
}
my: "x typed MyClass\n→ equals(MyClass)\noverload" {
  width: 260
  height: 90
  style.fill: "#fff3e0"
}
obj: "x typed Object\n→ equals(Object)\nObject identity" {
  width: 260
  height: 90
  style.fill: "#ffebee"
}

call -> my
call -> obj
```

**Fig. 1.** Same runtime object, two compile-time types, two methods. Collections pass `Object`.

```java
class MyClass {
    int id;
    MyClass(int id) { this.id = id; }

    // Compiles. Does not override Object.equals.
    public boolean equals(MyClass that) {
        return that != null && id == that.id;
    }
}

MyClass a = new MyClass(1);
MyClass b = new MyClass(1);
Object o = b;

a.equals(b); // true  — overload, compile-time MyClass
a.equals(o); // false — Object.equals, a != o
```

**Listing 2.** Conceptual: value-style body on the overload, identity on the real `equals(Object)`. A `HashSet<MyClass>` uses the second path, so `a` and `b` are two elements. The dump’s `return this == that` only **looks** like `Object.equals`; collections never call it. [[How would you explain pitfalls when implementing equals and hashCode]]

The correct shape is `public boolean equals(Object o)` (`this == o`, `instanceof`, fields) and a matching `hashCode`. [[Why should equals and hashCode be overridden together]]

> [!warning] `@Override` is the cheap test
> If the compiler will not accept `@Override` on your `equals`, you are not overriding `Object.equals`. An `equals(MyClass)` that compares fields will pass your unit test `a.equals(b)` and still fail in a `HashMap` key. Do not add a typed overload “for convenience” next to a real `equals(Object)` — call sites pick by static type and symmetry dies.

> [!tip] Interview answer
> **You can write `equals(MyClass)`, but that overloads `Object.equals`, it does not override it.** Collections still use `equals(Object)`, which stays identity unless you override that signature. `@Override` on the typed method will not compile. The real method is `equals(Object)` plus `hashCode`.
