<!--
reps: 0
priority: 0
-->
#Java/Language/Modifiers/Static #Java/OOP/Interfaces #SRS

# How would you explain static methods on Java interfaces?

> [!abstract] Short answer
> They are **class methods declared on the interface type**: invoked **without** an object, with a block body, in a **static context** (no `this` / `super`). They are **not** `default` methods, **not** inherited by implementing classes or by subinterfaces, and **not** overridden. Helpers and factories live next to the type instead of a separate `FooUtils` class. Call site: [[How do you invoke a static method on a Java interface]]. Versus class `static`: [[How would you explain static methods in Java]]. Versus `default`: [[How would you explain default interface methods since Java 8]].

## Helpers on the type, not on instances

An interface may declare `static` methods. Those are distinct from `abstract` methods, `default` methods, and non-`static` `private` methods, which are all **instance** methods. `static` cannot be paired with `abstract` or `default`. No access modifier means implicit **`public`**; **`private static`** is allowed and is callable only from the declaring interface. `protected` and package access are illegal. Implied modifiers: [[How would you explain default modifiers for fields and methods inside interfaces]].

A class does **not** inherit `private` or `static` methods from its superinterface types. An interface does **not** inherit `static` methods from its superinterfaces. So `static` on an interface is not a member you acquire by `implements` or `extends`. A `static` method also cannot hide a `public` instance method of a superinterface, and an interface cannot declare a method override-equivalent to a `public` method of `Object` unless that method is `abstract`.

`InterfaceName.super.m()` is for **default** methods. Class methods use `InterfaceName.m()` (or a static import). An expression qualifier (`p.m()`) is a compile-time error when `m` is `static` **and declared in an interface** — unlike `static` methods of a class.

```java
interface Id {
    int value();

    static Id of(int n) {
        return () -> n;
    }

    static int requireNonNegative(int n) {
        if (n < 0) {
            throw new IllegalArgumentException();
        }
        return n;
    }

    default boolean nonNegative() {
        return value() >= 0;
    }
}

class UsesId implements Id {
    public int value() { return 1; }

    void demo() {
        Id x = Id.of(Id.requireNonNegative(2));
        boolean ok = x.nonNegative();
        // Id.of is not UsesId.of
        // this.of(3) is illegal
    }
}
```

**Listing 1.** `of` / `requireNonNegative` are class methods of `Id`. `nonNegative` is a `default` instance method. `implements Id` does not import the static names.

```d2
direction: down
iface: "interface Id" {
  width: 160
  height: 36
  style.fill: "#fff8e1"
}
st: "static of / requireNonNegative\n(not inherited)" {
  width: 260
  height: 48
  style.fill: "#e8f5e9"
}
def: "default nonNegative()\n(instance, overridable)" {
  width: 260
  height: 48
  style.fill: "#e3f2fd"
}
cls: "class implements Id" {
  width: 200
  height: 40
  style.fill: "#ffcdd2"
}
iface -> st
iface -> def
iface -> cls: "does not inherit static"
cls -> def: "may inherit / override"
```

**Fig. 1.** `static` stays on the interface type. `default` participates in instance inheritance.

> [!warning] Not “default methods with static”
> `default` is an instance method with a body that implementing classes inherit. `static` has no receiver, is not inherited, and cannot be overridden. Putting both keywords on one method is a compile-time error.

> [!warning] `implements` does not give you `Impl.staticName()`
> Copying a same-signature `static` method onto the class creates a **different** method. It does not override or hide the interface’s class method — the class never inherited that method. Use `Id.of(...)`.

> [!tip] Interview answer
> Static methods on an interface are class methods of that interface: helpers and factories with no this. Implementing classes and subinterfaces do not inherit them, so you call InterfaceName.method. They are not default methods and they are not overridden. Private static is allowed as an implementation detail of the interface itself.
