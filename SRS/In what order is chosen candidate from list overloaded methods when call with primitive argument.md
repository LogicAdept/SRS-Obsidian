<!--
reps: 0
priority: 0
-->
#Java/Language/Primitives #Java/Language/Wrappers/Autoboxing #SRS

# In what order is a candidate chosen from overloaded methods when called with a primitive argument?

> [!abstract] Short answer
> Overload resolution walks **three phases**. **Phase 1** (strict): identity and **widening** only — no boxing, no varargs. If several match, the **most specific** primitive wins (`int` over `long` over `float` …). **Phase 2** (loose): **boxing** / unboxing, still fixed arity. **Phase 3**: **varargs**, with boxing allowed. An `int` argument prefers `m(int)` then `m(long)`/`m(float)` before `m(Integer)` before `m(int...)`.

## Three phases, then most specific

Applicability is tested in order so pre-Java-5 calls stay unambiguous after boxing and varargs arrived ([[Why does autoboxing exist in Java]]). The search **stops** at the first phase that has any applicable method; only then is “most specific” applied **inside that phase**.

1. **Strict** — `int` → `int` (identity) or `int` → `long` / `float` / `double` (widening). **No** `Integer`, **no** `int...`.
2. **Loose** — boxing allowed: `int` → `Integer` (then maybe `Number` / `Object`) ([[When does autoboxing occur in Java]], [[What method does the compiler insert when autoboxing an int]]).
3. **Varargs** — `m(int...)`, `m(Object...)`, including boxing into `m(Integer...)`.

Widening among primitives, most specific first: `byte` → `short` → `int` → `long` → `float` → `double`. `char` widens to `int` → `long` → `float` → `double` (not to `short`). Invocation still does **not** narrow (`m(byte)` is not applicable to a non-constant `int`) ([[What are the autoboxing rules when assigning a primitive to a wrapper]]).

```d2
direction: down
p1: "Phase 1 strict\nint / long / float / double" {
  width: 300
  height: 70
  style.fill: "#e8f5e9"
}
p2: "Phase 2 loose\nInteger / Number / Object" {
  width: 300
  height: 70
  style.fill: "#e3f2fd"
}
p3: "Phase 3 varargs\nint... / Object..." {
  width: 280
  height: 70
  style.fill: "#fff3e0"
}
p1 -> p2 -> p3
```

**Fig. 1.** Later phases run only if the earlier phase found nobody.

```java
void m(int i) { }
void m(long l) { }
void m(Integer i) { }
void m(int... xs) { }

m(10);           // m(int) — phase 1 exact, most specific

// If m(int) is absent:
// m(10) → m(long)     // still phase 1 widening; Integer is not considered
// If only Integer and int... remain:
// m(10) → m(Integer)  // phase 2 beats varargs
```

**Listing 1.** Conceptual: `int` vs `long` vs `Integer` vs `int...` for argument `10`.

The interview trap is `m(long)` competing with `m(Integer)`: widening lives in phase 1, boxing in phase 2, so **`long` wins**. `m(int)` vs `m(float)` is both phase 1; `int` is more specific.

> [!warning] Exact and widening are the same phase
> Dumps that list “exact, then widening, then box, then varargs” as four **phases** are slightly wrong. Exact and widening are both **phase 1**; most-specific then picks `int` over `long`. Boxing is not “a little worse widening.” It is a later phase, which is why it loses to `long`.

> [!tip] Interview answer
> **For a primitive argument the compiler tries identity and widening first, then boxing, then varargs.** So `m(int)` beats `m(long)` beats `m(Integer)` beats `m(int...)`. If you only have `long` and `Integer`, `int` widens to `long` and never boxes. That order exists so old overloads did not become ambiguous in Java 5.
