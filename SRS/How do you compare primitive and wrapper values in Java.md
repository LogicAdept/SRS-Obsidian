<!--
reps: 0
priority: 0
-->
#Java/Language/Primitives #Java/Language/Wrappers #SRS

# How do you compare primitive and wrapper values in Java?

> [!abstract] Short answer
> **`int` vs `int`:** `==` is numeric equality. **`int` vs `Integer`:** `==` **unboxes** the wrapper, then compares bits — `null` throws `NullPointerException`. **`Integer` vs `Integer`:** `==` is **identity** (cache can fake equality in **-128..127**); use **`equals`** for value. For ordering, `Integer.compare(a, b)` or `compareTo` (NPE if the receiver is `null`).

## Three shapes of `==`

If either side is a primitive numeric type (or unboxes to one), `==` is **numerical** equality: binary numeric promotion, which **unboxes** ([[What method does the compiler insert when unboxing an Integer]]). If both sides are references, `==` is **identity** — same object or both `null` — not the same rule as `int`.

`boolean` / `Boolean` is the same split: mixed `==` unboxes; two `Boolean`s are identity (`TRUE`/`FALSE` happen to intern both values).

```d2
direction: down
mix: "int == Integer\nunbox, then numeric" {
  width: 280
  height: 70
  style.fill: "#e3f2fd"
}
refs: "Integer == Integer\nidentity, not value" {
  width: 280
  height: 70
  style.fill: "#ffebee"
}
eq: "a.equals(b)\nvalue" {
  width: 200
  height: 50
  style.fill: "#e8f5e9"
}
```

**Fig. 1.** Mixed `==` unboxes; two wrappers need `equals`.

```java
int p = 100;
Integer w = 100;
Integer w2 = 100;
Integer big = 200;
Integer big2 = 200;
Integer missing = null;

boolean mixed = (p == w);            // true — unbox w
boolean cached = (w == w2);          // true — cache identity
boolean uncached = (big == big2);    // not required; often false
boolean value = big.equals(big2);    // true
// boolean boom = (p == missing);    // NPE — unbox null
boolean bothNull = (missing == null); // true — reference ==

int ord = Integer.compare(p, w);     // unboxes w; NPE if w is null
```

**Listing 1.** Conceptual: numeric `==`, identity `==`, `equals`, and `compare` ([[What is the difference between int and Integer in Java]], [[Which wrapper types besides Integer cache boxed values]]).

`equals` on `Integer` is value equality with another `Integer` (not with an `int` — that would be `equals` on a boxed argument, or just `==` after unbox). `a.equals(b)` NPEs if `a` is `null`; `Objects.equals(a, b)` does not.

`<` / `>` / `compareTo` on wrappers unbox or dereference; a `null` operand throws. Primitive-only comparison has no that hazard ([[How do you compare primitive values in Java]], [[Why cannot a Java primitive variable be null]]).

> [!warning] `==` on two `Integer`s is not “the int value”
> `Integer a = 100; Integer b = 100; a == b` can pass because of the cache. Change to `200` and the same snippet can fail. Interviewers mix `==` with `equals` on purpose. Prefer `equals` / `intValue()` / `Integer.compare`.

> [!tip] Interview answer
> **Compare `int`s with `==`. Compare an `int` to an `Integer` with `==` only if you accept unboxing — `null` explodes.** Two `Integer`s need `equals` (or `compare`); `==` tests identity and the cache will lie for small numbers. Never use `==` as value equality on wrappers.
