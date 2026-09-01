<!--
reps: 0
priority: 0
-->
#Java/Language/Modifiers/Static #Java/Versions/8 #Java/OOP/Interfaces #SRS

# How do default interface methods differ from static interface methods?

> [!abstract] Short answer
> A **`default` method is an instance method** with a body: implementing classes **inherit** it and may **override** it; you call it on an instance (`s.size()`), or `I.super.size()` from an implementor. A **`static` interface method is a class method**: it is **not inherited** by classes or subinterfaces, has **no** `this`, and is invoked as **`I.method()`** only — not `Impl.method()` and not `s.method()`. Both have bodies; you cannot combine `default` and `static` on one method. Both arrived as **public** interface methods in **Java 8**. Default: [[How would you explain default interface methods since Java 8]]. Static: [[How would you explain static methods in Java]]. Kinds: [[What kinds of methods can a Java interface declare]].

## Instance contract vs namespaced helper

`default` provides a **fallback implementation** for classes that `implements` the interface and do not override the method. It is inherited as a `public` instance member (unless the class already has a concrete method with that signature). Overriding is ordinary instance override. An overridden default is reached with a **qualified `super`**: `I.super.m()`. Invocation from an implementor: [[How do you invoke a default interface method from an implementing class]]. Two inherited defaults with the same signature **conflict** until the class or subinterface redeclares one.

`static` methods are **invoked without a particular object**. The declaration is a **static context**: no `this` / `super`, no unqualified instance members. Subinterfaces and implementing classes **do not inherit** them. `TypeName.m()` must name the interface (or a class) that **declares** the method. `ExpressionName.m()` / `primary.m()` is a compile-time error when the compile-time declaration is a **static method of an interface**. Class `static` methods are also not overridden ([[Can static methods be overridden in Java]]); interface `static` methods go further: they never appear on the class at all.

Implicitly `public` unless `private` (Java 9). `private` + `static` is legal; `private` + `default` is not. `abstract`, `default`, and `static` are pairwise exclusive. Helpers: [[Can a Java interface declare private methods]]. Omitting modifiers: [[How would you explain default modifiers for fields and methods inside interfaces]].

```d2
direction: down
call: "how do you call it?" {
  width: 220
  height: 40
  style.fill: "#e3f2fd"
}
d: "default\ninstance: s.m() / I.super.m()\ninherited, overridable" {
  width: 300
  height: 55
  style.fill: "#e8f5e9"
}
s: "static\nI.m() only\nnot inherited" {
  width: 300
  height: 55
  style.fill: "#fff3e0"
}
call -> d
call -> s
```

**Fig. 1.** Default methods participate in instance dispatch. Static interface methods stay on the interface name.

```java
interface Seq {
    default int size() {
        return 0;
    }

    static Seq empty() {
        return new Seq() {};
    }

    // default static int bad() { return 0; } // compile-time error
}

class A implements Seq {
    @Override
    public int size() {
        return 1;
    }

    int both() {
        return Seq.super.size() + size(); // 0 + 1
    }
}

class Use {
    static void go(Seq s, A a) {
        s.size();
        a.size();
        Seq.empty();
        // A.empty(); // compile-time error: not inherited
        // s.empty(); // compile-time error: static method of an interface
    }
}
```

**Listing 1.** `size` is inherited and overridden. `empty` exists only as `Seq.empty()`.

| | `default` | `static` |
| Kind | Instance method | Class method |
| Inherited by implementors / subinterfaces | Yes | No |
| Override | Yes (`@Override`) | No — not even present on the class |
| Call | `s.m()`, `I.super.m()` | `I.m()` |
| `this` in the body | Yes | No |
| Diamond of two bodies | Compile-time conflict | Cannot arise by inheritance |

> [!warning] `Impl.staticMeth()` looks like a class static call and does not compile
> Classes do not inherit `static` methods from superinterfaces. Use the **interface** name. `instance.staticMeth()` is also illegal for an interface `static` method, even though the same form is allowed (and discouraged) for a class `static` method.

> [!warning] `default` cannot redeclare `Object` methods
> A default method must not be override-equivalent with a non-`private` method of `Object` (`equals`, `hashCode`, `toString`, …). Class `Object` would always win. `static` helpers with those names are a different signature story; do not try to “default” `equals`.

> [!warning] `default static` is not a thing
> One method cannot be both. Need a shared helper with no instance? `static` (or `private static` since 9). Need a mixin body that uses `this`? `default`.

> [!tip] Interview answer
> Default interface methods are public instance methods with a body, inherited and overridable, called on an instance or via I.super. Static interface methods are helpers with no this, not inherited by classes or subinterfaces, and called only as I.method(). Both have had bodies since Java 8; they cannot be combined on one declaration. Use default to evolve an interface; use static for factories and utilities that must not join the instance API.
