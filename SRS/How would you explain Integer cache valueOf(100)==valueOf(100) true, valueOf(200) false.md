<!--
reps: 0
priority: 0
-->
#Java/Language/Primitives #Java/Language/Wrappers/Autoboxing/Cache #SRS

# How would you explain Integer cache `valueOf(100)==valueOf(100)` true, `valueOf(200)` false?

> [!abstract] Short answer
> **`Integer.valueOf` interned **-128..127**.** `100` is in that range, so both calls return the **same** cached object and `==` (identity) is true. `200` is outside the default cache, so each call **may allocate**; `==` is often false and is **never a language guarantee**. Autoboxing uses `valueOf`, so `Integer a = 100; Integer b = 100; a == b` is the same trick. Compare wrappers with `equals`.

## Identity is a cache hit, not value equality

`valueOf(int)` returns `IntegerCache.cache[i - low]` when `i` is between `low` (**-128**, fixed) and `high` (**127** unless you raised it). Otherwise it does `new Integer(i)` ([[How can you extend the Integer autobox cache maximum]], [[What is the difference between Integer.valueOf and new Integer]]).

Boxing conversion of **constants** in **-128..127** must yield `==` identical references. There is **no** such rule for `200`. JavaDoc: the method **may** cache other values. Default HotSpot does not intern `200`, so two `valueOf(200)` calls are typically distinct — until someone sets `-XX:AutoBoxCacheMax=200` or higher, which can make `valueOf(200) == valueOf(200)` true.

```d2
direction: down
hit: "valueOf(100)\nsame cached instance" {
  width: 260
  height: 70
  style.fill: "#e8f5e9"
}
miss: "valueOf(200)\nnew object (default)" {
  width: 260
  height: 70
  style.fill: "#ffebee"
}
```

**Fig. 1.** `==` follows interned identity, not the number’s magnitude except by accident of the range.

```java
Integer a = Integer.valueOf(100);
Integer b = Integer.valueOf(100);
boolean inRange = (a == b);          // true — cache

Integer c = Integer.valueOf(200);
Integer d = Integer.valueOf(200);
boolean out = (c == d);              // typically false; not guaranteed

Integer e = 100;
Integer f = 100;
boolean boxed = (e == f);            // true — autoboxing is valueOf

boolean byValue = c.equals(d);       // true — use this
```

**Listing 1.** Conceptual: range hit, range miss, autoboxing, `equals` ([[What method does the compiler insert when autoboxing an int]]).

`new Integer(100) == new Integer(100)` is **false** even in range: `new` never reads the cache. `Byte`/`Short`/`Long` intern **-128..127** too; `Character` intern `0..127`; `Boolean` intern both values. `Float`/`Double` do not ([[Which wrapper types besides Integer cache boxed values]]).

> [!warning] Do not memorize “200 always false” as a spec
> The exam fact is **guaranteed identity only for **-128..127** (and the other interned wrappers).** `200` is the usual counterexample on an unmodified HotSpot. Raising the cache high, or a different runtime, can intern `200`. `equals` does not care.

> [!tip] Interview answer
> **`valueOf` reuses one `Integer` per value in **-128..127**, so two `100`s are the same object and `==` is true.** `200` is outside that table by default, so you get two objects and `==` is false. Autoboxing is `valueOf`, which is why boxed literals play the same trick. Always `equals` for wrapper value.
