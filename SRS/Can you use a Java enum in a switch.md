<!--
reps: 0
priority: 0
-->
#Java/Language/Enum #SRS

# Can you use a Java enum in a `switch`?

> [!abstract] Short answer
> **Yes.** An enum type is a legal selector. Each `case` label is the **name** of a constant of that enum (`case DIME`), matched with `==`. A classic `switch` **statement** on an enum need not list every constant; a `switch` **expression** must be exhaustive (all names, or `default`).

## How the labels work

`case` constants are either a constant expression (`int` / `String` / …) **or** the name of an enum constant. For an enum selector, the compiler checks that each name is assignment-compatible with that enum type. At run time the label applies if the selector is `==` to that constant — identity, which is the right equality for enums.

`String` selectors arrived in Java 7; enum selectors came with enums themselves (Java 5). Do not `switch` on `ordinal()` to fake an `int` switch ([[What does ordinal do on a Java enum]]).

```d2
direction: down
sel: "switch (coin)" {
  width: 200
  height: 50
  style.fill: "#e3f2fd"
}
cases: "case PENNY, NICKEL, …\nnames, matched with ==" {
  width: 280
  height: 70
  style.fill: "#e8f5e9"
}
alt: "constant-specific methods\nwhen the enum owns the behavior" {
  width: 280
  height: 70
  style.fill: "#fff3e0"
}

sel -> cases
sel -> alt
```

**Fig. 1.** A `switch` is how *outside* code branches on constants. Behavior that belongs on the type is better as methods on those constants.

```java
enum Currency { PENNY, NICKEL, DIME, QUARTER }

void describe(Currency coin) {
    switch (coin) {
        case PENNY:
            System.out.println("1 cent");
            break;
        case NICKEL:
            System.out.println("5 cents");
            break;
        case DIME, QUARTER:
            System.out.println("silver");
            break;
        default:
            throw new AssertionError("unknown coin: " + coin);
    }
}
```

**Listing 1.** Classic statement: unqualified constant names, `break` to avoid fall-through, `default` as a belt for future constants.

```java
int cents(Currency coin) {
    return switch (coin) {
        case PENNY   -> 1;
        case NICKEL  -> 5;
        case DIME    -> 10;
        case QUARTER -> 25;
    };
}
```

**Listing 2.** A `switch` expression must be exhaustive. Listing every constant makes `default` optional. Arrow form does not fall through.

A non-enhanced `switch` **statement** on an enum (no `case null`, no patterns) is **not** required to be exhaustive. Missing `C` in `enum { A, B, C }` compiles; that value just does nothing — a silent bug. `switch` expressions, and enhanced statements, must cover the type or include `default`. If a new constant is added in a later class file, an exhaustive `switch` compiled against the old list can fail at run time ([[Can you add constants to a Java enum at runtime]]).

`null` as the selector: with no `case null`, a `switch` statement throws `NullPointerException`.

## When not to `switch`

If every constant should carry its own behavior, put a method on the enum (abstract + class bodies, or `implements`) instead of a growing `switch` outside ([[Can a Java enum have abstract methods]], [[Can a Java enum implement an interface]]). A `switch` is the right tool when the branching is not yours to add to the type — the JLS even uses that “add a method from outside” pattern.

> [!warning] Incomplete classic `switch` statements fail open
> `switch (e) { case A -> …; case B -> …; }` is legal on an enum and does **nothing** for `C`. A `switch` expression with the same holes does not compile. Prefer covering all names, or `default` that fails loudly.

> [!warning] Do not `switch` on `ordinal()`
> `case 0` / `case 1` tracks source order, not names. Inserting a constant in the middle silently remaps every later `case`. Switch on the enum value and name the constants.

> [!tip] Interview answer
> **Yes — you can `switch` on an enum, and the `case` labels are the constant names, compared with `==`.** A statement need not be exhaustive, which is a bug magnet; a `switch` expression must list every constant or `default`. For behavior the enum should own, use methods on the constants instead of a large external `switch`.
