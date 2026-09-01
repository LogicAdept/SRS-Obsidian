<!--
reps: 0
priority: 0
-->
#Java/Language/Primitives #Java/Language/Wrappers/Autoboxing/Cache #SRS

# Which wrapper types besides `Integer` cache boxed values?

> [!abstract] Short answer
> **`Boolean`, `Byte`, `Short`, `Character`, and `Long`.** Autoboxing/`valueOf` intern `true`/`false`; **every** `byte`; `short` and `long` in **-128..127**; and `char` in **`'\u0000'`..`'\u007F'`**. Only `Integer`’s high bound is raised by `-XX:AutoBoxCacheMax`. `Float` and `Double` have **no** integer-style identity cache. Use `equals`, not `==`.

## Who interned what

Language boxing of **constants** in those ranges must yield `==` identical references. The factories implement that (and more) by caching on every `valueOf` in range, not only on literals ([[How can you extend the Integer autobox cache maximum]], [[What method does the compiler insert when autoboxing an int]]).

| Type | Always interned | Notes |
| --- | --- | --- |
| `Boolean` | `true` and `false` | `TRUE` / `FALSE` — the whole type ([[What are Boolean.TRUE and Boolean.FALSE]]) |
| `Byte` | **all** 256 values | `byte` *is* **-128..127** |
| `Short` | **-128..127** | may cache more; `128` need not match |
| `Character` | `'\u0000'`..`'\u007F'` | ASCII only; `'€'` need not match |
| `Integer` | **-128..127** | high configurable |
| `Long` | **-128..127** | **not** extended by `AutoBoxCacheMax` |
| `Float` / `Double` | none required | do not treat `==` as value equality |

```d2
direction: down
yes: "Boolean Byte Short\nCharacter Integer Long" {
  width: 280
  height: 70
  style.fill: "#e8f5e9"
}
no: "Float Double" {
  width: 200
  height: 50
  style.fill: "#ffebee"
}
```

**Fig. 1.** Integral wrappers (plus `Boolean`) intern a small set; the floating wrappers do not.

```java
Boolean t1 = true, t2 = true;          // t1 == t2  (TRUE)
Byte b1 = (byte) 1, b2 = (byte) 1;     // b1 == b2  (all bytes cached)
Short s1 = 127, s2 = 127;              // s1 == s2
Short s3 = 128, s4 = 128;              // s3 == s4 not required
Character c1 = 127, c2 = 127;          // interned
Character c3 = 128, c4 = 128;          // not required
Long n1 = 127L, n2 = 127L;             // interned
Long n3 = 128L, n4 = 128L;             // not required

Double d1 = 1.0, d2 = 1.0;             // d1 == d2 not required
```

**Listing 1.** Conceptual: identity holds only inside each type’s interned set.

`new Byte((byte) 1)` still bypasses the cache, as `new Integer` does ([[What is the difference between Integer.valueOf and new Integer]]).

> [!warning] Dumps that skip `Long` are incomplete
> `Long.valueOf` is specified to cache **-128..127**, and boxing a `long` constant in that range must share identity. Raising `AutoBoxCacheMax` still does **not** grow the `Long` table — that flag is `Integer` only.

> [!warning] `==` is not an equals shortcut
> Inside the cached set, `==` can look like value equality and pass a unit test. Outside it, or with `Float`/`Double`, it fails. Prefer `equals` / `xxxValue()`.

> [!tip] Interview answer
> **Besides `Integer`, the caches are `Boolean` (both values), `Byte` (all of them), `Short` and `Long` in **-128..127**, and `Character` for ASCII `0..127`.** `Float` and `Double` do not get that deal. Only `Integer`’s maximum is tunable. Never use `==` to compare wrappers.
