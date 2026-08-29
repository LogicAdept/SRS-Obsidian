<!--
reps: 0
priority: 0
-->
#Java/Exceptions/Hierarchy #SRS

# Is `Throwable` a class or an interface?

> [!abstract] Short answer
> **A class.** `java.lang.Throwable` is a concrete class (`extends Object`, `implements Serializable`). Its usual direct subclasses are `Exception` and `Error`. Only instances of `Throwable` or a subclass may be thrown or caught. It is not an interface.

## Class at the root of the exception tree

An exception is an instance of the **class** `Throwable` or one of its subclasses. `Exception` and `Error` are the two usual direct subclasses ([[What is the difference between Throwable and Exception]], [[What is java.lang.Error]], [[Why is Error a sibling of Exception rather than a subclass]]).

A `throw` expression and a `catch` parameter must be that class or a subclass. You cannot throw an arbitrary object, and you cannot declare `catch` on a type outside that tree ([[Can you throw an object that is not a Throwable]], [[Can you catch Throwable]]).

`Throwable` itself is a checked exception class. Application types are still normally declared under `Exception` (or `RuntimeException`), not as direct children of `Throwable` ([[Is Throwable a checked exception]], [[Do checked exceptions inherit Throwable directly]]).

```d2
direction: down
obj: "Object" {
  width: 200
  height: 50
  style.fill: "#eceff1"
}
t: "class Throwable\nimplements Serializable" {
  width: 280
  height: 70
  style.fill: "#e8f5e9"
}
ex: "class Exception" {
  width: 220
  height: 50
  style.fill: "#e3f2fd"
}
err: "class Error" {
  width: 200
  height: 50
  style.fill: "#fff8e1"
}
obj -> t
t -> ex
t -> err
```

**Fig. 1.** `Throwable` is a class. `Serializable` is the interface it implements, not a substitute for the type itself.

```java
class Demo {
    static void run() {
        Throwable t = new Throwable("demo");
        try {
            throw t;
        } catch (Throwable caught) {
            System.out.println(caught.getClass().getName());
        }
    }
}
```

**Listing 1.** `new Throwable()` compiles: the type is a instantiable class, not `abstract` and not `interface`. A `Throwable` carries a message, stack trace, and optional cause ([[What information does a Throwable carry]]).

> [!warning] Interview dumps call it “the throwable interface”
> That confuses the *role* (“anything you can throw”) with the *declaration*. The type in `java.lang` is `public class Throwable`. The interface on it is `Serializable`.

> [!warning] Instantiable does not mean you should throw raw `Throwable`
> `new Throwable()` is legal. New application failures should almost always be a subclass of `Exception` or `RuntimeException`, so callers can use `catch (Exception)` without catching `Error` ([[Are Error subclasses checked or unchecked]]).

> [!tip] Interview answer
> **`Throwable` is a class, not an interface.** It extends `Object` and implements `Serializable`. `Exception` and `Error` extend it, and only those instances can be thrown or caught.
