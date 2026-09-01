<!--
reps: 0
priority: 0
-->
#Java/Language/Switch #Java/String #SRS

# Can you use strings in a Java `switch` statement?

> [!abstract] Short answer
> **Yes, from Java 7.** A `switch` statement may select on a `String`. `case` labels are string constants matched with `String.equals` (case-sensitive, not `==`). A `null` selector throws `NullPointerException`; `default` does not catch it. Java 6 and earlier do not allow a `String` selector.

## Selector type and `case` constants

A Java 7 `switch` statement accepts `char`, `byte`, `short`, `int`, `Character`, `Byte`, `Short`, `Integer`, `String`, or an enum. Enums were already legal in Java 5 ([[Can you use a Java enum in a switch]]). String *constant* labels require the selector type to be `String`. `CharSequence` or `StringBuilder` is not that type. From Java 21 an enhanced `switch` may select on any reference type, but then you match with patterns, not `"INFO"` constants.

Each `case` label must be a compile-time constant expression assignable to `String`: a literal, or a `final String` initialized with a constant expression ([[What is a compile-time constant in Java]]). A runtime variable, a method call, and `null` are illegal labels on a classic `String` switch. Two labels with the same string value do not compile.

## Matching

The statement compares the selector to each `case` constant as if it called `String.equals`. Two distinct `String` objects with the same characters match; identity (`==`) is not used ([[Why should arbitrary objects not be compared with double equals in Java]]). `"INFO"` does not match `"info"`. Constant-label matching does not use `equalsIgnoreCase`.

If the selector is `null`, the statement throws `NullPointerException` and no label runs. That happens **before** `equals`. `String.equals(null)` would return `false`; a `String` `switch` never gets there. `default` does not apply to `null`. From Java 21, `case null` on an enhanced `switch` applies instead of throwing.

Colon labels still fall through. Arrow arms and `switch` expressions (Java 14) do not. The compiler generates generally more efficient bytecode for a `String` `switch` than for an equivalent `if` / `else` `equals` chain.

```d2
direction: down
stmt: "switch (level)  // String" {
  width: 280
  height: 50
  style.fill: "#e3f2fd"
}
nullSel: "null selector\nNullPointerException\n(case null only in Java 21+)" {
  width: 320
  height: 80
  style.fill: "#ffebee"
}
match: "equals against case constants\ncase-sensitive" {
  width: 300
  height: 70
  style.fill: "#e8f5e9"
}
miss: "no constant matches\ndefault, or complete normally" {
  width: 300
  height: 70
  style.fill: "#fff8e1"
}

stmt -> nullSel
stmt -> match
match -> miss
```

**Fig. 1.** Null fails before any label. Non-null values are matched with `equals`; `default` is only for a non-null leftover.

```java
class LogRoute {
    static int rank(String level) {
        switch (level) {
            case "ERROR":
                return 3;
            case "WARN":
                return 2;
            case "INFO":
                return 1;
            case "DEBUG":
            case "TRACE":
                return 0;
            default:
                throw new IllegalArgumentException(level);
        }
    }
}
```

**Listing 1.** Classic `switch` statement on `String`. `"INFO"` and `"info"` take different paths. `rank(null)` throws `NullPointerException` even though `default` is present.

```java
class LogRouteExpr {
    static int rank(String level) {
        return switch (level) {
            case "ERROR" -> 3;
            case "WARN" -> 2;
            case "INFO" -> 1;
            case "DEBUG", "TRACE" -> 0;
            default -> throw new IllegalArgumentException(level);
        };
    }
}
```

**Listing 2.** `switch` expression on `String` (Java 14). Same matching rules; arrow arms do not fall through. A null selector still throws.

> [!warning] `default` does not absorb `null`
> `rank(null)` throws `NullPointerException` with Listing 1 as written. The `"INFO".equals(level)` trick that keeps an `if` chain from throwing does not apply: the language throws on a null selector before any `equals` call. Test for `null` first, or in Java 21+ add `case null`.

> [!warning] Labels are case-sensitive
> `"Warn"` does not match `case "WARN"`. If callers mix case, normalize the selector with an explicit `Locale` before the `switch`. `equalsIgnoreCase` is not part of constant-label matching.

> [!tip] Interview answer
> **Yes — Java 7 added `String` as a `switch` selector.** Cases are constant strings compared with `equals`, so matching is case-sensitive and ignores object identity. A null selector throws `NullPointerException`; `default` does not handle it. Before Java 7 only the integral types (except `long`), their wrappers, and enums were legal.
