<!--
reps: 0
priority: 0
-->
#Java/OOP/Constructors #Java/Language/Modifiers/Access #SRS

# Where and how you can you use constructor?

> [!abstract] Short answer
> The dump is **`private` constructors**. `private` is **access**, not hiding: only code in the **same nest** (the class and its nested types) may call it. Typical callers are a **`public static` factory** (`return new C(...)`), **`this(...)`** from another constructor of `C`, instance methods of `C`, and **nested classes**. Outside the nest, `new C(...)` and `super(...)` do not compile. Patterns: [[How would you explain private constructors and common patterns that use them in Java]]. Constructors: [[What is constructor]]. Nest: [[How can a nested class access fields of its enclosing class]].

## Who may write `new` / `this(...)`

A constructor is invoked by a **class instance creation** (`new`), by **`this(...)` / `super(...)`**, and by a few implicit conversions. Access follows the same modifiers as other members: `public`, `protected`, package, `private`.

**Same class.** A static factory, a static method, an instance method, and another constructor’s `this(...)` may all call a `private` constructor. The dump’s “public static generation method” is the usual factory. It is not the only legal caller.

**Nested types.** A nested class or interface in the same top-level type may call that constructor, including a `static` nested class. The dump is right that nested types have access. They are not limited to “inner-only.”

**Outside.** Other top-level types cannot. A subclass **outside the nest** cannot run `super(...)` to a `private` superclass constructor, so you cannot extend the class from the outside if every constructor is `private`. Declaring any constructor also drops the implicit default one.

```d2
direction: down
nest: "nest: C, nested types" {
  width: 280
  height: 40
  style.fill: "#e8f5e9"
}
out: "other top-level types" {
  width: 280
  height: 40
  style.fill: "#ffebee"
}
nest -> factory: "static factory, this(), nested new"
out -> blocked: "new / super — compile error"
```

**Fig. 1.** `private` constructor: nest may construct; everyone else may not, at compile time.

```java
class Box {
    private final int n;

    private Box(int n) {
        this.n = n;
    }

    private Box() {
        this(0);
    }

    static Box empty() {
        return new Box();
    }

    static class Nested {
        static Box zero() {
            return new Box(0);
        }
    }
}
```

**Listing 1.** `empty()` and `Nested.zero()` call the `private` constructors. `this(0)` is another in-class use. `new Box()` from a different top-level class would not compile.

> [!warning] “Hidden” is the wrong word
> Constructors are **not members** and are never inherited, so they are not hidden. `private` only restricts **who may invoke** them. Nested access is nest-wide, not a special inner-class privilege.

> [!warning] Reflection still exists
> `Constructor.setAccessible` can invoke a `private` constructor at run time ([[How do you invoke a private constructor using reflection]]). That does not make `new` legal in source outside the nest. Do not treat a private constructor as a security boundary.

> [!warning] All-private is the instantiation lock
> One unused `private` no-arg constructor, and no other constructors, is the usual **utility-class** shape. If any constructor is package-accessible or wider, outside code can still `new` or subclass.

> [!tip] Interview answer
> A private constructor is for code in the same class and its nested types. You use it from a static factory, from `this()` in another constructor, and from nested classes that need to build an instance. Callers outside the nest cannot write `new` or `super` to it. That is how factories, utility types, and hand-rolled singletons keep construction in one place.
