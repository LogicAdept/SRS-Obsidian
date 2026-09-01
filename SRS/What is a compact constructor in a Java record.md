<!--
reps: 0
priority: 0
-->
#Java/Language/Records/Constructors #SRS

# What is a compact constructor in a Java record?

> [!abstract] Short answer
> It is a **record-only spelling of the canonical constructor** that **omits the parameter list**. Write `Name { … }` instead of `Name(T a, U b) { … }`. The header parameters are implicit. You validate or **reassign those parameters**; you do **not** assign component fields. When the body completes normally, the compiler assigns each field from the corresponding parameter.

## Same constructor, shorter header

```d2
direction: down
compact: "public Range {\n  if (min > max) throw ...\n}" {
  width: 280
  height: 70
  style.fill: "#e3f2fd"
}
params: "implicit params min, max\nreassign / validate here" {
  width: 280
  height: 70
  style.fill: "#fff3e0"
}
assign: "compiler appends\nthis.min = min; this.max = max" {
  width: 300
  height: 70
  style.fill: "#e8f5e9"
}
compact -> params
params -> assign
```

**Fig. 1.** Compact is not a second constructor kind. It *is* the canonical constructor ([[What is a canonical constructor in a Java record]]) with the repetitive signature and field writes supplied by the compiler.

JLS §8.10.4.2: only a record declaration may use this form. Formal parameters are the derived list from the header (same names and types, including a trailing varargs component). In the body, the simple name `c` denotes that **parameter**, not the field. After the last statement completes normally, fields are initialized in **header order**.

The body must not contain `return`, `this(...)` / `super(...)`, or an assignment to a **component field**. That last rule is why you normalize with `value = value.trim()`, not `this.value = value.trim()`.

```java
record Rational(int num, int denom) {
    private static int gcd(int a, int b) {
        return b == 0 ? Math.abs(a) : gcd(b, a % b);
    }

    Rational {
        int g = gcd(num, denom);
        num /= g;
        denom /= g;
    }
}
```

**Listing 1.** JLS example: compact body **reassigns parameters**. Equivalent normal canonical constructor ends with `this.num = num; this.denom = denom`.

```java
public record Email(String value) {
    public Email {
        if (value == null || !value.contains("@"))
            throw new IllegalArgumentException("Invalid email");
        value = value.toLowerCase().trim();
    }
}
```

**Listing 2.** Validation plus normalisation. The compiler still writes `this.value = value` after this body. `this.value = …` in the compact body is a compile-time error.

You may declare extra constructors alongside a compact one; they still start with `this(...)` ([[Can a Java record declare additional constructors]]). You may **not** also declare a full-parameter canonical constructor. Compact constructors have no `throws` clause — wrap checked exceptions.

Deserialization still runs this constructor ([[How does Java serialization treat record classes]]), so compact checks apply to the stream as well as to `new`.

> [!warning] Reassign the parameter, never the field
> `this.min = min` is legal only in a **normal** canonical constructor. In compact form that assignment is illegal. `min = Math.min(min, max)` is the intended normalisation. A dump table that says “compact constructors cannot change parameters” contradicts both the JLS `Rational` example and this rule.

> [!warning] `this.x` is not initialized yet
> Fields are written **after** the compact body. Reading `this.min` in that body is a definite-assignment error (blank `final`). `this(...)` is also illegal. Using `this` as a receiver to leak a half-built instance is still the usual constructor footgun — the spec does not add a blanket ban on the word `this`.

> [!tip] Interview answer
> **A compact constructor is the canonical constructor without repeating the header: `RecordName { validate or rewrite the implicit parameters }`.** The compiler then assigns the component fields. Do not assign `this.x` in that body; do reassign the parameter `x` when you need to normalise. It is not a second constructor next to the canonical one.
