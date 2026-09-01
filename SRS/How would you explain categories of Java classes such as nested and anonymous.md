<!--
reps: 0
priority: 0
-->
#Java/OOP #Java/Language/NestedClasses #SRS

# How would you explain categories of Java classes such as nested and anonymous?

> [!abstract] Short answer
> **Split on where the class is declared, then on whether it is inner.** A **top-level** class sits directly in a compilation unit. Anything whose declaration is **inside another class or interface** is **nested**: a **member** class, a **local** class (in a block), or an **anonymous** class (`new Type() { }` or an enum constant body). **Inner** means nested and **not** `static` (explicitly or implicitly).

## Two axes: place, then inner vs static

A **top-level** class is declared directly in a compilation unit. It may be `public` or package-private. It cannot be `private`, `protected`, or `static`. Nested types exist to group a helper with its only client, keep `private` members of the outer type usable from that helper, and keep the code next to the use.

A **nested** class is any class whose declaration occurs **in the body of another class or interface**. That umbrella has three shapes ([[How would you explain nested classes in Java and when to use each kind]]):

```d2
direction: down
cls: "Class declaration" {
  width: 220
  height: 40
}
top: "Top-level\n(compilation unit)" {
  width: 240
  height: 55
  style.fill: "#e3f2fd"
}
nested: "Nested\n(inside a class or interface body)" {
  width: 280
  height: 55
  style.fill: "#fff3e0"
}
mem: "Member\n(static nested or inner)" {
  width: 260
  height: 55
  style.fill: "#e8f5e9"
}
loc: "Local\n(in a block; has a name)" {
  width: 260
  height: 55
  style.fill: "#e8f5e9"
}
anon: "Anonymous\n(new Type() { } / enum constant)" {
  width: 280
  height: 70
  style.fill: "#ffebee"
}
cls -> top
cls -> nested
nested -> mem
nested -> loc
nested -> anon
```

**Fig. 1.** Nested is the parent category. Anonymous is one nested shape, not a third kind beside “nested.”

- **Member class** — declared in the class body like a field. May be `public` / `protected` / package-private / `private`. May be `static` (no enclosing instance) or inner (`outer.new Inner()`) ([[How would you explain static nested classes in Java]], [[How do you from class get access to field outer class]]).
- **Local class** — declared in a **block** (method, constructor, initializer). It has a **simple name**, is **not** a member of any type, and cannot be `public`, `protected`, `private`, `static`, `sealed`, or `non-sealed`. A local **normal** class is inner. A local **enum** or **record** is implicitly `static`, so **not** inner ([[How would you explain local classes in Java and their scoping rules]]).
- **Anonymous class** — declared by `new Type(...) { ... }` or by an enum constant’s `{ ... }`. No name, implicit constructor, always inner ([[What are anonymous classes and where are they used]]).

**Inner** is not a fourth placement. It is a nested class that is not explicitly or implicitly `static`: a non-`static` member class, a local normal class, or an anonymous class. Implicitly `static` (hence **not** inner): member/local enum, member/local record, and a member class of an **interface**. Nested interfaces are all implicitly `static`; there are no “inner interfaces.”

```java
class Outer {
    static class Nested { }

    class Inner { }

    void method() {
        class Local { }

        Runnable once = new Runnable() {
            @Override
            public void run() { }
        };
        once.run();
    }
}
```

**Listing 1.** `Outer` is top-level. `Nested` and `Inner` are member classes. `Local` is local. The `Runnable` is anonymous. `new Nested()` works in `Outer`; from another type it is `new Outer.Nested()`. `Inner` needs `outer.new Inner()`.

Enum and record classes are **kinds of class declaration**. Each may be top-level, member, or local; an enum constant’s body is still an anonymous class. Do not put them on a third axis next to “nested.”

> [!warning] Nested ≠ inner, and anonymous **is** nested
> Interview shorthand “inner vs nested” treats nested as meaning only `static` member classes. In the language, **nested = member + local + anonymous**; **inner ⊂ nested**. Saying “anonymous classes are not nested” is false.

> [!warning] “Every nested class is a member” is the JDK 8 tutorial’s slip
> Member classes are members. Local and anonymous classes are nested and **not** members of a package or type, which is why they cannot take `public` / `private`. A `static` nested class still may read `private` instance fields of `Outer` **if** you pass an `Outer` — “no access to outer members” is about **no enclosing instance**, not about `private`.

> [!warning] Local enum/record and `static` members of inner classes
> A local enum/record is nested but **not** inner. Since **Java SE 16** an inner class (including anonymous) may declare static members and static initializers; it still is not a `static` class.

> [!tip] Interview answer
> **Top-level vs nested is about where the class is written. Nested splits into member, local, and anonymous.** Inner means nested and not static — that includes inner member classes, local normal classes, and every anonymous class. **A static nested class is nested but not inner; a local enum is nested but not inner.**
