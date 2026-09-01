<!--
reps: 0
priority: 0
-->
#Paradigms/OOP #Java/OOP/Polymorphism #SRS

# What is polymorphism?

> [!abstract] Short answer
> **Polymorphism** means using a value through a **common type** without knowing the **run-time class**. In Java interviews that is **subtype polymorphism**: `Shape s = new Square(3); s.area();` runs `Square.area` ([[How would you explain dynamic runtime polymorphism in Java]]). The **compiler** picks a **signature**; the **JVM** picks the **body** ([[How would you explain Overload vs Override]]). Override: [[How would you explain method overriding in Java]]. Principles: [[What are the main oop principles]].

## Same type, different bodies

The dump’s useful sentence: work through one **interface** (type) without the internals. `callAnotherUser(int, AbstractPhone phone)` then `phone.call(n)` is that: the parameter is the abstract type; each model **overrides** `call`. `@Override` only checks the signature ([[How does the Override annotation work]]). Inheritance supplies the subtype ([[What is inheritance]]). Abstraction is the type you publish ([[What is abstraction]]). Java OO: [[What does it mean that Java is object oriented]].

**The dump contradicts itself.** First it says the **compiler** chooses the action; later the phone example correctly says **dynamic** choice at **run time**. For **overriding**, believe the second. The compiler proves `call` exists on `AbstractPhone`. It does **not** pick `VideoPhone.call`. That is overload resolution vs virtual dispatch ([[How would you explain method overloading in Java]]). A cast of the reference does **not** change which override runs. `super.m()` and `static` / `private` calls do **not** use this lookup. Mechanisms: [[What mechanisms implement polymorphism in Java]].

**Other senses (if asked).**

- **Ad hoc:** different bodies for different **compile-time** types—**overloading** (`draw(Circle)` vs `draw(Square)`), or operators on `int` vs `double`.
- **Parametric:** one body for many type arguments—**generics** (`List.add`). Erasure: still one class at run time.
- **Subtype / inclusion:** the Java OOP default, above.

A **polymorphic variable** is a supertype reference that may denote subtype instances (`AbstractPhone phone = new VideoPhone(...)`).

```d2
direction: down
v: "phone : AbstractPhone" {
  width: 220
  height: 36
  style.fill: "#e3f2fd"
}
a: "ThomasEdisonPhone.call" {
  width: 240
  height: 36
  style.fill: "#fff8e1"
}
b: "VideoPhone.call" {
  width: 200
  height: 36
  style.fill: "#e8f5e9"
}
v -> a: "phone.call"
v -> b: "or"
```

**Fig. 1.** One compile-time type. The run-time class supplies `call`.

```java
abstract class Phone {
    abstract void call(int n);
}

class Landline extends Phone {
    @Override
    void call(int n) {}
}

class User {
    void callOther(int n, Phone phone) {
        phone.call(n);
    }
}

class Use {
    static void go() {
        User u = new User();
        Phone p = new Landline();
        u.callOther(1, p);
    }
}
```

**Listing 1.** `callOther` is written against `Phone`. `p`’s run-time class chooses `call`. Adding another `extends Phone` does not change `User`.

> [!warning] The compiler does not pick the overriding body
> Overload = compile-time signature from argument types. Override = run-time body for that signature. Mixing them is the dump’s first paragraph.

> [!warning] Overloading is not “OOP polymorphism” in a Java interview
> `void f(Phone p)` vs `void f(Landline l)`: `Phone x = new Landline(); f(x);` calls `f(Phone)`. You need an **overridden instance method** on the object.

> [!warning] Same interface is a type, not a Java `interface` only
> An `abstract class` or a superclass works the same. A public-field struct with no methods is not polymorphism.

> [!tip] Interview answer
> Polymorphism is using objects through a shared type while each class provides its own method body. In Java that is overriding and virtual dispatch: the compiler checks the supertype, the JVM runs the subclass method. Overloading is a different, compile-time mechanism. Generics are parametric polymorphism and still use overriding for instance calls.
