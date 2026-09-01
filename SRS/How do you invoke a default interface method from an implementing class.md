<!--
reps: 0
priority: 0
-->
#Java/Versions/8 #Java/OOP/Interfaces #SRS

# How do you invoke a default interface method from an implementing class?

> [!abstract] Short answer
> If the class **does not override** it, call it like any instance method: `show()` or `this.show()`. If the class **does override** it, the inherited body is reached with **`Interface.super.show()`** — the interface name plus `super`, not a bare `super.show()`. `I` must be a **direct** superinterface of the class (or interface) that contains the call. Defaults: [[How would you explain default interface methods since Java 8]]. vs `static`: [[How do default interface methods differ from static interface methods]]. Class `super.m()`: [[How do you call an overridden superclass method in Java]].

## `m()` vs `I.super.m()`

A `default` method is a **public instance** method with a body. An implementing class **inherits** it unless it declares an override-equivalent instance method. Unqualified `show()` is then **virtual**: you get the class override if there is one.

To invoke the **interface** declaration you overrode, the form is `TypeName.super.show(...)`. `TypeName` names that **direct superinterface**. Unqualified `super.show()` searches only the **direct superclass** (`Object` unless you `extends` something else) and will not find the default.

You cannot skip a more specific interface: if `Glossy extends Paper` and both are in play, `Paper.super.show()` is illegal when `Glossy` already overrides `show`. Call `Glossy.super.show()`. There is **no** syntax for `Enclosing.Interface.super.m()` from a nested class; a `private` helper on the enclosing class that does `I.super.m()` is the workaround.

`I.m()` is for **`static`** interface methods, not defaults. Kinds: [[What kinds of methods can a Java interface declare]].

```d2
direction: down
need: "run the interface default from a class" {
  width: 320
  height: 40
  style.fill: "#e3f2fd"
}
plain: "not overridden\nshow() / this.show()" {
  width: 280
  height: 50
  style.fill: "#e8f5e9"
}
qual: "overridden\nPaper.super.show()" {
  width: 280
  height: 50
  style.fill: "#fff8e1"
}
need -> plain
need -> qual
```

**Fig. 1.** Inherited default: ordinary instance call. Overridden default: qualified `Interface.super`.

```java
interface Paper {
    default void show() {
        System.out.println("paper");
    }
}

interface Glossy extends Paper {
    @Override
    default void show() {
        System.out.println("glossy");
    }
}

class Licence implements Paper {
    @Override
    public void show() {
        Paper.super.show();
        System.out.println("licence");
    }
}

class Card implements Glossy {
    @Override
    public void show() {
        Glossy.super.show();
        // Paper.super.show(); // compile-time error: not a direct superinterface,
        // or skipped by Glossy's override
    }
}

class Silent implements Paper {
    void demo() {
        show(); // Paper's default — no override
    }
}
```

**Listing 1.** `Licence` and `Card` re-enter the default with `I.super.show()`. `Silent` just calls `show()`. `Card` must use `Glossy`, not `Paper`.

> [!warning] `super.show()` is not `Paper.super.show()`
> Bare `super` is the **superclass**. A class that only `implements Paper` has superclass `Object`. `Object` has no `show`. Always qualify with the **interface** name.

> [!warning] `I` must be a **direct** superinterface of the current type
> `implements Glossy` does not let you write `Paper.super.show()` to skip `Glossy`. If a direct superinterface already overrides the default, that override blocks the grandparent form. Re-implement `Paper` as a **direct** superinterface only if you mean both to be direct — and the skip-override rule may still forbid `Paper.super`.

> [!warning] Nested classes cannot write `Outer.Paper.super.show()`
> That combination is illegal. Put a `private` method on `Outer` that calls `Paper.super.show()`, and invoke that helper from the nested type.

> [!tip] Interview answer
> From an implementing class, call an inherited default method as a normal instance method. After you override it, invoke the interface body with Interface.super.method(), where Interface is a direct superinterface. Unqualified super looks at the superclass, not the interface. Static interface methods are Interface.method(), never Interface.super.
