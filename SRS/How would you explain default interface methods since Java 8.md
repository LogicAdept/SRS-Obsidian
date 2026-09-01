<!--
reps: 0
priority: 0
-->
#Java/OOP/Interfaces #Java/Language #Java/Versions/8 #SRS

# How would you explain default interface methods since Java 8?

> [!abstract] Short answer
> **A `default` method is an interface instance method with a body.** Classes that implement the interface **inherit that body** unless they override it. The point is **evolution**: you can add methods to an existing interface (`Collection.stream`, `List.sort`, `Map.forEach`) without forcing every implementor to recompile a new abstract method. They are not class methods, not `static`, and they cannot redeclare `Object`’s methods.

## Instance fallback, not a second superclass

A default method is declared with the `default` modifier and a **block** body. Interface methods are implicitly `public`. You cannot mark the same method `abstract` and `default`, or `static` and `default`. A method with neither `default` nor `static` is abstract (semicolon body) ([[How do default interface methods differ from static interface methods]], [[Why can an interface method not be declared final in Java]]).

A non-abstract class may skip the default and inherit it, or override it. To call the interface body from the class, use `InterfaceName.super.method(...)` ([[How do you invoke a default interface method from an implementing class]]). A **concrete method from a superclass** already overrides a matching interface default — the class does not inherit the default at all.

Java 8 used this to grow the collections APIs with lambda-friendly methods while remaining binary-compatible: `Collection.stream()` / `parallelStream()` / `removeIf` / `spliterator` are default methods `@since 1.8`. `List.sort` and the Java 8 `Map` defaults are the same story ([[Which new Map methods were added in Java 8]], [[Which functional interface does Iterable forEach use]]).

```d2
direction: down
pre: "Java 7 interface\nonly abstract instance methods" {
  width: 300
  height: 60
  style.fill: "#fff3e0"
}
v8: "Java 8 default + static\nbody on the interface" {
  width: 300
  height: 60
  style.fill: "#e8f5e9"
}
jdk: "Collection.stream, List.sort,\nMap.forEach, Iterable.forEach" {
  width: 320
  height: 60
  style.fill: "#e3f2fd"
}

pre -> v8: "add without breaking implementors"
v8 -> jdk
```

**Fig. 1.** Defaults exist so libraries can add instance behavior. `static` interface methods are the “put helpers on the interface” feature, a different modifier.

```java
interface Example {
    int process(int a);

    default void show() {
        System.out.println("default show()");
    }
}

class Impl implements Example {
    @Override
    public int process(int a) {
        return a;
    }
    // show() inherited
}

interface A {
    default void m() { }
}

interface B {
    default void m() { }
}

class Clash implements A, B {
    @Override
    public void m() {
        A.super.m();
    }
}
```

**Listing 1.** `Impl` compiles without writing `show`. `Clash` does **not** compile without an override: two inherited defaults with the same signature. `A.super.m()` picks one. `default boolean equals(Object o)` is illegal — it is override-equivalent with `Object.equals`.

Two interfaces, one `default m()` and one `abstract m()`, are the same class of conflict for a concrete class: you must override. (An `abstract` method declared **in a superclass** is a special case that makes the defaults act abstract.) A subinterface that inherits two matching defaults must also declare `m` itself.

> [!warning] Two defaults (or default + abstract) is a compile error, not a silent pick
> The compiler does not prefer the “first” interface. Override in the class or in a subinterface. Class concrete methods already win over defaults; that can hide a library default you thought you inherited.

> [!warning] No `default` `equals` / `hashCode` / `toString`
> A default method must not be override-equivalent with a non-private `Object` method. Every class already has those from `Object`, and a default would never be the one you call. Put extra formatting on a differently named method.

> [!tip] Interview answer
> **Java 8 default methods are public instance methods on an interface with a body, so old implementors keep compiling when the interface grows.** You inherit the body unless you override it or a superclass already provides a concrete method. Conflicts of two defaults — or default versus abstract from another interface — must be overridden; you cannot default `Object`’s methods. That is why `stream()` and the Java 8 `Map` methods could be added as defaults.
