<!--
reps: 0
priority: 0
-->
#Java/Language/Modifiers/Access #Java/Versions/9 #Java/OOP/Interfaces #SRS

# Can a Java interface declare private methods?

> [!abstract] Short answer
> **Yes, since Java 9.** An interface method may be **`private`** or **`private static`**. It must have a **block body**. It is **not** inherited by implementing classes or by subinterfaces, and it cannot be `abstract` or `default`. The point is code sharing among `default` / `static` methods on the same interface. Omitted access is still **`public`**, not private. Method kinds: [[What kinds of methods can a Java interface declare]]. Fields stay public constants: [[Can a Java interface declare private fields or variables]].

## Helpers on this interface only

A method in an interface may be declared `public` or `private`. No access modifier means implicit `public`. `protected` and package access are illegal. `private` cannot be combined with `abstract` or `default`. `private static` is legal. `private`, `default`, and `static` methods have a block body; a semicolon body is a compile-time error.

A private interface method is neither inherited nor overridden. A class that `implements` the interface does not acquire it. A subinterface does not inherit it. Only `public` interface methods can be overridden, and only by `public` methods.

If the interface declares a `private` or `static` method whose signature is a subsignature of a `public` instance method in a superinterface (and that method would be accessible), that is a compile-time error: the private method cannot override or hide that instance method.

```d2
direction: down
iface: "interface I" {
  width: 160
  height: 40
  style.fill: "#e3f2fd"
}
priv: "private / private static\nblock body, same interface" {
  width: 260
  height: 55
  style.fill: "#e8f5e9"
}
def: "default / static methods\nmay call it" {
  width: 240
  height: 55
  style.fill: "#fff3e0"
}
impl: "implements I / extends I\ndoes not inherit it" {
  width: 240
  height: 55
  style.fill: "#ffcdd2"
}
iface -> priv
priv -> def: "call"
priv -> impl: "not a member"
```

**Fig. 1.** Private methods exist for helpers inside the declaring interface. Implementors never see them.

```java
interface Named {
    String name();

    private String padded() {
        return "[" + name() + "]";
    }

    default String label() {
        return padded();
    }

    private static String none() {
        return "none";
    }

    static Named missing() {
        return () -> none();
    }
}

class Person implements Named {
    @Override
    public String name() {
        return "p";
    }
}
```

**Listing 1.** `label()` and `missing()` share private helpers. `Person` implements `name()` and inherits `label()`, not `padded()` or `none()`.

```java
// Conceptual: does not compile
interface Named {
    private String a();                      // no body
    private abstract String b();             // private + abstract
    private default String c() { return ""; } // private + default
    protected void d();                      // protected illegal
    void e() { }                             // implicit abstract, but has a body
}

class Outsider implements Named {
    String x = padded();  // even on Listing 1's Named: not inherited
}
```

**Listing 2.** Conceptual. Private methods need a block, cannot be `abstract`/`default`/`protected`, and are not members of the implementor.

## Java 9, call sites, and what is still public

Java 9 added private interface methods so non-abstract methods can share code without putting helpers on a public API or a separate utility type. Java 8 already had `default` and `static` methods; those stayed `public` unless you write `private` on a Java 9+ compiler. `default` methods: [[How would you explain default interface methods since Java 8]]. Interface `static`: [[How would you explain static methods on Java interfaces]]. Implied modifiers: [[How would you explain default modifiers for fields and methods inside interfaces]].

A **private instance** method is an instance method. Call it from another instance method of the **same** interface (`default` or `private`). It is not a static context, so `this` is allowed. A **`private static`** method is a class method of the interface type: call `none()` from `static`, `default`, or `private` methods in that same interface. An implementing class does not write `Named.none()` or `this.padded()` — those members are not accessible there.

Annotation interfaces (`@interface`) cannot declare `private`, `default`, or `static` methods. Nested **classes** inside a normal interface may declare `private` methods of their own; those are class methods, not interface methods.

`final` is still illegal on every interface method, including private ones: [[Why can an interface method not be declared final in Java]]. Access catalog: [[How do Java access modifiers work]].

> [!warning] `private` is not the default, and it is not allowed on fields
> Write `private` explicitly. A bare `void m();` is still `public abstract`. Interface fields remain `public static final`; Java 9 did not add private fields.

> [!warning] Implementors cannot call or override the helper
> `class C implements I { public int m() { return helper(); } }` fails if `helper` is private on `I`. Expose a `default` method that calls the helper, or keep the helper `private static` and call it only from interface methods.

> [!warning] `private default` is not a thing
> `default` means a public-or-implicitly-public instance method with a body that implementors **may** override. `private` means not inherited. Combining them is a compile-time error. Use `private` with a block, or `default` with a block, not both.

> [!tip] Interview answer
> Yes, since Java 9 an interface may declare private and private-static methods with a real body, so default and static methods can share code without publishing helpers. They are not inherited and cannot be abstract or default. Omitting the modifier still means public, and fields are still not allowed to be private.
