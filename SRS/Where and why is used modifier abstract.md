<!--
reps: 0
priority: 0
-->
#Java/Language/Modifiers/Abstract #Java/OOP #SRS

# Where and why is used modifier abstract?

> [!abstract] Short answer
> Write **`abstract`** on a **class** that is incomplete (you must not `new` it) and on an **instance method** that has **no body** — a hole a concrete subclass must fill. A class that declares or inherits an unimplemented abstract method must itself be `abstract`. **Why:** share fields and concrete methods among related types while forcing each subclass to supply the parts that differ. Interfaces are already abstract; their non-`default`, non-`static`, non-`private` methods are already abstract. Meaning of the keyword: [[How would you explain the abstract keyword in Java]]. Opposite lock: [[What does the final keyword mean in Java]]. Interface members: [[How would you explain default modifiers for fields and methods inside interfaces]].

## Where you may write it

| Construct | `abstract`? |
| --- | --- |
| Class | yes — cannot be instantiated; may have zero or more abstract methods |
| Instance method | yes — no body; class must be `abstract` |
| Interface | redundant — the interface is already `abstract` |
| Interface instance method (not `default` / `static` / `private`) | redundant — already `abstract` |
| Constructor, field, `static` method | **illegal** |
| `final` / `private` method | **illegal** with `abstract` |
| `final` class | **illegal** with `abstract` |

An `abstract` class may still have constructors (for subclasses), instance state, concrete methods, and `static` members. `AbstractType.staticMethod()` does not instantiate it.

A concrete subclass must implement every abstract method it inherits. If it does not, it stays `abstract`. An `abstract` class may implement an interface only in part; the rest waits for a further subclass.

## Why you use it

Use an abstract class when closely related types share **code and state**, including non-`public` methods and non-`static` fields, but some operations **must differ** in each subclass (`draw`, `resize`). That is a template: common `moveTo`, required `draw`.

Prefer an **interface** when unrelated types should share a contract, you need multiple supertypes, or you do not need instance fields. Prefer a **concrete class with a private constructor** when the type is complete and you only want to block `new` (utility classes). `abstract` is not that tool.

```java
abstract class Graphic {
    int x, y;
    void moveTo(int x, int y) { this.x = x; this.y = y; }
    abstract void draw();
}

class Circle extends Graphic {
    void draw() { /* ... */ }
}
```

**Listing 1.** `moveTo` is shared. `draw` is the hole. `new Graphic()` does not compile; `new Circle()` does.

```d2
direction: down
where: "abstract on..." {
  width: 160
  height: 36
  style.fill: "#fff8e1"
}
cls: "class\n(no new)" {
  width: 140
  height: 48
  style.fill: "#e3f2fd"
}
meth: "instance method\n(no body)" {
  width: 160
  height: 48
  style.fill: "#e8f5e9"
}
why: "share code, force\nsubclass to fill holes" {
  width: 200
  height: 48
  style.fill: "#fff3e0"
}
where -> cls
where -> meth
cls -> why
meth -> why
```

**Fig. 1.** Where: class or instance method. Why: incomplete related types, not “cannot construct.”

> [!warning] `abstract` is not a utility-class lock
> `Math` is not abstract; it uses a private constructor. An abstract class still has a type you subclass and a constructor subclasses can call. If the class is complete, do not mark it `abstract` only to forbid `new`.

> [!warning] One abstract method makes the class abstract
> Leaving the class concrete is a compile error. `abstract` + `final` on the same class or method is also illegal: one demands subclasses, the other forbids them.

> [!tip] Interview answer
> Use `abstract` on a class you must not instantiate and on instance methods with no body so subclasses supply the missing behavior while inheriting shared code. A class with any abstract method must be abstract. Do not put `abstract` on constructors, fields, or static methods, and do not use it to hide a finished utility type — use a private constructor instead.
