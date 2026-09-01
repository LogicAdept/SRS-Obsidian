<!--
reps: 0
priority: 0
-->
#Java/Language/Switch #Paradigms/Functional #SRS

# What is the difference between pattern matching and a `switch` statement?

> [!abstract] Short answer
> **They are different kinds of construct.** Pattern matching is the run-time test of a value against a pattern; on success it initializes pattern variables. A `switch` statement is multi-way control transfer. Classic `switch` matches constants with `==` or `String.equals` and does **not** pattern-match. From Java 21 a `switch` *may* host patterns in `case` labels; `instanceof` has hosted them since Java 16.

## Pattern matching is a process, not a statement

A pattern is a test plus zero or more pattern variables. Pattern matching checks a value against that pattern. If it succeeds, those variables are initialized and are in scope only where the match is guaranteed. That process is distinct from executing a statement or evaluating an expression.

A **type pattern** (`String s`) asks whether the value is an instance of that type and binds it. A **record pattern** (`Point(int x, int y)`) also deconstructs components ([[How do records work with pattern matching in switch]]). The null reference does not match a top-level type pattern or a record pattern.

The first host in the language was `instanceof` (Java 16): `obj instanceof String s` replaces `instanceof` plus a cast ([[What is the instanceof operator for in Java]]).

## A `switch` statement is multi-way dispatch

A `switch` chooses among labels for one selector ([[Can you use strings in a Java switch statement]], [[Can you use a Java enum in a switch]]). Until Java 21 the selector had to be an integral type except `long`, a matching wrapper, `String`, or an enum. Labels were **constants** (or `default`). Matching was `==`, except `String`, which uses `equals`. No pattern variables. A non-enhanced `switch` **statement** need not be exhaustive: a missed value does nothing. A `null` selector throws `NullPointerException`; `default` does not catch `null`.

That is equality dispatch, not pattern matching.

## Java 21 can put patterns *in* a `switch`

A `case` label may be a pattern (`case String s`, `case Point(int x, int y)`), optionally with a `when` guard. The selector may be any reference type. The label applies if pattern matching succeeds and the guard is true.

That `switch` is **enhanced** (a `case` pattern or `case null` is present, or the selector is not a classic type). Enhanced `switch` statements must be exhaustive, like `switch` expressions. Existing constant `switch` statements keep the old semantics.

```d2
direction: down
pm: "pattern matching\ntest + bind variables" {
  width: 280
  height: 70
  style.fill: "#e8f5e9"
}
inst: "instanceof (Java 16)\nobj instanceof String s" {
  width: 280
  height: 70
  style.fill: "#e3f2fd"
}
sw: "switch statement\nmulti-way labels" {
  width: 280
  height: 70
  style.fill: "#fff3e0"
}
classic: "classic: case constants\n== or String.equals" {
  width: 280
  height: 70
  style.fill: "#fff8e1"
}
pat: "Java 21: case patterns\nenhanced, exhaustive" {
  width: 280
  height: 70
  style.fill: "#e8f5e9"
}

pm -> inst
pm -> pat
sw -> classic
sw -> pat
```

**Fig. 1.** Pattern matching is the test-and-bind process. `switch` is the control statement. They meet only in enhanced `case` patterns.

```java
class Demo {
    static int classic(String s) {
        switch (s) {
            case "ok":
                return 1;
            default:
                return 0;
        }
    }

    static int typeTest(Object obj) {
        if (obj instanceof String s) {
            return s.length();
        }
        return 0;
    }

    static int patterned(Object obj) {
        return switch (obj) {
            case String s -> s.length();
            case Integer i -> i;
            case null, default -> 0;
        };
    }
}
```

**Listing 1.** `classic` is constant equality on `String`, not a type pattern. `typeTest` is pattern matching without a `switch`. `patterned` is a `switch` whose labels *are* patterns (Java 21).

> [!warning] `case "ok"` is not `case String s`
> A string constant label matches one value with `equals`. A type pattern `String s` matches every `String` and binds `s`. Mixing them up is a type error or a dominance error (`case Object o` before `case String s` does not compile).

> [!warning] Patterns make the `switch` enhanced
> One `case` pattern or `case null` turns a statement into an enhanced `switch`. It must then be exhaustive or it does not compile. A classic constant `switch` on `String` or an enum may still omit cases and silently do nothing.

> [!tip] Interview answer
> **Pattern matching tests a value against a pattern and binds variables; a `switch` statement picks a label for a selector.** Classic `switch` is constant equality, not pattern matching. `instanceof` gained type patterns in Java 16; `switch` gained `case` patterns in Java 21, and those switches must be exhaustive.
