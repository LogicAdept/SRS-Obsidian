<!--
reps: 0
priority: 0
-->
#Java/Language/Enum #SRS

# Can a Java enum have abstract methods?

> [!abstract] Short answer
> **Yes — in the enum body, not as a modifier on the type.** You may declare an `abstract` method as a member of the enum if there is at least one constant and **every** constant has a class body that implements it. You cannot write `abstract enum`. That exception exists because an enum is not an `abstract` class: without constant bodies it is implicitly `final`; with them it is implicitly `sealed`.

## The rule

An `abstract` method normally has to live in an `abstract` class. Enum declarations are the exception: the method may be declared in the enum, and each constant’s anonymous class is then a concrete subclass that must supply the body.

You still cannot put `abstract`, `final`, `sealed`, or `non-sealed` on the enum declaration itself. The compiler chooses `final` vs `sealed` from whether any constant has a class body ([[Can a Java enum extend a class]]).

```d2
direction: down
e: "enum Op\nabstract int apply(...)" {
  width: 260
  height: 80
  style.fill: "#e3f2fd"
}
plus: "PLUS { apply = a+b }" {
  width: 220
  height: 60
  style.fill: "#e8f5e9"
}
minus: "MINUS { apply = a-b }" {
  width: 240
  height: 60
  style.fill: "#e8f5e9"
}
call: "Op x = Op.PLUS\nx.apply(1, 2)" {
  width: 260
  height: 70
  style.fill: "#fff3e0"
}

e -> plus
e -> minus
plus -> call
minus -> call
```

**Fig. 1.** The abstract method is a member of the enum type, so you can call it on any `Op`. Each constant’s class body is the implementation.

```java
enum Op {
    PLUS {
        int apply(int a, int b) { return a + b; }
    },
    MINUS {
        int apply(int a, int b) { return a - b; }
    };

    abstract int apply(int a, int b);
}

int n = Op.PLUS.apply(2, 3); // 5
```

**Listing 1.** Legal pattern: every constant has a class body; the enum declares `abstract int apply`. Adding a new constant without a body is a compile-time error — safer than a `switch` you can forget to update.

The same obligation applies if the abstract method is a member because the enum implements an interface and does not provide a concrete method in the enum body. Constant class bodies then implement the interface method ([[Can a Java enum implement an interface]]). That is not a substitute for declaring the method on the enum when you want a method that is *not* on an interface.

## What does not compile

```java
// abstract enum Wrong { A, B }   // cannot mark the enum type abstract

enum MissingBodies {
    A, B;
    abstract int apply(int a, int b); // error: constants have no class bodies
}

enum Partial {
    ADD {
        int apply(int a, int b) { return a + b; }
    },
    MUL; // error: this constant has no class body
    abstract int apply(int a, int b);
}

enum Empty {
    ;
    abstract int apply(int a, int b); // error: no enum constants at all
}
```

**Listing 2.** Conceptual: the four ways people miss the rule — `abstract` on the type, no constant bodies, one constant without a body, empty enum.

A constant’s own class body also cannot declare a new `abstract` method. Those anonymous classes are `final`. Extra per-constant methods that do **not** override something accessible on the enum cannot be called through an `Op` reference.

```java
enum Color {
    RED {
        String hex() { return "#ff0000"; } // does not override anything on Color
    },
    GREEN {
        String hex() { return "#00ff00"; }
    };
}

// Color.RED.hex(); // does not compile: hex() is not a member of Color
```

**Listing 3.** Constant-only methods are not part of the enum API. If callers need `hex()`, declare it on `Color` (`abstract` or a default implementation the constants override).

> [!warning] “Enums are final, so no abstract methods” is the wrong half of the rule
> With no constant class bodies the enum *is* implicitly `final`, and then an `abstract` member is illegal. The moment every constant has a body, the enum is implicitly `sealed`, not a user-written `abstract` class, and abstract methods are allowed. The type still must not be declared `abstract`.

> [!warning] One missing `{ … }` rejects the whole enum
> `PLUS { … }, MINUS;` plus `abstract int apply(...)` does not compile. Every constant is a subclass that must implement the method. The same trap appears when you add a constant later and forget the class body.

> [!tip] Interview answer
> **Yes: an enum may declare abstract methods, but only if every constant has a class body that implements them.** You cannot write `abstract enum`. Without those bodies the enum is implicitly final, so the abstract method would have nowhere to live. Callers see the method on the enum type; methods that exist only inside one constant’s braces are not part of that type.
