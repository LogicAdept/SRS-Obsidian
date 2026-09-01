<!--
reps: 0
priority: 0
-->
#Java/Language/Modifiers/Abstract #Java/Language/Modifiers/Static #Java/OOP #SRS

# Can a method be abstract and static at the same time?

> [!abstract] Short answer
> **No.** `abstract` and `static` on the same method is a compile-time error, in a class and in an interface. `abstract` is an **instance** method with no body that a concrete subclass **must override**. `static` is a **class** method with no `this`, invoked without an object. Those contracts cannot hold together. `abstract`: [[How would you explain the abstract keyword in Java]]. `static`: [[How would you explain static methods in Java]]. Instance vs class members: [[What is the difference between an instance member and a static member in Java]].

## Override demand vs class method

An `abstract` method introduces signature, result, and `throws`, and **no implementation**. Its body is a semicolon. It must sit in an `abstract` class (or an enum) unless it is an interface method. Every **non-`abstract` subclass** must provide an instance method that implements it.

A `static` method is a class method. It is always invoked without a particular object. Its declaration is a static context: no `this` / `super`, no unqualified instance members. Subclasses do not **override** class methods; at most they **hide** them. A `static` method cannot hide an instance method.

So `abstract static void m();` asks for an implementation via override **and** forbids instance dispatch. The modifier list makes that a compile-time error, together with `abstract` plus `private`, `final`, `native`, `strictfp`, or `synchronized`.

```d2
direction: down
abs: "abstract\ninstance, no body\nsubclass must override" {
  width: 240
  height: 70
  style.fill: "#e3f2fd"
}
st: "static\nclass method, no this\nhide, not override" {
  width: 240
  height: 70
  style.fill: "#fff3e0"
}
bad: "abstract static\ncompile-time error" {
  width: 220
  height: 50
  style.fill: "#ffcdd2"
}
abs -> bad
st -> bad
```

**Fig. 1.** One modifier requires instance override; the other has no instance. The pair is illegal.

```java
abstract class Named {
    abstract String name();          // legal: instance, no body

    static Named missing() {         // legal: class method with a body
        return new Named() {
            @Override
            String name() {
                return "none";
            }
        };
    }
}

class Person extends Named {
    @Override
    String name() {
        return "p";
    }
}
```

**Listing 1.** An abstract **class** may declare abstract instance methods and concrete `static` methods. The combination is on **one method**, not on the class.

```java
// Conceptual: does not compile
abstract class Named {
    abstract static String name();
}

interface AlsoNamed {
    abstract static String name();   // abstract, default, static: pick one
    static String name();            // static still needs a block body
}
```

**Listing 2.** Conceptual. On an interface, `abstract`, `default`, and `static` are mutually exclusive. A `static` interface method has a block body and is not inherited: [[How would you explain static methods on Java interfaces]].

javac reports an illegal combination of modifiers for `abstract` and `static` (same family of diagnostic as `abstract`+`private` or `abstract`+`final`). Do not memorize punctuation of one compiler build; the language rule is the compile-time error.

Interface methods that omit `private`, `default`, and `static` are already implicitly `abstract`. Writing `static` on those is the same conflict, not a new Java 8 exception. `final` is also illegal on every interface method: [[Why can an interface method not be declared final in Java]].

> [!warning] An abstract **class** may still have `static` methods
> `abstract class Foo { static void helper() {} }` is legal. The ban is `abstract` **and** `static` on the **same method**. A static factory on an abstract class is a normal pattern.

> [!warning] `static` methods are not “implemented by subclasses”
> A subclass `static` method with the same signature **hides** the superclass class method. The compile-time type of the qualifier chooses which one runs. That is not the abstract-method contract. Hiding vs override: [[Can static method be override or]].

> [!warning] Other `abstract` pairs fail for the same reason
> `abstract` also cannot be `private` (not inherited, cannot be overridden), `final` (cannot be overridden), `native`, `strictfp`, or `synchronized`. `abstract` plus a method body is a separate error.

> [!tip] Interview answer
> No. Abstract means an instance method with no body that a concrete subclass must override; static means a class method with no current object and no override. The combination is a compile-time error on classes and on interfaces. An abstract class can still declare ordinary static helpers; those methods are not abstract.
