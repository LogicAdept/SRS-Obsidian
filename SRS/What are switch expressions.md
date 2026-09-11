<!--
reps: 0
priority: 0
-->
#Java/Versions/14 #SRS

# What are switch expressions

> [!abstract] Short answer
> **A `switch` expression (final in Java 14, JEP 361; previewed 12–13) yields a value: arrow labels `case X ->` run without fall-through, a block yields with `yield`, and the compiler enforces exhaustiveness — every path must produce a value or throw.** Selector typing stays classic for constants; patterns in `case` labels are the separate, later feature (final in 21). `switch` still works as a statement — the expression form is additive ([[What is the difference between pattern matching and a switch statement]]).

## Arrow labels, yield, exhaustiveness

The arrow form runs exactly the right-hand side — no fall-through, no accidental case bleed. The right side is an expression, a `throw`, or a block whose value is `yield n;` (a keyword introduced for this; `return` is illegal inside an `switch` expression's block, and `break value` from the early previews was dropped). When the `switch` is used as an **expression**, the compiler requires exhaustiveness: a `default`, or for an `enum` selector, coverage of every constant — which makes adding a constant a compile error at every non-default site, a feature, not an annoyance. Colon-form `case:` labels are still legal inside a switch expression, but then fall-through rules apply as before and `yield` is the value keyword.

`case null` is **not** allowed in a plain switch expression — `null` selector throws `NullPointerException`; null-tolerant label matching arrived with pattern `switch` in 21 ([[How do records work with pattern matching in switch]]).

```d2
direction: down
sel: "switch (x) used as a value" {
  width: 300
  height: 55
  style.fill: "#e3f2fd"
}
arr: "case A, B -> expr\nno fall-through" {
  width: 280
  height: 55
  style.fill: "#e8f5e9"
}
blk: "case C -> { ... yield v; }" {
  width: 300
  height: 55
  style.fill: "#e8f5e9"
}
exh: "must be exhaustive:\ndefault, or all enum constants" {
  width: 380
  height: 60
  style.fill: "#fff8e1"
}
sel -> arr
sel -> blk
arr -> exh
blk -> exh
```

**Fig. 1.** An expression switch must produce exactly one value per path; the compiler holds you to exhaustiveness instead of hoping `default` was there.

```java
enum Day { MON, TUE, OTHER }

public class V18_SwitchExpressions {
    static int numLetters(Day d) {
        return switch (d) {
            case MON, TUE -> 3;
            case OTHER -> {
                int n = 5;          // block needs yield, not return
                yield n;
            }
        };                          // exhaustive: no default needed for a covered enum
    }

    static int classify(Object o) { // default required when not exhaustive
        return switch (o.getClass().getSimpleName()) {
            case "String" -> 6;
            default -> 0;
        };
    }

    public static void main(String[] args) {
        System.out.println("numLetters(MON): " + numLetters(Day.MON));
        System.out.println("numLetters(OTHER): " + numLetters(Day.OTHER));
        System.out.println("classify: " + classify("s"));
    }
}
```

**Listing 1.** Verified on JDK 21 (V18_SwitchExpressions in empirics): `numLetters(MON): 3`, `numLetters(OTHER): 5`, `classify: 6` — multi-constant arrow labels, `yield` from a block, and enum exhaustiveness without `default` (out/V18_SwitchExpressions.txt).

> [!warning] yield is not return — and exhaustiveness has a catch
> Three traps: `yield` leaves the switch expression; `return` inside it tries to leave the enclosing **method** and does not compile at all inside the expression's block. Second, exhaustiveness without `default` compiles only for covered enums or (with patterns, 21+) sealed selector types — cover one constant and add a new one later, and every non-default switch site becomes a compile error; that is by design, but teams discover it in CI. Third, mixing colon cases with arrow cases in one switch is illegal, and a colon case in an expression switch still falls through ([[What are text blocks]]-era Java 14+ code must keep this straight).

> [!tip] Interview answer
> **Switch expressions, final in 14, make switch produce a value: arrow labels with no fall-through, `yield` for block results, compiler-enforced exhaustiveness — an enum switch without default fails to compile when a constant is added.** Previewed in 12–13; `case null` belongs to pattern switch in 21, not here.
