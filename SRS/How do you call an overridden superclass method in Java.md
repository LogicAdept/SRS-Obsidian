<!--
reps: 0
priority: 0
-->
#Java/OOP/Polymorphism #SRS

# How do you call an overridden superclass method in Java?

> [!abstract] Short answer
> Use **`super.method(...)`** in an **instance** context of the subclass. That form searches the **direct superclass** and uses **non-virtual** invocation: the superclass method runs, even if a further subclass also overrides it. A **cast** `((Super) this).method()` is still **virtual** and hits the override. For a default method, use **`Interface.super.method()`**. From an inner class, **`Enclosing.super.method()`** targets the enclosing instance’s superclass. Overriding: [[How would you explain method overriding in Java]]. Superclass calls in general: [[How do you call superclass methods from a subclass in Java]]. Defaults: [[How do you invoke a default interface method from an implementing class]].

## `super.m()` is not a cast

`this.m()` and `obj.m()` use **virtual** lookup from the **run-time class** of the target. `super.m()` does not: the invocation mode is **`super`**, **overriding is not allowed**, and the method found in the **direct superclass type** is the one invoked (`this` is still the subclass object). Overload vs override: [[How would you explain Overload vs Override]].

You cannot write `super.super.m()` or `Grandparent.super.m()` to skip the immediate superclass. `TypeName.super.m()` means either (i) the **superclass of a lexically enclosing class** `TypeName`, or (ii) a **direct superinterface** default (or other instance method) of the current type — not “any ancestor class.”

`super(...)` at the start of a constructor is an **explicit constructor invocation**, not a method call. Constructors are not overridden ([[Can you override a constructor the same way you override a method]]). `static` methods are not overridden ([[Can static methods be overridden in Java]]); call them as `Super.staticMeth()`, not as an override hook.

`super.m()` is illegal in a **static context**, on `Object`, and as unqualified `super` in an **interface**. It is illegal if the chosen method is `abstract`.

```d2
direction: down
call: "want Super.m on this object" {
  width: 260
  height: 40
  style.fill: "#e3f2fd"
}
ok: "super.m()\nnon-virtual, direct superclass" {
  width: 280
  height: 50
  style.fill: "#e8f5e9"
}
bad: "((Super) this).m()\nstill virtual → override" {
  width: 280
  height: 50
  style.fill: "#fff3e0"
}
call -> ok
call -> bad
```

**Fig. 1.** Only `super.m()` bypasses the override. A superclass cast does not.

```java
class Point {
    void clear() {
        System.out.println("Point");
    }
}

class ColoredPoint extends Point {
    @Override
    void clear() {
        super.clear(); // Point.clear
        System.out.println("color");
    }

    void stillVirtual() {
        ((Point) this).clear(); // ColoredPoint.clear again
    }
}

interface Named {
    default String name() {
        return "unnamed";
    }
}

class Person implements Named {
    @Override
    public String name() {
        return Named.super.name() + "/person";
    }
}

class Outer extends Point {
    @Override
    void clear() {
        System.out.println("Outer");
    }

    class Nested {
        void reset() {
            Outer.super.clear(); // Point.clear on the enclosing Outer
        }
    }
}
```

**Listing 1.** `super.clear()` is the superclass body. `((Point) this).clear()` is not. `Named.super.name()` is a direct superinterface. `Outer.super.clear()` is the enclosing class’s **superclass**, not a superinterface of `Nested`.

> [!warning] `((Super) this).m()` still dispatches to the override
> The cast only changes the **compile-time** type. Run-time lookup starts at the actual class. That is why `super` exists.

> [!warning] There is no `super.super`
> `super.m()` is the **immediate** superclass (or, with `I.super`, a **direct** superinterface). To reuse a grandparent implementation, the middle class must expose it, or you duplicate the logic. `Outer.super.m()` is **not** “call `m` on type Outer as superclass of this nested class” unless `Outer` is an enclosing class.

> [!warning] `super()` is not `super.m()`
> `super()` / `super(args)` runs a **constructor**. It must be the first statement in the constructor (aside from prologue rules). It does not call an overridden method named after the superclass.

> [!tip] Interview answer
> Call an overridden superclass method with super.method(...) from an instance method or constructor of the subclass; that invocation is not virtual. Casting this to the superclass still calls the override. For a default method use Interface.super.method(), and from an inner class use Enclosing.super.method() to reach that enclosing type’s superclass. You cannot skip a generation with super.super.
