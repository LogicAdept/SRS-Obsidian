<!--
reps: 0
priority: 0
-->
#Java/OOP #Java/Language/NestedClasses #Java/Language/Enum #Java/Language/Records #SRS

# Which kinds of classes exist in Java?

> [!abstract] Short answer
> **Three declaration kinds: normal class, `enum`, and `record`.** Independently, a class is **top-level** or **nested** (member, local, or anonymous). **Inner** vs **`static` nested** is about an enclosing instance, not a third placement. `abstract` / `sealed` / `final` are **modifiers**. An **interface** is a type, not a class.

## Declaration kind is not the same as placement

A class declaration is one of **normal**, **enum**, or **record**. An enum is a class with a fixed set of named instances; a record is a class for a simple aggregate of values. Either may be top-level, member, or local. An enum constant’s `{ ... }` is still an **anonymous** class.

**Top-level** means declared directly in a compilation unit (`public` or package-private; not `private` / `protected` / `static`). **Nested** means declared in the body of another class or interface ([[How would you explain categories of Java classes such as nested and anonymous]]):

```d2
direction: down
decl: "Class declaration" {
  width: 220
  height: 40
}
kind: "Kind: normal / enum / record" {
  width: 280
  height: 50
  style.fill: "#e3f2fd"
}
place: "Place: top-level or nested" {
  width: 280
  height: 50
  style.fill: "#fff3e0"
}
mem: "Member\n(static nested or inner)" {
  width: 260
  height: 55
  style.fill: "#e8f5e9"
}
loc: "Local\n(in a block)" {
  width: 220
  height: 50
  style.fill: "#e8f5e9"
}
anon: "Anonymous\n(new Type() { })" {
  width: 260
  height: 55
  style.fill: "#ffebee"
}
decl -> kind
decl -> place
place -> mem
place -> loc
place -> anon
```

**Fig. 1.** Dump lists that put `enum` beside `nested`, or `abstract` only under top-level, collapse two axes into one tree.

**Inner** = nested and not (explicitly or implicitly) `static`. That is a non-`static` **member** class, a local **normal** class, or an **anonymous** class. Implicitly `static` (not inner): nested enum/record, member class of an interface ([[How would you explain static nested classes in Java]], [[How would you explain nested classes in Java and when to use each kind]]).

`abstract`, `sealed`, and `final` control completeness and subclassing. They apply to **normal** classes (with the usual restrictions) whether top-level or nested. They are not extra “types of class” next to nested. An anonymous class from `new` is never `final`; one from an enum constant **is** `final`.

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

enum Mode { FAST, SLOW }

record Point(int x, int y) { }

abstract class Shape {
    abstract void draw();
}

final class Unit { }
```

**Listing 1.** `Outer` is a top-level normal class. `Nested` / `Inner` / `Local` / the `Runnable` are the three nested shapes. `Mode` and `Point` are the other two **declaration** kinds. `Shape` and `Unit` are modifier variants of a normal class, not a separate placement.

A local **enum** or **record** is nested but **not** inner. A local **normal** class is inner ([[How would you explain local classes in Java and their scoping rules]], [[What are anonymous classes and where are they used]]).

> [!warning] An interface is not a class
> Interview dumps file `interface` under “types of classes.” A class declaration and an interface declaration are different type declarations. Nested interfaces exist; they are still interfaces, and they are implicitly `static`.

> [!warning] Abstract/final are not “kinds of top-level class”
> A nested class may be `abstract` or `final`. A top-level class need be neither. `sealed` (Java SE 17) belongs on this modifier axis, not under nested.

> [!warning] “Local inner” / “anonymous inner” are usually inner, not always the whole nested story
> Anonymous classes are always inner. A **local enum/record** is nested and implicitly `static`. Static nested is nested and **not** inner.

> [!tip] Interview answer
> **Classes come in three declarations — normal, enum, record — and two places — top-level or nested (member, local, anonymous).** Inner means nested and not static: inner member, local normal class, anonymous class. **Interfaces are not classes. Abstract and final are modifiers, not extra kinds.**
