<!--
reps: 0
priority: 0
-->
#Java/Language/Wrappers/Autoboxing #Java/Collections #Java/Exceptions/Unchecked #SRS

# How do you avoid `NullPointerException` when unboxing a `Map` value?

> [!abstract] Short answer
> **Do not assign `map.get(key)` straight to a primitive.** `get` returns `null` when the key is missing (and when a stored value is `null`). Unboxing that wrapper throws `NullPointerException`. Keep the wrapper, default with `getOrDefault` / `requireNonNullElse` / `Optional.ofNullable`, or use `containsKey` when those two `null`s must stay distinct.

## `get` returns a wrapper; unboxing does not tolerate `null`

`Map.get` returns the mapped value, or `null` if there is no mapping. On a map that permits `null` values, that same `null` can also mean “this key is present and mapped to `null`.” `containsKey` is the operation that tells those cases apart ([[Can TreeMap have null keys or null values]]).

Assigning an `Integer` (or `Long`, `Boolean`, …) to a primitive performs unboxing. If the reference is `null`, that conversion throws `NullPointerException` ([[What is unboxing]], [[What method does the compiler insert when unboxing an Integer]], [[What is NullPointerException]]).

```d2
direction: down
get: "map.get(key)" {
  width: 280
  height: 50
  style.fill: "#e3f2fd"
}
n: "null (missing or stored null)" {
  width: 300
  height: 50
  style.fill: "#fff8e1"
}
npe: "int x = that Integer\nNullPointerException" {
  width: 280
  height: 70
  style.fill: "#ffebee"
}
ok: "null-check, getOrDefault,\nor requireNonNullElse" {
  width: 300
  height: 70
  style.fill: "#e8f5e9"
}
get -> n
n -> npe
n -> ok
```

**Fig. 1.** The failure is unboxing `null`, not `Map` itself.

```java
import java.util.HashMap;
import java.util.Map;
import java.util.Objects;
import java.util.Optional;

class Demo {
    static int boom(Map<String, Integer> map) {
        return map.get("k");
    }

    static int orDefault(Map<String, Integer> map) {
        return map.getOrDefault("k", 0);
    }

    static int coalesce(Map<String, Integer> map) {
        return Objects.requireNonNullElse(map.get("k"), 0);
    }

    static int optional(Map<String, Integer> map) {
        return Optional.ofNullable(map.get("k")).orElse(0);
    }

    static int inspect(Map<String, Integer> map) {
        Integer wrapped = map.get("k");
        if (wrapped == null) {
            return 0;
        }
        return wrapped;
    }
}
```

**Listing 1.** `boom` compiles and throws at run time if `get` is `null`. `orDefault` substitutes `0` only when the key is **absent**. `coalesce` and `optional` treat any `null` from `get` as `0`. `inspect` unboxes only after a non-null check ([[How do you prevent a NullPointerException]]).

`getOrDefault(key, defaultValue)` returns the mapped value, or `defaultValue` if the map contains **no mapping** for the key. The default (`0`) is assignment-compatible with `Integer` via boxing.

`Objects.requireNonNullElse(map.get(key), 0)` and `Optional.ofNullable(map.get(key)).orElse(0)` both replace a `null` **result** with `0`, whether that `null` meant missing or a stored `null`.

> [!warning] `getOrDefault` still unboxes a stored `null`
> If the key is present and mapped to `null`, `getOrDefault` returns that `null`, not the default. `int val = map.getOrDefault("k", 0)` then throws `NullPointerException`. Maps that forbid null values (`ConcurrentHashMap`, `Hashtable`, `EnumMap`) do not have this case; `HashMap` / `TreeMap` / `LinkedHashMap` do ([[Does ConcurrentHashMap allow null keys or values]], [[Does LinkedHashMap allow null keys or values]]).

> [!warning] Default `0` is not the same as “not present”
> Using `0` (or `orElse(0)`) collapses “missing,” and sometimes “stored null,” into a real primitive. If `0` is a legitimate stored count, use `containsKey` (or keep `Integer`) instead of pretending absence equals zero.

> [!tip] Interview answer
> **`Map.get` can be `null`; unboxing that to `int` throws `NullPointerException`.** Use a wrapper null-check, `getOrDefault` when a present `null` cannot occur, or `requireNonNullElse` / `Optional.ofNullable` when any `null` should become a default. Do not confuse a missing key with a stored `0`.
