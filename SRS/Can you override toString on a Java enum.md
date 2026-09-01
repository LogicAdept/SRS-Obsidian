<!--
reps: 0
priority: 0
-->
#Java/Language/Enum #SRS

# Can you override `toString` on a Java enum?

> [!abstract] Short answer
> **Yes.** `Enum.toString` is not `final`. The default returns the constant’s declared identifier (the same string `name()` returns). Override it when you want a friendlier display. `name()` stays `final`, and `valueOf` still matches that identifier — not your `toString` ([[What is the difference between name and toString on a Java enum]]).

## Default vs override

`java.lang.Enum` documents that `toString` *may* be overridden, though it often is unnecessary. Unlike `compareTo`, `equals`, `hashCode`, `name`, and `ordinal`, it is an ordinary instance method ([[Can you override compareTo on a Java enum]]).

```java
public String toString() {
    return name;
}
```

**Listing 1.** Default in `java.lang.Enum` (JDK 21). `name` is the private field filled from the constant identifier; `name()` is the `final` getter for the same value.

```d2
direction: down
id: "constant identifier\nRED" {
  width: 220
  height: 55
  style.fill: "#e3f2fd"
}
ts: "toString()\noverridable display" {
  width: 240
  height: 60
  style.fill: "#e8f5e9"
}
nm: "name() / valueOf\nfinal identity" {
  width: 240
  height: 60
  style.fill: "#fff3e0"
}

id -> ts
id -> nm
```

**Fig. 1.** Display can change. The identifier used by `name()` and `valueOf` cannot.

You can override once on the enum type, or per constant in a class body (same rules as other instance methods).

```java
enum Traffic {
    RED("stop"), GREEN("go");

    private final String label;
    Traffic(String label) { this.label = label; }

    @Override
    public String toString() { return label; }
}

// Traffic.RED.toString() -> "stop"
// Traffic.RED.name()     -> "RED"
// Traffic.valueOf("RED") -> RED
// Traffic.valueOf("stop") throws IllegalArgumentException
```

**Listing 2.** Friendly `toString` does not change lookup. Conversion from a string still uses the declared name ([[How do you convert a String to a Java enum]]).

Print, string concat, and many log APIs call `toString`, so the override shows up widely. Serialization of enum constants does **not** use it; it is based on the constant identity/name ([[How does Java serialization treat enum constants]]).

> [!warning] `valueOf` and `name()` ignore your `toString`
> `valueOf("stop")` does not find `RED` after Listing 2. Round-trip identity is `name()` → `valueOf(name())`. Using `toString()` as a map key or wire value breaks when the display text changes or collides.

> [!warning] Override only for display, not for identity
> The platform prefers `toString` for humans and `name()` when the exact identifier must not vary. If two constants would print the same string, you still have two instances; `equals` remains identity.

> [!tip] Interview answer
> **Yes — `toString` is the one `Enum` method you are expected to be able to override.** By default it returns the constant name. `name()` is `final` and `valueOf` still wants that identifier, so a prettier `toString` is display only.
