<!--
reps: 0
priority: 0
-->
#Java/Language/Enum #SRS

> [!abstract] Short answer
> **An `enum` is a dedicated type whose only values are the named constants.** `public static final int` / `String` fields are still just `int` and `String`: any number or any text compiles, names collide unless you prefix them, and those literals are inlined into callers. The language `enum` fixes that and is still a class: constructors, fields, methods, interfaces, `switch` ([[In which Java version were enums introduced]], [[How would you explain Java enum types]]).

## What the old patterns cannot check

A method `int cents(int coin)` accepts `99`. A method `int cents(String coin)` accepts `"nickle"`. Neither is a coin type. The int pattern also lets you add two “seasons.” The compiler has no universe to enforce.

Those fields have **no namespace of their own**. Two int “enums” both want a `PENNY = 1`, so you write `COIN_PENNY` and `STAMP_PENNY`. An enum constant is `Coin.PENNY` — the type *is* the namespace. `import static` can shorten the name; it does not restore a type.

`static final int` / `String` fields initialized with literals are compile-time constant variables. Callers bake the number or text into their class files. Insert a value in the middle, or change `1` to `2`, and old binaries keep running with the **old** number. Enum constants are objects, not inlined ints. Adding or reordering constants is binary-compatible for clients that used the names ([[Can you add constants to a Java enum at runtime]]). Printing an int yields `1`; printing `Coin.PENNY` yields a name ([[Can you override toString on a Java enum]]).

```d2
direction: down
bad: "int / String parameter\n99 and \"dime\" both compile" {
  width: 300
  height: 70
  style.fill: "#ffebee"
}
good: "enum Coin { PENNY, NICKEL, DIME }\nonly those constants type-check" {
  width: 320
  height: 70
  style.fill: "#e8f5e9"
}

bad -> good: "language enum"
```

**Fig. 1.** The win is a closed type, not prettier names for the same `int`.

```java
class IntCoins {
    static final int PENNY = 1;
    static final int NICKEL = 5;
    static int cents(int coin) { return coin; }
}

enum Coin {
    PENNY(1), NICKEL(5), DIME(10);
    private final int cents;
    Coin(int cents) { this.cents = cents; }
    int cents() { return cents; }
}

class Demo {
    static int demo() {
        int oops = IntCoins.cents(99); // compiles
        return Coin.NICKEL.cents() + oops;
        // Coin.cents(99) does not exist
    }
}
```

**Listing 1.** The int helper cannot reject `99`. `Coin` can carry `cents` on the constant ([[Can you declare a constructor inside a Java enum]]).

The hand-rolled “typesafe enum” class (private constructor, `public static final` instances) already had a real type, but it was verbose and those instances were not `switch` cases. A language enum is that pattern in the language: closed instance set, `values()` / `valueOf`, `switch` ([[Can you use a Java enum in a switch]]), interfaces ([[Can a Java enum implement an interface]]), plus `EnumSet` / `EnumMap` ([[What is EnumSet]]). Serialization stores the constant **name**, not an int code ([[How does Java serialization treat enum constants]]).

> [!warning] `ordinal()` is the int pattern coming back
> Persisting or switching on `ordinal()` reintroduces inlined-code brittleness: insert a constant and every later number moves ([[What does ordinal do on a Java enum]]). Keep a field you own (`cents`, a wire code) if the outside world needs a number. Keep `valueOf` at a String boundary ([[How do you convert a String to a Java enum]]).

> [!warning] Static import does not make `int` typesafe
> `PENNY` as a bare name is still an `int`. `Coin.PENNY` is a `Coin`. Prefer the type in signatures even when the name is imported.

> [!tip] Interview answer
> **Prefer a language `enum` over `public static final int` or `String` constants because it is a type: only declared constants compile, names live on that type, and callers are not stuck with inlined literals.** It is still a class, so constants can hold data and methods, implement interfaces, and be `switch`ed on. Do not smuggle the old int codes back in through `ordinal()`.
