<!--
reps: 0
priority: 0
-->
#Java/Language/NestedClasses #Java/OOP/Constructors #Java/Language/Modifiers/Static #SRS

# Does a static nested class have a constructor in Java?

> [!abstract] Short answer
> **Yes.** A `static` nested class is a **class**, so it has constructors like any other class. If you declare none, a **default constructor** is synthesized — with **no** hidden enclosing-instance parameter. You instantiate it with `new Outer.Nested(...)`, not `outer.new Nested(...)`. Nested kinds: [[How would you explain nested classes in Java and when to use each kind]]. Default constructors: [[How would you explain the default constructor synthesized by the Java compiler]]. Constructors: [[What is constructor]].

## A class, without an enclosing instance

A member class may be declared `static`. That nested class is **not** an inner class (an inner class is nested and not explicitly or implicitly `static`). `static` on a class is legal only for **member** and **local** classes, not for a top-level class.

Because it is a class, the usual constructor rules apply: you may declare one or more constructors (overloads), they are not members and are not inherited, and if the class declares none, a default constructor is implicit. For a **member class that is not inner**, that default constructor has **no** extra formal parameter. The extra enclosing-instance parameter exists only on the default constructor of a **non-`private` inner member class**.

```d2
direction: down
st: "static class Nested" {
  width: 220
  height: 40
  style.fill: "#e3f2fd"
}
ctor: "Nested() / Nested(args)\nordinary constructors" {
  width: 260
  height: 50
  style.fill: "#e8f5e9"
}
newx: "new Outer.Nested(...)\nno Outer instance required" {
  width: 280
  height: 50
  style.fill: "#e8f5e9"
}
st -> ctor
ctor -> newx
```

**Fig. 1.** Construction is `new` on the nested type name. There is no hidden `Outer.this` argument.

```java
class Outer {
    private static int n = 1;

    static class Nested {
        final int value;

        Nested() {
            this(n);
        }

        Nested(int value) {
            this.value = value;
        }
    }

    static class Empty {} // implicit Nested-style default constructor
}

class Demo {
    static Outer.Nested make() {
        return new Outer.Nested(2); // no Outer instance
    }

    static Outer.Empty empty() {
        return new Outer.Empty();
    }
}
```

**Listing 1.** `Nested` declares two constructors. `Empty` gets a default constructor with no enclosing-instance parameter. Both can read `Outer`’s `private static` members.

A member class of an **interface** is implicitly `static`, so it is also a static nested class and may declare constructors. That constructor belongs to the nested class, not to the interface: [[Can a Java interface declare a constructor]]. Member enums and records are implicitly `static` too; they follow enum/record constructor rules, not inner-class construction.

Inner member classes still have constructors, but `new` is qualified by an enclosing instance (`outer.new Inner()`). You cannot write `static` on a top-level class to “make it nested.” Nested vs inner: [[How would you explain categories of Java classes such as nested and anonymous]] and [[Which specifics using classes static and inner in how is difference between]]. Constructors are not overridden: [[Can you override a constructor the same way you override a method]].

> [!warning] “Static classes have no constructors” confuses them with interfaces
> Interfaces have no constructors. A `static` nested **class** does. Missing constructor declarations only means the compiler supplies a default one, as for a top-level class.

> [!warning] `outer.new Nested()` is the inner-class form
> If `Nested` is `static`, the enclosing instance is not part of construction. `new Outer.Nested()` is the legal expression. Using an instance qualifier as if it were an inner class is a compile-time error.

> [!warning] The default constructor still needs an accessible no-arg `super()`
> Same rule as any class: if the nested class’s superclass has no accessible no-arg constructor, you must declare a constructor that chains correctly. `static` does not skip `super`.

> [!tip] Interview answer
> Yes. A static nested class is an ordinary class without an enclosing instance, so it has constructors — including a synthesized default constructor if you write none. You create instances with new Outer.Nested(...). That is not the inner-class outer.new Inner() form, and it is not the same as an interface, which cannot declare constructors.
