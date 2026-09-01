<!--
reps: 0
priority: 0
-->
#Java/Language/Enum #SRS

# How do you convert a `String` to a Java enum?

> [!abstract] Short answer
> Call the enum’s implicit `public static E valueOf(String name)`. The string must be exactly the constant’s identifier — same case, no extra whitespace. A miss throws `IllegalArgumentException`; a `null` name throws `NullPointerException`. That lookup uses `name()`, not `toString()`. When you only have a `Class` object, use `Enum.valueOf(enumClass, name)` instead.

## Two `valueOf` methods

The compiler declares `public static E valueOf(String name)` on each enum type `E`. It is **not** inherited from `java.lang.Enum` the way `name()` and `ordinal()` are. `Enum` does provide a different helper: `static <T extends Enum<T>> T valueOf(Class<T> enumClass, String name)`. The typed `Color.valueOf("RED")` is the usual call; the `Class` form is for reflective or generic code.

The name must match an identifier used to declare a constant. No trimming. Reverse direction: `name()` (always) and default `toString()` (unless overridden) produce that same identifier ([[What is the difference between name and toString on a Java enum]]).

```d2
direction: down
s: "\"RED\"" {
  width: 140
  height: 45
  style.fill: "#fff3e0"
}
vo: "Color.valueOf(s)" {
  width: 200
  height: 50
  style.fill: "#e8f5e9"
}
c: "Color.RED" {
  width: 160
  height: 45
  style.fill: "#e3f2fd"
}
nm: "name() -> \"RED\"" {
  width: 180
  height: 45
  style.fill: "#e3f2fd"
}

s -> vo -> c -> nm
```

**Fig. 1.** Identifier string → constant → identifier string. A custom `toString` is not on this path.

```java
enum Color { RED, GREEN, BLUE }

class Demo {
    Color byName() {
        return Color.valueOf("RED");                 // RED
        // Color.valueOf("red")  -> IllegalArgumentException
        // Color.valueOf(" RED") -> IllegalArgumentException
        // Color.valueOf(null)   -> NullPointerException
        // java.lang.Enum.valueOf(Color.class, "GREEN") -> GREEN
    }
}
```

**Listing 1.** Exact match only. JDK 21’s `Enum.valueOf` message is `No enum constant` plus the canonical type name and the bad token — not a reason to parse exception text.

You cannot declare another `valueOf(String)` on the enum; it would clash with the implicit method. You also cannot make the generated method ignore case.

## When the wire format is not the identifier

If callers send `"red"` or a display label, write your own parser on top of `values()` ([[How do you iterate over all Java enum constants]]). That is application code, not a second platform `valueOf`.

```java
enum Color {
    RED, GREEN, BLUE;

    static Color parse(String s) {
        for (Color c : Color.values()) {
            if (c.name().equalsIgnoreCase(s)) {
                return c;
            }
        }
        throw new IllegalArgumentException("No color named " + s);
    }
}
```

**Listing 2.** Case-insensitive factory you maintain. It still keys off `name()`, not `toString()`. After `toString` is overridden to `"stop"` for `RED`, `valueOf("stop")` still fails ([[Can you override toString on a Java enum]]).

> [!warning] `valueOf` is case-sensitive and does not trim
> `"red"`, `"Red"`, `"RED "`, and `"RED"` are four different keys. Only the last one is `Color.RED`. Catch `IllegalArgumentException` at a boundary; do not treat `valueOf` as a validator that returns `null`.

> [!warning] Overriding `toString` does not change lookup
> `valueOf` matches the declaration identifier. `name()` is `final` and is the round-trip partner. Using `toString()` as the map key and `valueOf` as the reverse is a common production bug.

> [!warning] `valueOf` is generated; `name()` / `ordinal()` are inherited
> Interview lists that dump `values`, `valueOf`, `name`, and `ordinal` as one “compiler-added” bundle mix two origins. `values()` and `valueOf(String)` are implicit on the enum type. `name()` and `ordinal()` live on `Enum`.

> [!tip] Interview answer
> **Use the generated `valueOf(String)` — the argument must be the exact constant name.** Wrong token → `IllegalArgumentException`, `null` → `NullPointerException`. `toString` is display; `name()` / `valueOf` are identity. For ignore-case input, loop `values()` yourself.
