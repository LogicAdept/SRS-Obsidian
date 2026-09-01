<!--
reps: 0
priority: 0
-->
#Java/Language #Java/Versions/8 #Java/Versions/9 #Java/OOP/Interfaces #SRS

# What kinds of methods can a Java interface declare?

> [!abstract] Short answer
> An interface may declare **abstract** instance methods (implicit if no `default`/`static`/`private`), **`default`** instance methods with a body (Java 8), **`static`** methods with a body (Java 8), and **`private`** methods with a body—instance or `static` (Java 9). There is **no constructor** ([[Can a Java interface declare a constructor]]). `default` vs `static`: [[How do default interface methods differ from static interface methods]]. Private: [[Can a Java interface declare private methods]]. vs abstract class: [[What is the difference between a Java interface and an abstract class]].

## Four method shapes

**Abstract.** No `private`, `default`, or `static` → implicitly `public abstract`, body `;`. `abstract`/`public` may be written redundantly. Implementors must provide an instance method (or inherit a `default`). Cannot be `protected`, package-private, `final`, `synchronized`, or `native`.

**`default` (Java 8).** `public` instance method with a **block**. Inherited by implementing classes unless overridden. Call `m()` or `I.super.m()` ([[How do you invoke a default interface method from an implementing class]]). Cannot be a `default` override of `Object`’s `equals` / `hashCode` / `toString`. Details: [[How would you explain default interface methods since Java 8]].

**`static` (Java 8).** Called as `I.m()`, **not** inherited as an instance method, **not** overridden. Implicitly `public` unless `private`. Static context: no `this`. Not `abstract` ([[Can a method be abstract and static at the same time]]).

**`private` (Java 9).** Must have a body. Instance `private` is for sharing code among `default` methods; not inherited. `private static` is for sharing among `static` (and other) methods in the interface. Not `abstract` or `default`.

**Not methods of the interface type.** Constructors. Nested types in an interface are implicitly `public static` members, not instance methods.

```d2
direction: down
abs: "abstract\npublic, ;" {
  width: 160
  height: 36
  style.fill: "#e3f2fd"
}
def: "default\npublic, block, inherited" {
  width: 240
  height: 40
  style.fill: "#e8f5e9"
}
st: "static\nI.m(), not inherited" {
  width: 220
  height: 40
  style.fill: "#fff8e1"
}
pr: "private\nbody, nest-only, Java 9" {
  width: 260
  height: 40
  style.fill: "#f3e5f5"
}
```

**Fig. 1.** Abstract, default, and static (8). Private helpers (9). No `protected` methods.

```java
interface Counter {
    int step();

    default int twice() {
        return helper() + step();
    }

    static int zero() {
        return Counter.hid() - 2;
    }

    private int helper() {
        return 1;
    }

    private static int hid() {
        return 2;
    }
}

class One implements Counter {
    @Override
    public int step() {
        return 10;
    }
}
```

**Listing 1.** `step` is abstract. `twice` is `default` and uses `private helper`. `zero` is `static` and uses `private static hid`. `new One().twice()` is `11`. `Counter.zero()` is `0`.

> [!warning] Implicitly abstract is the pre-Java-8 shape
> `void m();` is enough. `default void m();` or `static void m();` without a body is a compile-time error. `private void m();` is illegal for the same reason.

> [!warning] No `protected` / package / `final` / `native` / `synchronized`
> Access is `public` or `private` only. `abstract` cannot combine with `default` or `static`. `private` cannot combine with `abstract` or `default`.

> [!warning] `static` is not a `default` you forgot to inherit
> `C.m()` does not find `I.m()` as an instance method of `C`. Classes do not inherit interface `static` methods. `private` methods never appear on the implementing class.

> [!tip] Interview answer
> Interfaces declare public abstract methods, and since Java 8 also default instance methods and static methods with bodies. Since Java 9 they may declare private methods with bodies to share code. There are no constructors, and you cannot use protected, package-private, final, native, or synchronized on interface methods. Abstract methods have a semicolon; the others have a block.
