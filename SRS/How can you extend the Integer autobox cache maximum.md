<!--
reps: 0
priority: 0
-->
#Java/Language/Wrappers/Autoboxing/Cache #Java/JVM/Tuning #SRS

# How can you extend the Integer autobox cache maximum?

> [!abstract] Short answer
> On HotSpot, start the VM with **`-XX:AutoBoxCacheMax=<n>`**, choosing **`n` greater than 127**. The VM copies that number into the saved property `java.lang.Integer.IntegerCache.high`; `Integer.valueOf` then keeps instances from **-128 through `n`**. The low bound stays **-128**. This extra range is an OpenJDK cache, not a language identity guarantee.

## What is cached by default

`Integer.valueOf(int)` is the factory autoboxing uses. Its contract is to cache **-128..127** inclusive and to be allowed to cache values outside that range. Boxing conversion of an `int` constant in **-128..127** must yield indistinguishable references (`==`); for any other value the language forbids assuming identity.

OpenJDK implements that with a private `IntegerCache`: `low` is the constant **-128**, `high` starts at **127**, and `valueOf` returns `cache[i - low]` when `i` is in range, otherwise a fresh `Integer`. See [[How would you explain Integer cache valueOf(100)==valueOf(100) true, valueOf(200) false]] and [[What is the difference between Integer.valueOf and new Integer]].

```d2
direction: down
flag: "-XX:AutoBoxCacheMax=n" {
  width: 260
  height: 70
  style.fill: "#e3f2fd"
}
prop: "saved property\nIntegerCache.high = n" {
  width: 280
  height: 80
  style.fill: "#fff3e0"
}
cache: "IntegerCache array\n[-128 .. max(n, 127)]" {
  width: 300
  height: 80
  style.fill: "#e8f5e9"
}
hit: "valueOf(i) in range\nreturns cached instance" {
  width: 280
  height: 80
  style.fill: "#e8f5e9"
}
miss: "valueOf(i) outside range\nnew Integer(i)" {
  width: 280
  height: 80
  style.fill: "#ffebee"
}

flag -> prop
prop -> cache
cache -> hit
cache -> miss
```

**Fig. 1.** HotSpot feeds the XX flag into `IntegerCache.high`; only `valueOf` / autoboxing consult the array.

## Raising `high`

`IntegerCache` reads `VM.getSavedProperty("java.lang.Integer.IntegerCache.high")`. If the string parses as an `int`, it sets

`high = min(max(parsed, 127), Integer.MAX_VALUE - 128 - 1)`

so:

- a value **below 127 is ignored** for the ceiling — you cannot shrink the JLS range
- a value **above 127** extends the cache upward until the array would overflow
- a non-numeric property is ignored and `high` stays 127

HotSpot’s C2 flag `AutoBoxCacheMax` is documented as setting the max value cached by the `java.lang.Integer` autobox cache. When you actually pass the flag (it is no longer at its VM default), `arguments.cpp` does `add_property("java.lang.Integer.IntegerCache.high=<n>")`. Launch with:

```text
java -XX:AutoBoxCacheMax=256 YourMain
```

**Listing 1.** Conceptual VM launch: cache `Integer` instances through 256, still starting at -128.

```java
Integer a = Integer.valueOf(200);
Integer b = Integer.valueOf(200);
boolean same = (a == b);
// default high 127: typically false
// -XX:AutoBoxCacheMax=256 on HotSpot: true, because 200 is now in the array
```

**Listing 2.** Conceptual: `==` for 200 is a cache hit only after `high` is raised; `equals` / `intValue()` stay correct either way.

The flag’s own HotSpot default is **128**, but that default is **not** copied into `IntegerCache` until you set the option. Until then the Java cache high remains **127**. Passing `-XX:AutoBoxCacheMax=128` is the smallest explicit raise (it adds boxed `128`).

> [!warning] `==` outside -128..127 is not a language rule
> Extending the cache can make `Integer.valueOf(200) == Integer.valueOf(200)` true on that JVM. The boxing spec still withholds identity for values outside **-128..127**. Another vendor, a smaller flag, or `new Integer(200)` (deprecated; a newly allocated object) can make `==` false. Production code should use `equals` or `intValue()`.

> [!warning] The floor does not move, and `new` skips the cache
> There is no `AutoBoxCacheMin`. `low` is `final` **-128**. Setting `AutoBoxCacheMax` to 50 still caches **-128..127**. The flag names the **Integer** cache only; it does not retarget the other wrapper caches in [[Which wrapper types besides Integer cache boxed values]]. `new Integer(i)` never consults `IntegerCache`.

> [!tip] Interview answer
> **Raise HotSpot’s Integer cache with `-XX:AutoBoxCacheMax=<n>` and `n` greater than 127.** That sets `IntegerCache.high`; `valueOf` and autoboxing then reuse instances from -128 through `n`. The low bound stays -128, values above `high` still allocate, and `==` outside -128..127 remains an implementation extra — never a substitute for `equals`.
