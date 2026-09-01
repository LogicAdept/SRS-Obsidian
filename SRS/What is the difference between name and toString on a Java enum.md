<!--
reps: 0
priority: 0
-->
#Java/Language/Enum #SRS

> [!abstract] Short answer
> **`name()` is the constant’s exact source identifier and is `final`. `toString()` is the display string: it defaults to that same identifier and may be overridden.** Prefer `toString()` for humans. Prefer `name()` when the string must round-trip with `valueOf` or travel as the constant’s identity.

## Identity vs display

`java.lang.Enum` stores the identifier in a private `name` field filled from the declaration. `name()` returns that field and cannot be overridden. `toString()` returns the same field unless the enum type overrides it ([[Can you override toString on a Java enum]]). The API tells you most code should print `toString()`, and should call `name()` only when correctness depends on the identifier not changing from release to release.

`name()` is inherited from `Enum`. It is not one of the compiler-generated methods (`values()`, `valueOf(String)`). Those generated methods, and `Enum.valueOf(Class, String)`, match the **identifier** — exact spelling, case-sensitive, no trim ([[How do you convert a String to a Java enum]]). They never consult `toString()`.

Print, string concat, and logs call `toString()`. Serialization of an enum constant writes `name()`, then reconstitutes with `valueOf` ([[How does Java serialization treat enum constants]]).

```d2
direction: down
id: "declaration identifier\nHEARTS" {
  width: 240
  height: 50
  style.fill: "#e3f2fd"
}
nm: "name()  final\nvalueOf / serialization" {
  width: 280
  height: 70
  style.fill: "#e8f5e9"
}
ts: "toString()  overridable\nprint, logs, UI" {
  width: 280
  height: 70
  style.fill: "#fff3e0"
}

id -> nm
id -> ts: "default; you may change"
```

**Fig. 1.** Same default string. Only `toString` is allowed to diverge.

```java
enum Suit {
    HEARTS("♥"), SPADES("♠");
    private final String symbol;
    Suit(String symbol) { this.symbol = symbol; }
    @Override public String toString() { return symbol; }
}

class Demo {
    static String roundTrip() {
        String id = Suit.HEARTS.name();       // "HEARTS"
        Suit back = Suit.valueOf(id);         // HEARTS
        return back.toString();               // "♥"
        // Suit.valueOf("♥") throws IllegalArgumentException
    }
}
```

**Listing 1.** Display is `♥`. Lookup and identity stay `HEARTS`.

> [!warning] Do not `valueOf(e.toString())` after a custom `toString`
> That call succeeds only while `toString()` still equals `name()`. A friendlier label, a translation, or a symbol breaks the round-trip. Identity is `valueOf(e.name())`.

> [!warning] `println(e)` is not `e.name()`
> After Listing 1, `System.out.println(Suit.HEARTS)` prints `♥`. Debugging a wire protocol that expected `HEARTS` from logs will mislead you.

> [!tip] Interview answer
> **`name()` is `final` and returns the exact constant identifier; `toString()` defaults to that string but can be overridden for display.** `valueOf` and serialization use the identifier, not your `toString`. Print for humans with `toString()`; persist or parse with `name()`.
