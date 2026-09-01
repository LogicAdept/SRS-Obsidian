<!--
reps: 0
priority: 0
-->
#Java/Language/Assert #SRS

# When is it appropriate to use Java assertions?

> [!abstract] Short answer
> **For internal invariants you believe always hold: nonpublic preconditions, postconditions, class invariants, and “this line is unreachable.”** Do not use `assert` to enforce a public contract (`IllegalArgumentException` / `NullPointerException` instead), to validate `main`’s arguments, or to do work the program needs when assertions are off.

## What they are for

Assertions are typically on during development and test and off in deployment ([[Why are Java assertions disabled by default]], [[How do you enable Java assertions at runtime]]). A disabled `assert` is a no-op, so they must not be required control flow ([[Why must Java assert expressions be free of side effects]]).

**Use them** when you would otherwise write a comment that a condition is always true:

- **Nonpublic preconditions** — a helper that clients cannot call wrongly if they only use the public API ([[Why should you not use assert to validate public method arguments]]).
- **Postconditions** — in public or nonpublic methods, after the real work, to check the result.
- **Class invariants** — e.g. `assert balanced();` before a public method returns.
- **Control-flow invariants** — `assert false;` (optionally `: detail`) on a `switch` `default` you believe is unreachable, or after a loop that must have returned.

**Do not use them** to check **public** arguments (including `public static void main(String[] args)`). That contract must hold without `-ea`, and a failure should be `IllegalArgumentException` / `NullPointerException` / `IndexOutOfBoundsException`, not `AssertionError`. Do not put `names.remove(null)` inside `assert`: when asserts are off, the removal never happens.

```d2
direction: down
q: "Is this a published contract\nor required work?" {
  width: 300
  height: 70
  style.fill: "#e3f2fd"
}
no: "internal invariant\nassert" {
  width: 240
  height: 70
  style.fill: "#e8f5e9"
}
yes: "public args / must-run logic\nif + throw, not assert" {
  width: 300
  height: 70
  style.fill: "#ffebee"
}
q -> no
q -> yes
```

**Fig. 1.** `assert` documents an internal “this cannot happen.” Public contracts and required actions stay in ordinary code.

```java
class Demo {
    private void helper(int interval) {
        assert interval > 0 : interval;
        // ...
    }

    static Suit suitFrom(int n) {
        switch (n) {
            case 0: return Suit.CLUBS;
            case 1: return Suit.DIAMONDS;
            case 2: return Suit.HEARTS;
            case 3: return Suit.SPADES;
            default:
                throw new AssertionError(n);
        }
    }

    enum Suit { CLUBS, DIAMONDS, HEARTS, SPADES }
}
```

**Listing 1.** Nonpublic precondition via `assert`. The `switch` uses `throw new AssertionError` so an impossible `n` is still reported when assertions are disabled. `assert false` in `default` would fire only with `-ea`.

> [!warning] `assert false` in `default` is not a production trap
> If assertions are off, `default: assert false;` does nothing and execution falls through. Where the method must not return normally, `throw new AssertionError(...)` is the form that still runs. `assert false` is also a compile-time error if the compiler already knows the statement is unreachable.

> [!warning] `main` is a public method
> `assert args.length > 0` is the public-argument mistake. Parse and throw (or print usage) whether or not `-ea` was passed.

> [!tip] Interview answer
> **Use assertions for internal “this must be true” checks — private preconditions, postconditions, invariants, unreachable code.** Do not use them for public arguments, command-line validation, or any work the program still needs when asserts are off. They are off by default, so they are not a substitute for throwing the documented exception.
