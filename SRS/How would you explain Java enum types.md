<!--
reps: 0
priority: 0
-->
#Java/Language/Enum #SRS

> [!abstract] Short answer
> **A Java enum is a class with a fixed set of named instances — the constants listed in the declaration.** It is a real type (`enum Coin { PENNY, NICKEL }`), not a pile of `int` or `String` fields. Only those instances exist; the compiler gives you `values()` and `valueOf`, and the type may still have fields, constructors, methods, and interfaces.

## A restricted class, not glorified integers

An `enum` declaration defines an enum class whose superclass is `java.lang.Enum` ([[Can a Java enum extend a class]]). Each constant is a `public static final` field of that type, created when the class is initialized ([[When is a Java enum constructor invoked]]). There are no other instances: `new` is a compile-time error, clone and reflective construction are blocked, and serialization reconstitutes by name ([[Can you create a Java enum instance with new]], [[How does Java serialization treat enum constants]]).

That closed instance set is the language form of the old typesafe-enum idea. `int` / `String` constant patterns cannot stop `99` or `"nickle"` ([[What is the advantage of a Java enum over int and String constant patterns]]). The feature arrived in Java 5 ([[In which Java version were enums introduced]]).

Because it is a class, an enum can take constructor arguments, hold per-constant data, declare methods (including abstract methods implemented on constant bodies), and `implements` interfaces ([[Can you declare a constructor inside a Java enum]], [[Can a Java enum have abstract methods]], [[Can a Java enum implement an interface]]). `switch` works on the constants ([[Can you use a Java enum in a switch]]). `name()` is the identifier; `toString()` is overridable display ([[What is the difference between name and toString on a Java enum]]). `ordinal()` / `compareTo` follow declaration order and are `final` ([[What does ordinal do on a Java enum]]).

Special collections match the finite universe: `EnumSet` (bits) and `EnumMap` (array of values) ([[What special collections exist for Java enums]]). When the alternatives are *kinds with different state*, not singletons, a sealed hierarchy is the better model ([[When would you use a sealed class instead of an enum]]). `java.util.Enumeration` is an unrelated 1.0 cursor ([[What is the difference between enum Enum and Enumeration]]).

```d2
direction: down
decl: "enum Coin { PENNY, NICKEL, … }" {
  width: 300
  height: 50
  style.fill: "#e3f2fd"
}
cls: "class Coin extends Enum<Coin>\nfixed instances, methods, fields" {
  width: 340
  height: 70
  style.fill: "#e8f5e9"
}
use: "switch, values(), EnumSet / EnumMap" {
  width: 300
  height: 50
  style.fill: "#fff3e0"
}

decl -> cls -> use
```

**Fig. 1.** Syntax lists names. The runtime thing is a class with those objects and no others.

```java
enum Coin {
    PENNY(1), NICKEL(5), DIME(10), QUARTER(25);
    private final int cents;
    Coin(int cents) { this.cents = cents; }
    int cents() { return cents; }
}

class Demo {
    static int nickel() {
        return Coin.NICKEL.cents();
        // Coin.values() is PENNY, NICKEL, DIME, QUARTER
        // new Coin(1) does not compile
    }
}
```

**Listing 1.** Named instances, shared type, per-constant data. That is the explanation in one type.

> [!warning] Do not explain enums as “named ints”
> C-style enums are integers. Java enums are objects of a closed class. `ordinal()` is an index for `EnumMap`/`EnumSet`, not the value you persist ([[What does ordinal do on a Java enum]]).

> [!warning] `enum`, `Enum`, and `Enumeration` are three words
> The keyword declares the type. `java.lang.Enum` is the superclass. `java.util.Enumeration` walks a `Vector`. Mixing them is the fastest way to fail the follow-up.

> [!tip] Interview answer
> **An enum type is a class that lists its only instances by name.** Those constants are `public static final`, created at class initialization; you cannot `new` more. The type can have data and behavior, works in `switch`, and pairs with `EnumSet`/`EnumMap`. Prefer it over `int`/`String` constants whenever the set of values is known at compile time.
