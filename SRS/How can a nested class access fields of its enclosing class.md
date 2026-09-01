<!--
reps: 0
priority: 0
-->
#Java/Language/NestedClasses #Java/Language/Modifiers/Access #Java/OOP #SRS

# How can a nested class access fields of its enclosing class?

> [!abstract] Short answer
> **By sitting in the enclosing type’s body**, so even `private` fields are in scope for access control. An **inner** class also holds an **enclosing instance**: an unqualified instance field uses that instance; disambiguate with `Outer.this.field`. A **`static` nested class has no enclosing instance**, so it cannot use an unqualified instance field — it can still read `private` members through an `Outer` **reference**, and it can use **class** fields of `Outer`. Kinds: [[How would you explain nested classes in Java and when to use each kind]]. Static nested: [[How would you explain static nested classes in Java]]. Private: [[How would you explain private]].

## Two checks: access, then an instance

A nested class is declared **inside** another class or interface. `private` members of that top-level type are accessible from **any** nested type in its body — inner, `static` nested, local, or anonymous. That is the same nest rule as two instances of one class: [[Can one object access another class private fields in Java]]. Access modifiers: [[How do Java access modifiers work]].

**Using** an instance field still needs an instance of the class that declares it.

- An **inner** class (member class that is not `static`, or a local/anonymous class not in a static context) is created with an **immediately enclosing instance**. A valid reference to an enclosing instance variable uses **that** enclosing instance. `this` is the inner object; `Outer.this` is the enclosing `Outer`.
- A **`static` nested class** has **no** enclosing instance (`new Outer.Nested()`, not `outer.new Nested()`). Unqualified `inst` is a compile-time error. `Outer.cls` or a parameter `outer.inst` is fine. `static`: [[What does the static keyword mean in Java]]. Constructors: [[Does a static nested class have a constructor in Java]].
- A local or anonymous class in a **static context** (for example a `static` method) likewise has no enclosing instance of `Outer`. It may capture **effectively final** locals; it must not assign a blank `final` field of `Outer`.

```d2
direction: down
outer: "Outer instance\ninst, cls" {
  width: 220
  height: 50
  style.fill: "#e3f2fd"
}
inner: "Inner instance\nOuter.this → Outer" {
  width: 260
  height: 50
  style.fill: "#e8f5e9"
}
nested: "static Nested\nno enclosing instance" {
  width: 260
  height: 50
  style.fill: "#fff3e0"
}
outer -> inner: "enclosing instance"
nested -> outer: "only if you pass Outer"
```

**Fig. 1.** Inner objects carry `Outer.this`. A `static` nested type is not attached; it reaches instance state only through a reference.

```java
class Outer {
    private int inst = 1;
    private static int cls = 2;

    class Inner {
        private int inst = 10; // shadows Outer.inst

        int enclosingInst() {
            return Outer.this.inst; // 1
        }

        int ownInst() {
            return this.inst; // 10
        }

        int classField() {
            return cls; // 2
        }
    }

    static class Nested {
        int viaRef(Outer o) {
            return o.inst + cls; // private instance + class field
        }

        // int bad() { return inst; } // compile-time error: no enclosing instance
    }

    int fromLocal() {
        int captured = 3; // effectively final
        class Local {
            int n() {
                return inst + captured;
            }
        }
        return new Local().n();
    }
}
```

**Listing 1.** Inner class: unqualified/`Outer.this` instance fields. `static` nested: `private` via an `Outer` reference, not via `Outer.this`. Local class: enclosing instance plus an effectively final local.

> [!warning] “Static nested classes cannot access enclosing members” is too tight
> They cannot use `Outer.this` or an **unqualified instance** field. They **can** use `static` fields of `Outer` and **any** `private` member given an `Outer` (or other) reference, because the nested type is still in `Outer`’s body.

> [!warning] Same simple name as the inner class hides the outer field
> `inst` inside `Inner` is `Inner`’s field. The enclosing instance field is `Outer.this.inst`. Forgetting the qualifier is a logic bug, not an access error.

> [!warning] Static context cuts off `Outer`’s instance
> A local class in a `static` method cannot read `Outer`’s instance fields. Locals it does capture must be `final` or effectively final. An inner class must not assign a blank `final` field of a lexically enclosing class.

> [!tip] Interview answer
> Nested types can access private fields of the enclosing top-level class because they are declared in its body. An inner class also has an enclosing instance, so unqualified instance fields (or Outer.this.field when names clash) read that object. A static nested class has no enclosing instance: pass an Outer if you need instance state, and use class fields directly. Local classes in instance methods capture the enclosing object plus effectively final locals.
