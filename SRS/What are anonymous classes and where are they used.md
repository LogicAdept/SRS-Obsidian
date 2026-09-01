<!--
reps: 0
priority: 0
-->
#Java/OOP #Java/Language/NestedClasses #SRS

# What are anonymous classes, and where are they used?

> [!abstract] Short answer
> **A nested inner class with no name, declared by `new Type(...) { ... }` or an enum constant’s `{ ... }`.** The expression both declares the class and creates one instance. Use it for a **one-shot** type: multi-method types, a one-site subclass, GUI handlers, `Runnable` / `Comparator`. A **single-method** interface is usually a **lambda**. Extra methods are legal but invisible through the supertype.

## `new` plus a class body is the declaration

An anonymous class is **nested**, but it is **not** a local class and **not** a member class. A local class has a simple name in a block; this form is a class instance creation expression that **ends with `{ ... }`**. That expression is the only declaration of that class. You hold the **instance** (assign it, pass it, return it); you cannot name the **type**.

The type after `new` is either a **class** (the anonymous type is a direct subclass of it) or an **interface** (a direct subclass of `Object` that implements it). The superclass or superinterface must be accessible and **freely extensible** — not `final`, not `sealed`, not an enum class.

The same idea with a name is a **local class**; drop the name when that type is needed **once** ([[How would you explain local classes in Java and their scoping rules]], [[How would you explain nested classes in Java and when to use each kind]]).

```d2
direction: down
anon: "Anonymous class" {
  width: 220
  height: 40
}
cls: "new Class(args) { }\nsubclass of that class" {
  width: 300
  height: 70
  style.fill: "#e8f5e9"
}
iface: "new Interface() { }\nsubclass of Object" {
  width: 300
  height: 70
  style.fill: "#e3f2fd"
}
enumc: "EnumConstant { }\nfinal subclass of the enum" {
  width: 300
  height: 70
  style.fill: "#fff3e0"
}
anon -> cls
anon -> iface
anon -> enumc
```

**Fig. 1.** The class body is attached to `new` (or to an enum constant). There is no `class Foo` header to name or subclass.

An anonymous class is **always an inner class**. It is never `abstract` and never `sealed`. The `new` form is **not** `final` (narrowing casts still care); an **enum-constant** anonymous class **is** `final`. You still cannot write `extends` of it: it has no name.

The constructor is **always implicit**. Arguments in `new Type(args)` are forwarded to a constructor of the superclass. For an interface, `args` is empty. Instance initializers in the body run after that `super(...)`. Locals of the enclosing method must be **final or effectively final** ([[How do you from class get access to field outer class]]). In a **static context** (static method or static field initializer) there is **no enclosing instance**, but the class is still inner — not a `static` nested class, and you cannot mark it `static` ([[How would you explain static nested classes in Java]]).

If the creation uses diamond `<>`, every non-`private` method in the body is treated as if it had `@Override`, so a mistyped override fails at compile time instead of becoming a new method.

```java
interface Greeter {
    void greet();
    void greetSomeone(String who);
}

class UsesAnonymous {
    void hello() {
        Greeter g = new Greeter() {
            @Override
            public void greet() {
                greetSomeone("world");
            }

            @Override
            public void greetSomeone(String who) {
                System.out.println("Hello " + who);
            }
        };
        g.greet();
    }

    void sortByLength(java.util.List<String> names) {
        names.sort(new java.util.Comparator<String>() {
            @Override
            public int compare(String a, String b) {
                return Integer.compare(a.length(), b.length());
            }
        });
    }

    Thread worker() {
        return new Thread(new Runnable() {
            @Override
            public void run() { }
        });
    }
}
```

**Listing 1.** `Greeter` has two methods, so it is not a functional interface. `Comparator` and `Runnable` are SAMs; a lambda is the usual replacement ([[How would you explain lambda expressions in Java]]). `Thread` is a one-site subclass of a class (`new Thread() { @Override public void run() { } }` is the same idea).

```java
enum Op {
    PLUS {
        @Override
        int apply(int a, int b) {
            return a + b;
        }
    };

    abstract int apply(int a, int b);
}
```

**Listing 2.** An enum constant with a class body is a **final** anonymous subclass of `Op`. Methods added only in that body are not part of `Op`. The same shape appears as a **field initializer** (`static final Op PLUS = new Op() { ... }`) when each “constant” needs its own subclass.

Typical uses:

- **One-shot implementation** at the call site (listener / callback). GUI toolkits (`EventHandler.handle`, `setOnAction`) are the textbook case.
- **Function / process objects**: `Comparator`, `Runnable`, `Thread`.
- **Override several methods** of a concrete class at one construction site (not a SAM, so a lambda cannot replace it).
- **Enum constant–specific behavior** (Listing 2) instead of a `switch`.

> [!warning] It is not a “local class without a name”
> Local and anonymous are two nested shapes. You instantiate the **object**. You do not need to “never refer to the instance.” You cannot refer to the **class** by name.

> [!warning] No constructor, and extra methods hide behind the supertype
> You cannot write `Type() { ... }` inside the body. Use instance initializers and `super` arguments on `new`. Declaring `void extra()` is legal; `g.extra()` does not compile if `g` is `Greeter`.

> [!warning] JDK 8 “no static members” is stale
> Since **Java SE 16** an inner class, including an anonymous one, may declare static members and static initializers, not only constant variables. It still cannot be declared `static` itself.

> [!warning] “Anonymous classes are `final`” is only half true
> The `new Type() { }` form is **not** `final`. The enum-constant form **is**. Neither can be named in an `extends` clause. Do not anonymous-extend a `final` or `sealed` class or an enum type — that is a compile-time error on `new`.

> [!tip] Interview answer
> **An anonymous class is a nameless inner class in `new Type() { ... }` — declaration and one instance together.** Use it once: multi-method types, a one-site subclass, GUI handlers, `Runnable` / `Comparator`. **You hold the instance; you cannot name the type. Extra methods do not show up on the supertype. A single abstract method should be a lambda.** Enum constants with a body are anonymous classes too, and those are `final`.
