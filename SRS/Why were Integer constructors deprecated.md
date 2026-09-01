<!--
reps: 0
priority: 0
-->
#Java/Language/Primitives #Java/Language/Wrappers/Autoboxing/Cache #Java/Versions/9 #SRS

# Why were `Integer` constructors deprecated?

> [!abstract] Short answer
> **`new Integer(int)` always allocates** and **skips the cache**. `Integer.valueOf(int)` (what autoboxing calls) **reuses** interned instances for **-128..127**. Since Java 9 the constructors are `@Deprecated(since = "9", forRemoval = true)` for that reason — they are **not** removed in Java 17 or 21. For text, use `parseInt` (primitive) or `valueOf` (wrapper), not `new Integer(String)`.

## Factory, not `new`

The `Integer(int)` JavaDoc: it is rarely appropriate; `valueOf(int)` is generally better **space and time** because it caches frequently requested values; the constructor **will be removed in a future release**. `new` never reads `IntegerCache` ([[What is the difference between Integer.valueOf and new Integer]], [[How can you extend the Integer autobox cache maximum]]).

The same deprecation applies to `Integer(String)` and to the other language wrappers (`Byte`, `Short`, `Long`, `Float`, `Double`, `Character`, `Boolean`). Prefer `valueOf` / autoboxing ([[What are the different ways of creating a Java wrapper instance]]).

```d2
direction: down
neu: "new Integer(100)\nalways a fresh object" {
  width: 260
  height: 70
  style.fill: "#ffebee"
}
val: "valueOf(100) / autobox\ncache hit" {
  width: 240
  height: 70
  style.fill: "#e8f5e9"
}
```

**Fig. 1.** Deprecation is about identity and allocation, not a change in the `int` payload.

```java
Integer a = Integer.valueOf(55);     // cache
Integer b = 55;                      // autoboxing → valueOf
// Integer c = new Integer(55);      // deprecated, always distinct
// Integer d = new Integer("55");    // deprecated; use valueOf("55") or parseInt

int n = Integer.parseInt("55");      // primitive — no object
```

**Listing 1.** Conceptual: supported factories vs the deprecated constructors.

Wrappers are value-based: code should not rely on identity. `new Integer(100) == new Integer(100)` is false even inside the cache range. That is the interview `==` trap, and a reason the constructors are on the way out ([[Are Java wrapper types immutable]]).

Older dumps still show `new Integer(55)`. Those lines compile **with deprecation warnings** on current JDKs. They did **not** vanish in 17.

> [!warning] Deprecated is not deleted
> `forRemoval = true` means the API owners intend to remove the constructors later. Java 17 and 21 still have them. Answering “removed in 17” is wrong; answering “never use `new Integer`” is right.

> [!tip] Interview answer
> **The constructors were deprecated in Java 9 because they always allocate and bypass the integer cache; `valueOf` and autoboxing do not.** They are marked for removal but still present. Parse with `parseInt` or box with `valueOf` — do not write `new Integer`.
